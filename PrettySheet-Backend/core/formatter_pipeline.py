from io import BytesIO
from core.column_reorderer import ColumnReorderer
from core.stylizer import Stylizer
from core.width_adjuster import WidthAdjuster
import psutil
import logging

logging.basicConfig(level=logging.INFO)

class ExcelPipeline:
    def __init__(self, column_order=None, min_width=8, max_width=40):
        self.column_order = column_order
        self.min_width = min_width
        self.max_width = max_width

    def log_memory(self, step_name):
        process = psutil.Process()
        mem = process.memory_info().rss / (1024 * 1024)
        logging.info(f"[MEMORY] Step: {step_name} - Memory Usage: {mem:.2f} MB")

    def process(self, input_buffer: BytesIO) -> BytesIO:
        buf = input_buffer
        if self.column_order:
            buf = ColumnReorderer.reorder_columns(buf, self.column_order)
            self.log_memory('ColumnReorderer')
        buf = Stylizer.style_excel(buf)
        self.log_memory('Stylizer')
        buf = WidthAdjuster.adjust_widths(buf, self.min_width, self.max_width)
        self.log_memory('WidthAdjuster')
        return buf
