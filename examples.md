# Examples

A real run of InvoiceCraft, captured from an actual test.

## Command

```bash
python3 invoicecraft.py --from-name "SMM Ahsan" --to "Cafe Example" --item "Reels package:1:190" --item "Extra post:2:25" --tax 18 --out example-invoice.html
```

## Output

```
Invoice INV-001 written to example-invoice.html
Total: €283.20
```

The maths behind that total: the two items come to a subtotal of €240.00
(€190.00 + 2 x €25.00), 18 percent tax adds €43.20, giving a total of
€283.20.

## Generated file

The run generated an HTML invoice file named **example-invoice.html** in the
current folder - a tidy invoice for "Cafe Example" from "SMM Ahsan" with the
two item rows, subtotal, tax and total in a simple table. Open it in any
browser to view or print it.
