import os
import pytest
from llmlab import get_embedder, settings
from kbsearch.retriever import HybridRetriever
from kbsearch.evaluate import evaluate

pytestmark = pytest.mark.live
_LIVE = os.getenv("LLM_LIVE") == "1"

ARTICLES = [
  "Password reset: click 'Forgot password' on the sign-in page. The email link is valid for one hour. After five failed attempts the account locks for 30 minutes.",
  "Exporting data: use the Export button on any report to download a CSV. Large exports are emailed as a link within 24 hours.",
  "Invoices & receipts: download past invoices as PDF from Account > Billing. Invoices are issued on the first of each month.",
  "API rate limits: 600 requests per minute per key. Exceeding the limit returns HTTP 429 with a Retry-After header.",
  "Two-factor authentication: enable 2FA under Security. We support authenticator apps (TOTP) and SMS backup codes.",
  "Single sign-on (SSO): SAML SSO is available on Enterprise plans. Configure the IdP metadata URL under Security > SSO.",
  "Data retention: deleted projects are recoverable for 14 days, then permanently purged. Account deletion is immediate and irreversible.",
  "Webhooks: register endpoints under Developer > Webhooks. Failed deliveries retry with exponential backoff for up to 24 hours.",
  "Seats & billing: adding a seat is prorated for the current period. Removing a seat credits the next invoice.",
  "Supported browsers: the latest two versions of Chrome, Firefox, Safari and Edge. Internet Explorer is not supported.",
  "Mobile app: available for iOS and Android. Offline changes sync automatically when the device reconnects.",
  "Error E-5501: this occurs when a report references a deleted data source. Re-point the report to an active source.",
  "Custom domains: map a CNAME to cname.example.com and add the domain under Settings > Domains. TLS is provisioned automatically.",
  "Audit log: Enterprise admins can export the audit log (JSON) for the last 90 days under Security > Audit.",
  "Notifications: choose email, in-app or Slack per event type under Preferences > Notifications.",
]

QUERIES = [
  {"q": "how long is the password reset email good for", "relevant": [0]},
  {"q": "get a CSV of my report", "relevant": [1]},
  {"q": "where do I download my bill", "relevant": [2]},
  {"q": "what status code do I get when rate limited", "relevant": [3]},
  {"q": "turn on 2FA", "relevant": [4]},
  {"q": "set up SAML for my company", "relevant": [5]},
  {"q": "can I get back a project I deleted", "relevant": [6]},
  {"q": "my webhook endpoint keeps failing", "relevant": [7]},
  {"q": "does adding a user cost a full month", "relevant": [8]},
  {"q": "is IE supported", "relevant": [9]},
  {"q": "does the phone app work without internet", "relevant": [10]},
  {"q": "what is error E-5501", "relevant": [11]},
  {"q": "use my own domain name", "relevant": [12]},
  {"q": "export the audit trail", "relevant": [13]},
  {"q": "send alerts to slack", "relevant": [14]},
]


@pytest.mark.skipif(not _LIVE, reason="live")
def test_hybrid_recall_on_real_embeddings():
    provider = "openai" if settings.has("openai") else "local"
    r = HybridRetriever(get_embedder(provider), ARTICLES)
    m = evaluate(r, QUERIES, k=5)
    print(f"\n[{provider}] {m}")
    assert m["recall_at_5"] >= 0.8, m
    # exact-code query must land the right doc at rank 1
    assert r.search("what is error E-5501", k=1)[0] == 11
