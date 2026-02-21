import pandas as pd
from io import BytesIO

class ColumnReorderer:
    @staticmethod
    def reorder_columns(input_buffer: BytesIO, columns: list) -> BytesIO:
        """
        Reorders columns in the Excel file (in-memory) according to the provided list.
        Columns not in the list are appended at the end in their original order.
        Args:
            input_buffer (BytesIO): Input Excel file in memory.
            columns (list): Desired column order.
        Returns:
            BytesIO: Excel file with columns reordered.
        """
        input_buffer.seek(0)
        df = pd.read_excel(input_buffer)
        # Columns in the provided list
        ordered = [col for col in columns if col in df.columns]
        # Columns not in the provided list
        remaining = [col for col in df.columns if col not in columns]
        new_order = ordered + remaining
        df = df[new_order]
        output_buffer = BytesIO()
        df.to_excel(output_buffer, index=False)
        output_buffer.seek(0)
        return output_buffer
