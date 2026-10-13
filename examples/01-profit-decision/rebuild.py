"""Rebuild the illustrative profit decision from the supplied public CSVs.

Python 3.9+, standard library only. Run from any directory: python rebuild.py
No private fixture, external service, or installed skill is required.
"""
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"


def read(name):
    with (INPUTS / name).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def unique(rows, field):
    index = {row[field]: row for row in rows}
    if len(index) != len(rows) or "" in index:
        raise ValueError(f"{field} must be unique and nonblank")
    return index


lines = read("invoice_lines.csv")
credits = read("credit_lines.csv")
charges = read("carrier_charges.csv")
finance = read("monthly_finance.csv")
by_line = unique(lines, "line_id")
unique(credits, "credit_line_id")
unique(charges, "shipment_charge_id")
unique(finance, "accounting_month")
invoice_segments = {}
for row in lines:
    old = invoice_segments.setdefault(row["invoice_id"], row["customer_segment"])
    assert old == row["customer_segment"]
for row in credits:
    assert row["original_line_id"] in by_line
    assert by_line[row["original_line_id"]]["invoice_id"] == row["original_invoice_id"]
for row in charges:
    assert row["invoice_id"] in invoice_segments

monthly = []
for ledger in sorted(finance, key=lambda r: r["accounting_month"]):
    assert ledger["close_status"] == "CLOSED"
    month = ledger["accounting_month"]
    booked = [r for r in lines if r["posted_date"][:7] == month]
    adjustments = [r for r in credits if r["posted_date"][:7] == month]
    sales = sum(int(r["net_revenue_vnd"]) for r in booked) - sum(int(r["revenue_reduction_vnd"]) for r in adjustments)
    cogs = sum(int(r["cogs_vnd"]) for r in booked) - sum(int(r["cogs_reversal_vnd"]) for r in adjustments)
    assert sales == int(ledger["net_sales_vnd"])
    assert cogs == int(ledger["net_cogs_vnd"])
    freight = int(ledger["outbound_freight_vnd"])
    exported = sum(int(r["charge_vnd"]) for r in charges if r["expense_month"] == month)
    contribution = sales - cogs - freight
    monthly.append({"month": month, "net_sales_vnd": sales, "net_cogs_vnd": cogs,
                    "gross_profit_vnd": sales - cogs, "outbound_freight_vnd": freight,
                    "contribution_vnd": contribution,
                    "contribution_margin_pct": str(Decimal(contribution) / Decimal(sales) * 100),
                    "connected_freight_vnd": exported, "unattributed_freight_vnd": freight - exported})

sku_totals = defaultdict(lambda: {"q": 0, "r": 0, "c": 0})
for row in lines:
    bucket = sku_totals[row["posted_date"][:7], row["customer_segment"], row["sku"]]
    for key, field in (("q", "quantity"), ("r", "net_revenue_vnd"), ("c", "cogs_vnd")):
        bucket[key] += int(row[field])
unit_prices = {}
volume = price = unit_cost = 0
for segment, product in sorted({(r["customer_segment"], r["sku"]) for r in lines}):
    first, last = sku_totals["2026-06", segment, product], sku_totals["2026-07", segment, product]
    assert first["r"] % first["q"] == last["r"] % last["q"] == 0
    assert first["c"] % first["q"] == last["c"] % last["q"] == 0
    p0, p1 = first["r"] // first["q"], last["r"] // last["q"]
    c0, c1 = first["c"] // first["q"], last["c"] // last["q"]
    unit_prices[segment, product] = {"june": p0, "july": p1}
    volume += (last["q"] - first["q"]) * (p0 - c0)
    price += last["q"] * (p1 - p0)
    unit_cost -= last["q"] * (c1 - c0)
credit_gp = {month: sum(int(r["cogs_reversal_vnd"]) - int(r["revenue_reduction_vnd"])
                       for r in credits if r["posted_date"][:7] == month)
             for month in ("2026-06", "2026-07")}
bridge = {"volume_mix_at_june_unit_margin_vnd": volume,
          "invoice_price_at_july_quantities_vnd": price,
          "unit_cost_at_july_quantities_vnd": unit_cost,
          "change_in_posted_credit_effect_vnd": credit_gp["2026-07"] - credit_gp["2026-06"],
          "change_in_freight_effect_vnd": monthly[0]["outbound_freight_vnd"] - monthly[1]["outbound_freight_vnd"]}
assert sum(bridge.values()) == monthly[1]["contribution_vnd"] - monthly[0]["contribution_vnd"]

july_b2b_lines = [r for r in lines if r["posted_date"][:7] == "2026-07" and r["customer_segment"] == "B2B"]
july_b2b_credits = [r for r in credits if r["posted_date"][:7] == "2026-07"
                   and by_line[r["original_line_id"]]["customer_segment"] == "B2B"]
b2b_gp = (sum(int(r["net_revenue_vnd"]) - int(r["cogs_vnd"]) for r in july_b2b_lines)
          + sum(int(r["cogs_reversal_vnd"]) - int(r["revenue_reduction_vnd"]) for r in july_b2b_credits))
b2b_connected = sum(int(r["charge_vnd"]) for r in charges
                    if r["expense_month"] == "2026-07" and invoice_segments[r["invoice_id"]] == "B2B")
b2b_floor = b2b_gp - b2b_connected - monthly[1]["unattributed_freight_vnd"]

# Sensitivity, not a demand forecast: restore June B2B prices on July invoice
# quantities and revalue returns from those same invoices at restored prices.
# Keep return quantities, approved service allowances, COGS and freight fixed.
gross_price_sensitivity = sum(int(r["quantity"]) *
                              (unit_prices["B2B", r["sku"]]["june"] - unit_prices["B2B", r["sku"]]["july"])
                              for r in july_b2b_lines)
extra_return_credit = 0
for row in july_b2b_credits:
    original = by_line[row["original_line_id"]]
    if row["reason_code"] == "RETURN_RESELLABLE" and original["posted_date"][:7] == "2026-07":
        extra_return_credit += int(row["returned_quantity"]) * (
            unit_prices["B2B", original["sku"]]["june"] - unit_prices["B2B", original["sku"]]["july"])
price_sensitivity = gross_price_sensitivity - extra_return_credit
cross_period = [r for r in credits if r["posted_date"][:7] != by_line[r["original_line_id"]]["posted_date"][:7]]

result = {
    "disclosure": "Synthetic instructional fixture; verified arithmetic, no observed business result or causal price estimate.",
    "unit": "VND; integer amounts excluding VAT",
    "definition": "Contribution = net sales - net COGS - all recognized outbound freight; excludes overhead.",
    "monthly": monthly, "bridge": bridge,
    "b2b_july": {"gross_profit_vnd": b2b_gp, "connected_freight_vnd": b2b_connected,
                 "contribution_before_unattributed_freight_vnd": b2b_gp - b2b_connected,
                 "contribution_floor_if_all_missing_freight_is_b2b_vnd": b2b_floor},
    "full_price_restoration_sensitivity": {"invoice_quantity_effect_vnd": gross_price_sensitivity,
                                          "extra_return_credit_vnd": extra_return_credit,
                                          "net_contribution_effect_vnd": price_sensitivity,
                                          "assumptions": "Same July sales and return quantities, COGS, freight and service allowances. June B2B invoice prices restored only on July invoices; no demand response."},
    "cross_period_credit_lines": len(cross_period),
    "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(INPUTS.iterdir()) if p.is_file()},
}
assert [m["contribution_vnd"] for m in monthly] == [35000000, 30950000]
assert b2b_floor == 17700000
assert price_sensitivity == 6200000
(ROOT / "analysis.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

facts = []
for m in monthly:
    for field in ("net_sales_vnd", "gross_profit_vnd", "outbound_freight_vnd", "contribution_vnd", "unattributed_freight_vnd"):
        facts.append({"period": m["month"], "metric": field, "value": m[field], "unit": "VND",
                      "basis": "closed ledger, reconciled to invoice/credit rows; connector coverage checked separately"})
for metric, value in bridge.items():
    facts.append({"period": "June to July 2026", "metric": metric, "value": value, "unit": "VND",
                  "basis": "sequential bridge from invoices, credit posting month and full freight ledger"})
facts.extend([
    {"period": "2026-07", "metric": "b2b_contribution_floor", "value": b2b_floor, "unit": "VND", "basis": "B2B GP - connected B2B freight - all unallocated company freight"},
    {"period": "July quantities", "metric": "full_price_restoration_sensitivity", "value": price_sensitivity, "unit": "VND", "basis": "June B2B prices; fixed July sales/return quantities, COGS, freight, allowances; not forecast"},
])
with (ROOT / "evidence.csv").open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=("period", "metric", "value", "unit", "basis"))
    writer.writeheader()
    writer.writerows(facts)
print(json.dumps({"status": "passed", "inputs": len(result["input_sha256"]),
                  "invoice_lines": len(lines), "credit_lines": len(credits), "carrier_charges": len(charges),
                  "contribution_change_vnd": sum(bridge.values()), "b2b_floor_vnd": b2b_floor,
                  "price_sensitivity_vnd": price_sensitivity}))
