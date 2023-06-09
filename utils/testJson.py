import os
import json

data = {
    "nombre": "John",
    "edad": 30,
    "ciudad": "Nueva York"
}

# Obtén la ruta base de tu proyecto
base_path = os.getcwd()  # Esto obtiene el directorio actual como la ruta base

# Obtén la ruta del directorio actual (carpeta que contiene el archivo .py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta completa del directorio donde se guardará el archivo JSON
folder_path = os.path.join(current_dir, "data")

# Verifica si el directorio no existe y crea la carpeta si es necesario
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Construye la ruta completa del archivo JSON dentro de la carpeta
file_path = os.path.join(folder_path, "nombre_sarchivo.json")

# Abre el archivo en modo escritura y escribe el objeto JSON
with open(file_path, "w") as json_file:
    json.dump(data, json_file)

print("Archivo JSON creado con éxito en:", file_path)
