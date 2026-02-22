import streamlit as st
import pandas as pd
from io import BytesIO
from streamlit_sortables import sort_items
# Importaciones directas (asumiendo que están en la misma carpeta o subcarpeta core)
from core.formatter_pipeline import ExcelPipeline 

# Configuración de página
st.set_page_config(page_title="PrettySheet", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    apply_styles = st.checkbox("Aplicar Estilos", value=True)
    adjust_widths = st.checkbox("Ajustar Anchos", value=True)
    reorder_cols = st.checkbox("Reordenar Columnas", value=True)
    
    st.divider()
    st.info("🚀 **Local-First**: Tus datos se procesan en tu navegador y nunca viajan a un servidor.")

# --- CUERPO PRINCIPAL ---
st.title("PrettySheet: Procesador Local de Excel")
st.caption("Dale un acabado profesional a tus Excels en segundos.")

uploaded_file = st.file_uploader("Arrastra tu archivo Excel (.xlsx)", type="xlsx")

st.subheader("Personalización de Estilo")
col1, col2 = st.columns(2)

with col1:
    primary_color = st.color_picker("Color de Encabezado", "#1F4E78")
with col2:
    font_color = st.color_picker("Color de Texto", "#FFFFFF")

# Previsualización rápida con Markdown/HTML
st.markdown(
    f"""
    <div style="
        background-color: {primary_color}; 
        color: {font_color}; 
        padding: 10px; 
        border-radius: 5px; 
        text-align: center;
        font-weight: bold;
        border: 1px solid #ddd;
    ">
        VISTA PREVIA DEL ENCABEZADO
    </div>
    """, 
    unsafe_allow_html=True
)

if uploaded_file and ExcelPipeline:
    # 1. PRIMERO: Leer el archivo para obtener los headers
    file_bytes = BytesIO(uploaded_file.getvalue())
    file_bytes.seek(0)
    df_headers = pd.read_excel(file_bytes, nrows=0)
    headers = list(df_headers.columns)

    # 2. SEGUNDO: Configuración de Colores (Ahora que ya tenemos 'headers')
    st.subheader("Configuración de Columnas")
    column_configs = {}

    with st.expander("🎨 Personalizar colores por columna"):
        cols_ui = st.columns(3) 
        for i, col_name in enumerate(headers):
            with cols_ui[i % 3]:
                # Usamos un color por defecto inicial
                color = st.color_picker(f"Color: {col_name}", "#1F4E78", key=f"cp_{col_name}")
                column_configs[col_name] = {"bg_color": color.lstrip('#')}

    # 3. TERCERO: Reordenar columnas
    column_order = None
    if reorder_cols:
        st.subheader("Arrastra para reordenar las columnas:")
        
        # --- TRUCO CSS PARA COLORES DINÁMICOS ---
        # Esto genera estilos CSS para cada item del sortable basado en tus color_pickers
        css_colors = ""
        for col_name, config in column_configs.items():
            bg = f"#{config['bg_color']}"
            # Usamos selectores de texto para pintar las cajas del sortable
            css_colors += f"""
            div[data-testid="stMarkdownContainer"] p:contains("{col_name}") {{
                background-color: {bg} !important;
                color: {font_color} !important;
                padding: 5px 10px;
                border-radius: 5px;
            }}
            """
        st.markdown(f"<style>{css_colors}</style>", unsafe_allow_html=True)
        
        column_order = sort_items(headers, direction="vertical", key="sortable_col_order")
    else:
        # Si no reordenan, el orden es el original de los headers
        column_order = headers

    # 4. CUARTO: Procesamiento
    if st.button("Procesar y Previsualizar"):
        with st.spinner("Procesando..."):
            file_bytes.seek(0)
            
            # LIMPIEZA CRÍTICA: Asegurar que no haya '#' en ningún color
            clean_configs = {
                col: {"bg_color": cfg["bg_color"].replace("#", "")} 
                for col, cfg in column_configs.items()
            }
            clean_font_color = font_color.replace("#", "") # <--- Esto faltaba

            pipeline = ExcelPipeline(
                column_order=column_order,
                column_configs=clean_configs,
                font_color=clean_font_color
            )
                
            result_buffer = pipeline.process(file_bytes)
            result_buffer.seek(0)
            
            # Vista previa
            df_preview = pd.read_excel(result_buffer)
            st.subheader("Vista previa (primeras 5 filas):")
            st.dataframe(df_preview.head(5), use_container_width=True)
            
            # Botón de descarga
            result_buffer.seek(0)
            st.download_button(
                label="📥 Descargar archivo con formato",
                data=result_buffer.getvalue(),
                file_name="PrettySheet_Procesado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
elif not ExcelPipeline:
    st.warning("⚠️ El motor de procesamiento (ExcelPipeline) no está cargado.")
else:
    st.info("👋 Carga un archivo Excel para comenzar.")