import streamlit as st
from io import BytesIO
import sys
import os

# Backend import setup
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../PrettySheet-Backend'))
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

try:
    from core.formatter_pipeline import ExcelPipeline
except ImportError:
    st.error("No se pudo importar ExcelPipeline. Verifica la estructura del proyecto y dependencias.")
    ExcelPipeline = None

st.set_page_config(page_title="PrettySheet", layout="wide")

# Sidebar: Configuración y métricas
with st.sidebar:
    st.header("Configuración")
    apply_styles = st.checkbox("Aplicar Estilos", value=True)
    adjust_widths = st.checkbox("Ajustar Anchos", value=True)
    reorder_cols = st.checkbox("Reordenar Columnas", value=True)
    col_order_input = st.text_area("Orden de columnas (separadas por coma)", placeholder="col1, col2, col3")
    st.divider()
    st.header("Métricas de Sistema")
    try:
        import psutil
        mem = psutil.virtual_memory()
        st.write(f"RAM usada: {mem.used / 1024**2:.2f} MB / {mem.total / 1024**2:.2f} MB")
    except Exception:
        st.write("Métricas de memoria no disponibles en este entorno.")

st.title("PrettySheet: Procesador Local de Excel")
st.caption("Procesa y descarga archivos Excel de forma local, sin enviar datos a servidores.")

uploaded_file = st.file_uploader("Arrastra tu archivo Excel (.xlsx)", type="xlsx")

if uploaded_file and ExcelPipeline:
    with st.spinner("Procesando archivo..."):
        file_bytes = BytesIO(uploaded_file.read())
        # Configuración dinámica
        column_order = [c.strip() for c in col_order_input.split(",") if c.strip()] if col_order_input.strip() else None
        # Instanciar pipeline
        pipeline = ExcelPipeline(column_order=column_order)
        # Procesar archivo
        result_buffer = pipeline.process(file_bytes)
        # Preview
        import pandas as pd
        result_buffer.seek(0)
        df_preview = pd.read_excel(result_buffer)
        st.subheader("Vista previa (primeras 5 filas):")
        st.dataframe(df_preview.head(5), use_container_width=True)
        # Descargar
        result_buffer.seek(0)
        st.download_button(
            "Descargar archivo procesado",
            result_buffer.getvalue(),
            file_name="PrettySheet.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Carga un archivo Excel para comenzar.")
