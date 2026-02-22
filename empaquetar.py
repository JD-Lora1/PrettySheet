import os
import json

def build():
    # 1. Crear el diccionario de archivos
    files_dict = {}

    # Leer app.py principal
    with open("app.py", "r", encoding="utf-8") as f:
        files_dict["app.py"] = f.read()
        
    # Leer archivos de la carpeta core
    core_path = "core"
    if os.path.exists(core_path):
        for file in os.listdir(core_path):
            if file.endswith(".py"):
                with open(os.path.join(core_path, file), "r", encoding="utf-8") as f:
                    # Guardamos la ruta relativa como clave
                    files_dict[f"core/{file}"] = f.read()

    # 2. Convertir TODO el diccionario a un string JSON válido para JS
    # Esto escapa automáticamente comillas, saltos de línea y llaves {}
    files_json_content = json.dumps(files_dict)
    
    # 3. Generar el HTML
    # Nota: Insertamos files_json_content directamente, sin comillas extras
    html_template = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>PrettySheet</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.75.0/build/stlite.css" />
    <style>
        /* Opcional: Ocultar el menú de Streamlit para que parezca una app nativa */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.75.0/build/stlite.js"></script>
    <script>
      stlite.mount({{
        requirements: ["pandas", "openpyxl"],
        files: {files_json_content},
        entrypoint: "app.py",
      }}, document.getElementById("root"));
    </script>
  </body>
</html>
"""

    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print("¡LOGRADO! Index.html generado con escape de caracteres seguro.")

if __name__ == "__main__":
    build()