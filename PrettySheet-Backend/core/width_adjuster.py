from openpyxl import load_workbook
from io import BytesIO

class WidthAdjuster:
    @staticmethod
    def adjust_widths(input_buffer: BytesIO, min_width: int = 8, max_width: int = 40) -> BytesIO:
        """
        Adjusts column widths based on cell content, with min/max width constraints.
        Args:
            input_buffer (BytesIO): Input Excel file in memory.
            min_width (int): Minimum column width.
            max_width (int): Maximum column width.
        Returns:
            BytesIO: Excel file with adjusted column widths.
        """
        input_buffer.seek(0)
        wb = load_workbook(input_buffer)
        ws = wb.active
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    value = str(cell.value) if cell.value is not None else ''
                except Exception:
                    value = ''
                max_length = max(max_length, len(value))
            # Add a little extra space
            width = min(max_width, max(min_width, max_length + 2))
            ws.column_dimensions[col_letter].width = width
        output_buffer = BytesIO()
        wb.save(output_buffer)
        output_buffer.seek(0)
        wb.close()
        return output_buffer
