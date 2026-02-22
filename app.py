import streamlit as st
import pandas as pd
from io import BytesIO

# Importación del motor de procesamiento
try:
    from core.formatter_pipeline import ExcelPipeline 
except ImportError:
    ExcelPipeline = None

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="PrettySheet | Profesionales en Excel",
    page_icon="🎨",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuración Global")
    apply_styles = st.checkbox("Aplicar Estilos", value=True)
    adjust_widths = st.checkbox("Ajustar Anchos", value=True)
    
    st.divider()
    st.markdown("### 🎨 Colores Predeterminados")
    default_bg = st.color_picker("Fondo de cabecera base", "#1F4E78")
    default_txt = st.color_picker("Texto de cabecera base", "#FFFFFF")
    
    st.divider()
    st.info("🚀 **Local-First**: Tus datos se procesan en tu navegador y nunca viajan a un servidor.")

# --- CUERPO PRINCIPAL ---
st.title("🎨 PrettySheet")
st.caption("Ajusta el orden y los colores de cada columna de forma independiente.")

uploaded_file = st.file_uploader("Carga tu archivo Excel (.xlsx)", type="xlsx")

if uploaded_file:
    # 1. GESTIÓN DE ESTADO: Cargar datos iniciales
    if 'column_data' not in st.session_state or st.session_state.get('current_file') != uploaded_file.name:
        file_bytes = BytesIO(uploaded_file.getvalue())
        df_headers = pd.read_excel(file_bytes, nrows=0)
        
        # Inicializamos el estado con los colores base del sidebar
        st.session_state.column_data = [
            {"name": col, "bg": default_bg, "txt": default_txt} for col in df_headers.columns
        ]
        st.session_state.current_file = uploaded_file.name

    # --- PANEL DE PERSONALIZACIÓN ---
    st.subheader("🛠️ Configuración de Columnas")
    st.write("Cambia el orden con ⬆️ ⬇️ y elige colores específicos para cada encabezado.")

    # Encabezados de la tabla de configuración
    h1, h2, h3, h4 = st.columns([1, 4, 1.5, 1.5])
    with h1: st.write("**Orden**")
    with h2: st.write("**Columna (Vista Previa)**")
    with h3: st.write("**Fondo**")
    with h4: st.write("**Texto**")
    st.divider()

    # 2. RENDERIZADO DE FILAS DINÁMICAS
    for i, col_info in enumerate(st.session_state.column_data):
        with st.container():
            c1, c2, c3, c4 = st.columns([1, 4, 1.5, 1.5])
            
            with c1:
                # Controles de movimiento
                up = st.button("⬆️", key=f"up_{i}", disabled=(i == 0))
                down = st.button("⬇️", key=f"down_{i}", disabled=(i == len(st.session_state.column_data)-1))
                
                if up:
                    st.session_state.column_data[i], st.session_state.column_data[i-1] = \
                        st.session_state.column_data[i-1], st.session_state.column_data[i]
                    st.rerun()
                if down:
                    st.session_state.column_data[i], st.session_state.column_data[i+1] = \
                        st.session_state.column_data[i+1], st.session_state.column_data[i]
                    st.rerun()

            with c2:
                # Vista previa alineada
                st.markdown(f"""
                    <div style="
                        background-color: {col_info['bg']}; 
                        color: {col_info['txt']}; 
                        padding: 10px; 
                        border-radius: 6px; 
                        text-align: center;
                        font-weight: bold;
                        border: 1px solid #ddd;
                        font-family: sans-serif;
                        font-size: 14px;
                    ">
                        {col_info['name']}
                    </div>
                """, unsafe_allow_html=True)
            
            with c3:
                # Selector de fondo (sin texto de etiqueta para mayor limpieza)
                col_info['bg'] = st.color_picker(
                    f"BG_{i}", col_info['bg'], key=f"picker_bg_{i}", label_visibility="collapsed"
                )
            
            with c4:
                # Selector de fuente
                col_info['txt'] = st.color_picker(
                    f"TXT_{i}", col_info['txt'], key=f"picker_txt_{i}", label_visibility="collapsed"
                )
        st.write("") # Espaciado entre filas

    # --- ACCIÓN FINAL ---
    st.divider()
    
    if ExcelPipeline:
        if st.button("🚀 Procesar y Generar Excel", type="primary", use_container_width=True):
            with st.spinner("Generando formato profesional..."):
                file_bytes = BytesIO(uploaded_file.getvalue())
                
                # Preparar datos para el Pipeline
                final_order = [c['name'] for c in st.session_state.column_data]
                final_configs = {
                    c['name']: {
                        "bg_color": c['bg'].replace("#", ""),
                        "txt_color": c['txt'].replace("#", "")
                    } for c in st.session_state.column_data
                }

                pipeline = ExcelPipeline(
                    column_order=final_order,
                    column_configs=final_configs
                )
                
                result_buffer = pipeline.process(file_bytes)
                result_buffer.seek(0)
                
                # Mostrar éxito y descarga
                st.success("¡Archivo procesado con éxito!")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    df_preview = pd.read_excel(result_buffer)
                    st.write("📊 Vista previa rápida:")
                    st.dataframe(df_preview.head(5), use_container_width=True)
                
                with col_d2:
                    st.write("💾 Guardar resultado:")
                    result_buffer.seek(0)
                    st.download_button(
                        label="📥 Descargar Excel Formateado",
                        data=result_buffer.getvalue(),
                        file_name=f"Pretty_{uploaded_file.name}",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
    else:
        st.error("⚠️ Error: No se pudo cargar el motor `ExcelPipeline`. Revisa la carpeta `core`.")

else:
    # Pantalla de bienvenida
    st.info("👋 ¡Bienvenido! Por favor, carga un archivo Excel arriba para comenzar a personalizarlo.")
    
    # Ejemplo visual de qué hace la app
    st.image("https://img.icons8.com/clouds/200/microsoft-excel.png", width=100)
    st.write("Con PrettySheet puedes:")
    st.write("- ↕️ Reordenar columnas sin tocar el Excel original.")
    st.write("- 🎨 Asignar colores corporativos a cada encabezado.")
    st.write("- 📏 Ajustar anchos de celda automáticamente.")