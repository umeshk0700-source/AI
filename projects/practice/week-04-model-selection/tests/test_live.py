import os
import pytest
from llmlab import get_client, settings
from bench.bench import ModelBench

pytestmark = pytest.mark.live
_LIVE = os.getenv("LLM_LIVE") == "1"

INVOICES = [
  ("Northwind Traders\nInvoice No: NW-2024-0417\nBill to: Cirrus Inc\n"
   "2 x Widget @ $50.00\n1 x Setup fee @ $120.00\nSubtotal: $220.00\nTax: $0.00\n"
   "Total due: $220.00 USD\nPayment due: 2024-06-15",
   {"vendor": "Northwind Traders", "invoice_number": "NW-2024-0417", "total": 220.0,
    "currency": "USD", "due_date": "2024-06-15", "line_item_count": 3}),
  ("FACTURE\nSociete Lumiere SARL\nNo FR-8891\nConseil (1 poste) : 900,00 EUR\n"
   "Total: 900,00 EUR\nEcheance: aucune",
   {"vendor": "Societe Lumiere SARL", "invoice_number": "FR-8891", "total": 900.0,
    "currency": "EUR", "due_date": "", "line_item_count": 1}),
  ("Acme Cloud Services  |  Invoice #AC-55231\nUsage - compute: $412.09\n"
   "Usage - storage: $33.10\nSupport plan: $99.00\nAmount due: $544.19 (USD)\nDue by 2024-07-01",
   {"vendor": "Acme Cloud Services", "invoice_number": "AC-55231", "total": 544.19,
    "currency": "USD", "due_date": "2024-07-01", "line_item_count": 3}),
  ("INVOICE\nBluePeak Design Studio\nRef: BP1099\nBranding package .......... GBP 3,500.00\n"
   "Total GBP 3,500.00\nNet 30 - due 2024-05-20",
   {"vendor": "BluePeak Design Studio", "invoice_number": "BP1099", "total": 3500.0,
    "currency": "GBP", "due_date": "2024-05-20", "line_item_count": 1}),
]


@pytest.mark.skipif(not _LIVE, reason="live")
def test_selection_memo_from_real_models():
    lineup = {}
    if settings.has("anthropic"):
        lineup["claude-haiku-4-5"] = get_client("anthropic", model="claude-haiku-4-5")
    if settings.has("openai"):
        lineup["gpt-4o-mini"] = get_client("openai", model="gpt-4o-mini")
    if not lineup:
        pytest.skip("no provider keys")
    bench = ModelBench([{"text": t, "fields": f} for t, f in INVOICES])
    results = bench.run(lineup)
    memo = bench.select(results, min_accuracy=0.85)
    print("\n" + "\n".join(f"  {r}" for r in memo.table))
    print("  recommend:", memo.recommended, "| rationale:", memo.rationale)
    assert memo.recommended in lineup
    assert all(r.field_accuracy > 0 for r in results), "extraction produced nothing"
    assert sum(r.cost_usd for r in results) < 0.10
