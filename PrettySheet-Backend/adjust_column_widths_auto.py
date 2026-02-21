#!/usr/bin/env python3
"""
adjust_column_widths_auto.py

Auto-adjust Excel column widths to fit the longest cell in each column.

Usage:
  python adjust_column_widths_auto.py archivo.xlsx
  python adjust_column_widths_auto.py archivo.xlsx --sheet Hoja1 --min-width 8 --max-width 60 --padding 2 --out salida.xlsx
"""

import argparse
from openpyxl import load_workbook


def auto_adjust_widths(file_name, sheet=None, min_width=8, max_width=60, padding=2, out_file=None):
    wb = load_workbook(file_name)
    ws = wb[sheet] if sheet else wb.active

    for col in ws.columns:
        max_length = 0
        try:
            column = col[0].column_letter
        except Exception:
            continue
        for cell in col:
            try:
                v = cell.value
                if v is None:
                    continue
                l = len(str(v))
                if l > max_length:
                    max_length = l
            except Exception:
                pass

        adjusted_width = max(min_width, min(max_length + padding, max_width))
        ws.column_dimensions[column].width = adjusted_width

    target = out_file if out_file else file_name
    wb.save(target)
    return target


def main():
    parser = argparse.ArgumentParser(description="Auto-adjust Excel column widths to fit longest cell")
    parser.add_argument("file", help="Path to the Excel file (.xlsx)")
    parser.add_argument("--sheet", help="Sheet name (default: active)")
    parser.add_argument("--min-width", type=int, default=8, help="Minimum column width (chars)")
    parser.add_argument("--max-width", type=int, default=60, help="Maximum column width (chars)")
    parser.add_argument("--padding", type=int, default=2, help="Extra chars to add to measured length")
    parser.add_argument("--out", help="Output file (if omitted, overwrites input)")

    args = parser.parse_args()
    out = auto_adjust_widths(
        args.file,
        sheet=args.sheet,
        min_width=args.min_width,
        max_width=args.max_width,
        padding=args.padding,
        out_file=args.out,
    )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
