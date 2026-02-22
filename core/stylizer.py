from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
from io import BytesIO

class Stylizer:
    @staticmethod
    def style_excel(input_buffer, column_configs, font_color_unused=None):
        import openpyxl
        wb = openpyxl.load_workbook(input_buffer)
        ws = wb.active
        
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                            top=Side(style='thin'), bottom=Side(style='thin'))

        for cell in ws[1]:
            col_name = str(cell.value).strip()
            
            if col_name in column_configs:
                # Extraemos ambos colores específicos de la columna
                bg = column_configs[col_name]["bg_color"]
                txt = column_configs[col_name]["txt_color"]
                
                cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
                cell.font = Font(color=txt, bold=True, size=12)
            
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Cebra (opcional: puedes usar un gris muy suave para no chocar con los colores)
        zebra = PatternFill(start_color="F9F9F9", end_color="F9F9F9", fill_type="solid")
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.border = thin_border
                if cell.row % 2 == 0:
                    cell.fill = zebra

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output
