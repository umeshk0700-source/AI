# Day 32 — Packaging & IaC cheat sheet

## Container images
- An image = stack of read-only **layers**, each the fs diff of one build step, content-addressed.
- Cache rule: a layer is reused iff its instruction **and every layer before it** are unchanged.
- Order instructions **least-changing → most-changing**: base → system deps → `requirements.txt`
  → `pip install` → app code → CMD.
- Production Dockerfile: multi-stage (build tools don't ship), non-root `USER`, pinned base tag
  (digest in prod), `.dockerignore` (`.env`, `.git`, tests, notebooks), `HEALTHCHECK`,
  logs to stdout.

## Declarative infra
- **desired** (config) → **recorded** (state file) → **real** (the cloud).
- `plan` = diff(desired, recorded). **drift** = diff(recorded, real).
- `apply` executes the plan, updates state. Re-apply of an unchanged config = no-op (idempotent).
- Dependencies form a DAG (Terraform infers it from interpolations); create in topo order,
  destroy in reverse.
- State lives in remote storage (S3) with a lock — never only on a laptop.

## Terraform anatomy
- `terraform { backend "s3" {...} }` — remote, locked state.
- `resource "type" "name" { ... }` — one managed object; `type.name` is its address.
- `${aws_x.y.attr}` interpolation ⇒ implicit `depends_on`.
- `variable` / `-var` — CI passes `image_tag = $GIT_SHA` (immutable tag).
- `plan` in the PR for review; `apply` after merge.

## Config & secrets (12-factor)
- **Config** (model name, MAX_TOKENS, index URI) → env vars, not baked in. One image, all envs.
- **Secrets** (API keys, DB pw) → secrets manager, injected at container start, in memory only.
  Never in the image, `main.tf`, or console-visible env.
- **Disposability** — on `SIGTERM`: stop accepting, drain in-flight LLM calls, exit within grace.
- **Parity** — same image dev→prod; real backing services in dev, not stubs.
- Pipeline hygiene: scan on push, SBOM, sign, deploy only passing immutable tags.
