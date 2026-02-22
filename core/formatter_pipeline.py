from io import BytesIO
from core.column_reorderer import ColumnReorderer
from core.stylizer import Stylizer
from core.width_adjuster import WidthAdjuster
import logging

logging.basicConfig(level=logging.INFO)

class ExcelPipeline:
    def __init__(self, column_order=None, column_configs=None, font_color="FFFFFF"):
        self.column_order = column_order
        self.column_configs = column_configs or {} # Diccionario {col_name: {bg_color: ...}}
        self.font_color = font_color

    def process(self, input_buffer: BytesIO) -> BytesIO:
        buf = input_buffer
        
        # 1. Reordenar primero es vital para que el Stylizer encuentre las celdas
        if self.column_order:
            buf = ColumnReorderer.reorder_columns(buf, self.column_order)
        
        # 2. Estilizar con el diccionario de configuraciones
        buf = Stylizer.style_excel(buf, self.column_configs, self.font_color)
        
        # 3. Ajustar anchos
        buf = WidthAdjuster.adjust_widths(buf, 8, 40)
        
        return buf