import os
import base64

def build():
    # 1. Leer archivos principales
    with open("app.py", "r", encoding="utf-8") as f:
        app_code = f.read()
    
    # 2. Leer archivos de la carpeta core
    # Vamos a crear un diccionario para stlite
    files_dict = {
        "app.py": app_code
    }
    
    core_path = "core"
    for file in os.listdir(core_path):
        if file.endswith(".py"):
            with open(os.path.join(core_path, file), "r", encoding="utf-8") as f:
                files_dict[f"core/{file}"] = f.read()

    # 3. Generar el HTML
    # Usamos triple llave para las llaves de JS
    files_js = ",\n".join([f'"{name}": `{content}`' for name, content in files_dict.items()])
    
    html_template = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>PrettySheet 🎨</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.75.0/build/stlite.css" />
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.75.0/build/stlite.js"></script>
    <script>
      stlite.mount({{
        requirements: ["pandas", "openpyxl", "streamlit-sortables"],
        files: {{
          {files_js}
        }},
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
    
    print("✨ ¡LOGRADO! Archivo dist/index.html generado manualmente sin errores de wheel.")

if __name__ == "__main__":
    build()