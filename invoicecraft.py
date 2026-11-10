#!/usr/bin/env python3
"""InvoiceCraft - generate a clean HTML invoice from the command line.

A tiny, dependency-free tool for freelancers and small agencies.
Describe the invoice on the command line and get a tidy, printable
HTML invoice with subtotal, tax and total worked out for you.

Usage:
    python3 invoicecraft.py --from-name "SMM Ahsan" --to "Cafe Example" \
        --item "Reels package:1:190" --item "Extra post:2:25" --tax 18
"""

import argparse
import datetime
import html
import sys

CURRENCY_SYMBOLS = {
    "EUR": "€",
    "USD": "$",
    "GBP": "£",
    "PKR": "Rs ",
    "INR": "Rs ",
}


def money(currency, amount):
    symbol = CURRENCY_SYMBOLS.get(currency.upper(), currency.upper() + " ")
    return "{}{:,.2f}".format(symbol, amount)


def parse_item(raw, parser):
    """Parse one --item value of the form 'description:qty:unit_price'."""
    parts = raw.rsplit(":", 2)
    if len(parts) != 3 or not parts[0].strip():
        parser.error(
            "bad --item format: {!r} (expected 'description:qty:unit_price')".format(raw)
        )
    description = parts[0].strip()
    try:
        qty = float(parts[1])
        unit_price = float(parts[2])
    except ValueError:
        parser.error(
            "bad --item format: {!r} (qty and unit_price must be numbers)".format(raw)
        )
    if qty <= 0:
        parser.error("bad --item format: {!r} (qty must be above 0)".format(raw))
    if unit_price < 0:
        parser.error("bad --item format: {!r} (unit_price cannot be negative)".format(raw))
    return description, qty, unit_price


def format_qty(qty):
    if qty == int(qty):
        return str(int(qty))
    return "{:g}".format(qty)


def build_invoice_html(args, items, subtotal, tax_amount, total):
    rows = []
    for description, qty, unit_price in items:
        line_total = qty * unit_price
        rows.append(
            "      <tr><td>{}</td><td class='num'>{}</td>"
            "<td class='num'>{}</td><td class='num'>{}</td></tr>".format(
                html.escape(description),
                format_qty(qty),
                money(args.currency, unit_price),
                money(args.currency, line_total),
            )
        )
    items_rows = "\n".join(rows)

    from_detail = ""
    if args.from_detail:
        from_detail = "<p>{}</p>".format(html.escape(args.from_detail))

    tax_row = ""
    if args.tax:
        tax_row = (
            "      <tr><td colspan='3'>Tax ({}%)</td>"
            "<td class='num'>{}</td></tr>\n".format(
                "{:g}".format(args.tax), money(args.currency, tax_amount)
            )
        )

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Invoice {number}</title>
<style>
  body {{ font-family: Arial, Helvetica, sans-serif; margin: 40px; color: #222; }}
  h1 {{ margin-bottom: 0; }}
  .meta {{ color: #555; margin-top: 4px; }}
  .parties {{ display: flex; gap: 60px; margin: 30px 0; }}
  .parties h3 {{ margin-bottom: 4px; }}
  .parties p {{ margin: 0; color: #333; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ border-bottom: 1px solid #ddd; padding: 8px; text-align: left; }}
  th {{ background: #f5f5f5; }}
  .num {{ text-align: right; }}
  .totals {{ width: 320px; margin-left: auto; margin-top: 20px; }}
  .totals td {{ border-bottom: none; }}
  .grand td {{ font-weight: bold; border-top: 2px solid #222; font-size: 1.1em; }}
  footer {{ margin-top: 50px; color: #777; font-size: 0.85em; }}
</style>
</head>
<body>
  <h1>Invoice {number}</h1>
  <p class="meta">Date: {date}</p>

  <div class="parties">
    <div>
      <h3>From</h3>
      <p><strong>{from_name}</strong></p>
      {from_detail}
    </div>
    <div>
      <h3>Billed to</h3>
      <p><strong>{to_name}</strong></p>
    </div>
  </div>

  <table>
    <thead>
      <tr><th>Description</th><th class="num">Qty</th><th class="num">Unit price</th><th class="num">Amount</th></tr>
    </thead>
    <tbody>
{items_rows}
    </tbody>
  </table>

  <table class="totals">
    <tbody>
      <tr><td colspan="3">Subtotal</td><td class="num">{subtotal}</td></tr>
{tax_row}      <tr class="grand"><td colspan="3">Total</td><td class="num">{total}</td></tr>
    </tbody>
  </table>

  <footer>Generated with InvoiceCraft</footer>
</body>
</html>
""".format(
        number=html.escape(args.number),
        date=html.escape(args.date),
        from_name=html.escape(args.from_name),
        from_detail=from_detail,
        to_name=html.escape(args.to),
        items_rows=items_rows,
        subtotal=money(args.currency, subtotal),
        tax_row=tax_row,
        total=money(args.currency, total),
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a clean HTML invoice from the command line."
    )
    parser.add_argument("--from-name", required=True,
                        help="Your name or business name (the sender)")
    parser.add_argument("--from-detail", default="",
                        help="Optional extra sender line, e.g. address or email")
    parser.add_argument("--to", required=True,
                        help="Client name the invoice is billed to")
    parser.add_argument("--item", action="append", required=True,
                        metavar="'DESC:QTY:PRICE'",
                        help="One invoice line as 'description:qty:unit_price'. "
                             "Repeat for multiple lines.")
    parser.add_argument("--currency", default="EUR",
                        help="Currency code, e.g. EUR, USD, GBP (default: EUR)")
    parser.add_argument("--tax", type=float, default=0,
                        help="Tax rate in percent, e.g. 18 (default: 0)")
    parser.add_argument("--number", default="INV-001",
                        help="Invoice number (default: INV-001)")
    parser.add_argument("--date", default=datetime.date.today().isoformat(),
                        help="Invoice date, e.g. 2026-11-10 (default: today)")
    parser.add_argument("--out", default="invoice.html",
                        help="Output HTML file (default: invoice.html)")
    args = parser.parse_args(argv)

    items = [parse_item(raw, parser) for raw in args.item]

    subtotal = sum(qty * unit_price for _, qty, unit_price in items)
    tax_amount = subtotal * args.tax / 100.0
    total = subtotal + tax_amount

    document = build_invoice_html(args, items, subtotal, tax_amount, total)
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(document)

    print("Invoice {} written to {}".format(args.number, args.out))
    print("Total: {}".format(money(args.currency, total)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
