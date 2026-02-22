# 🎨 PrettySheet

**Local-First Excel Stylizer & Processor** *Tus datos, tus reglas. Sin servidores, sin fugas de privacidad.*

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Deploy PrettySheet](https://github.com/JD-Lora1/PrettySheet/actions/workflows/deploy.yml/badge.svg)](https://github.com/TU_USUARIO/PrettySheet/actions)

## Overview
**PrettySheet** es una herramienta web diseñada para transformar archivos Excel aburridos en reportes profesionales en segundos. Utiliza tecnología **WASM (WebAssembly)** para ejecutar Python directamente en tu navegador gracias a `stlite`.

> **Privacidad Total:** Al ser una app "Local-First", tus archivos nunca se suben a ningún servidor. El procesamiento ocurre enteramente en la memoria de tu navegador.

## Features
- **Procesamiento Local:** Carga y procesa archivos `.xlsx` de forma privada.
- **Smart Reordering:** Reorganiza columnas visualmente con drag-and-drop.
- **Styling Engine:** Aplica colores de encabezado, bordes y zebra-striping.
- **Auto-Width:** Ajuste automático de ancho de columnas basado en el contenido.
- **Resource Monitor:** Visualiza el consumo de memoria del proceso.

---

##  How to Run Locally

### Modo Desarrollo (Streamlit Nativo)
Ideal para modificar el código y ver cambios en tiempo real.
```powershell
# Instalar dependencias
pip install streamlit pandas openpyxl streamlit-sortables

# Ejecutar
streamlit run app.py
```

### Modo Producción (Empaquetado WASM)

Para probar la versión que verán los usuarios en la web.
```powershell
# 1. Generar el index.html
python empaquetar.py

# 2. Servir la carpeta dist
python -m http.server 3000 --directory dist
```
o
```powershell
npx serve dist
```

Abre el navegador en
http://localhost:3000

### CI/CD Pipeline

Este proyecto utiliza GitHub Actions para automatizar el despliegue:

    Al hacer push a main, un robot inicia un entorno Python.

    Ejecuta empaquetar.py para inyectar el código en un único HTML.

    Despliega automáticamente el resultado en la rama gh-pages.

### Tech Stack
- UI: Streamlit
- Engine: stlite
- Data: Pandas & Openpyxl

📄 License

Este proyecto está bajo la Apache License 2.0. Consulta el archivo LICENSE para más detalles.

Hecho con ❤️ por [JuanDi](https://github.com/JD-Lora1)
