"""RAG API Lambda handler (Day 30).

Runs behind API Gateway HTTP API. Module-scope init runs once per cold start and is
reused by every warm invocation. Keep NO model in this function — embeddings and
generation go through Bedrock; retrieval is a query to the vector DB.

Local testing:  python invoke.py
Deploy:         sam build && sam deploy --guided
"""
import json
import os
import time
import hashlib

_COLD_START_T = time.time()


def _init():
    """Expensive, once-per-container setup: clients, config, secrets. No model, no KB."""
    # import boto3
    # bedrock = boto3.client("bedrock-runtime")
    # secrets = boto3.client("secretsmanager")
    # db_creds = json.loads(secrets.get_secret_value(SecretId=os.environ["VECTOR_DB_SECRET"])["SecretString"])
    return {
        "model_id": os.environ.get("MODEL_ID", "anthropic.claude-sonnet-4-5-20250929-v1:0"),
        # demo KB stand-in; in production this lives in pgvector / a Bedrock Knowledge Base
        "kb": {
            "refund": "Refunds are issued within 5 business days to the original payment method.",
            "shipping": "Standard shipping is free on orders over $50 and takes 3-5 business days.",
            "api": "The API allows 600 requests per minute per key; it returns HTTP 429 when exceeded.",
        },
    }


STATE = _init()
INIT_MS = round((time.time() - _COLD_START_T) * 1000, 1)


def _rag_answer(question, state):
    """Stand-in for the real pipeline: retrieve from the vector DB, then call Bedrock.

    Replace with:
        q_vec = embed_via_bedrock(question)
        chunks = vector_db.search(q_vec, k=3)
        answer = bedrock_generate(state["model_id"], question, chunks)
    """
    q = question.lower()
    hit = next((v for k, v in state["kb"].items()
                if k in q or any(w in q for w in k.split())), None)
    if not hit:
        return "I don't have information on that in the knowledge base.", []
    return hit, [k for k in state["kb"] if k in q]


def _response(status, body, trace_id):
    return {
        "statusCode": status,
        "headers": {
            "content-type": "application/json",
            "x-trace-id": trace_id,
            "access-control-allow-origin": "*",
        },
        "body": json.dumps(body),
    }


def handler(event, context=None):
    trace_id = (getattr(context, "aws_request_id", None)
                or hashlib.md5(json.dumps(event, sort_keys=True).encode()).hexdigest()[:16])
    t0 = time.time()
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method")
        if method == "OPTIONS":
            return _response(204, {}, trace_id)  # CORS preflight

        body = json.loads(event.get("body") or "{}")
        question = (body.get("question") or "").strip()
        if not question:
            return _response(400, {"error": "missing 'question'"}, trace_id)
        if len(question) > 2000:
            return _response(413, {"error": "question too long (max 2000 chars)"}, trace_id)

        answer, sources = _rag_answer(question, STATE)
        latency_ms = round((time.time() - t0) * 1000, 1)
        print(json.dumps({
            "evt": "rag_request", "trace_id": trace_id, "q_len": len(question),
            "n_sources": len(sources), "latency_ms": latency_ms, "cold_start_ms": INIT_MS,
        }))
        return _response(200, {
            "answer": answer, "sources": sources,
            "trace_id": trace_id, "latency_ms": latency_ms,
        }, trace_id)

    except json.JSONDecodeError:
        return _response(400, {"error": "invalid JSON body"}, trace_id)
    except Exception as e:  # noqa: BLE001 — top-level guard; never leak the stack to the client
        print(json.dumps({"evt": "error", "trace_id": trace_id, "error": repr(e)}))
        return _response(500, {"error": "internal error", "trace_id": trace_id}, trace_id)
