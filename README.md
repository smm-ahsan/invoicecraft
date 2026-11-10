# InvoiceCraft

A tiny, dependency-free command line tool that turns a few command line
arguments into a clean, printable HTML invoice.

Describe who the invoice is from, who it is for, and what you are charging
for - InvoiceCraft works out the subtotal, tax and total, and writes a tidy
HTML invoice you can open in any browser, print, or save as a PDF.

## Why

Freelancers and small agencies send invoices every week, but most invoicing
software is either a paid subscription, an account you have to log into, or
a spreadsheet that breaks when you touch it. InvoiceCraft covers the common
case in one command: no account, no subscription, no dependencies, and the
invoice file is yours to keep.

## Features

- Zero dependencies - pure Python 3 standard library
- Multiple invoice lines with quantity and unit price
- Optional tax rate in percent, applied to the subtotal
- Currency choice: EUR, USD, GBP, PKR, INR, or any code
- Invoice number and date fields (date defaults to today)
- Clean, print-friendly HTML output with a simple table and totals
- Clear error and exit code 2 when an item is malformed

## Install

No installation and nothing to pip install. Clone the repo and run it with
Python 3:

```bash
git clone https://github.com/smm-ahsan/invoicecraft.git
cd invoicecraft
python3 invoicecraft.py --help
```

## Usage

One service, no tax:

```bash
python3 invoicecraft.py --from-name "SMM Ahsan" --to "Cafe Example" \
    --item "Reels package:1:190"
```

Several lines, 18 percent tax, custom invoice number and output file:

```bash
python3 invoicecraft.py --from-name "SMM Ahsan" \
    --from-detail "info@smmahsan.com" \
    --to "Cafe Example" \
    --item "Reels package:1:190" --item "Extra post:2:25" \
    --tax 18 --number INV-2026-014 --out example-invoice.html
```

Each `--item` takes the form `description:qty:unit_price` and can be
repeated as many times as you need. See [examples.md](examples.md) for a
real run with its actual output.

Then open the generated HTML file in a browser and print it, or use the
browser's "Save as PDF" to send it to your client.

## Roadmap

- Discount line (percent or fixed amount)
- Due date and payment terms footer
- Read invoice lines from a CSV or JSON file
- Direct PDF output without a browser

## Contributing

Issues and pull requests are welcome. If you are a freelancer and a feature
is missing for the way you actually bill clients, open an issue and describe
your workflow.

## License

MIT - see [LICENSE](LICENSE).
