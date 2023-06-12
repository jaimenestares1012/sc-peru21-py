import hashlib
import re
import os
import json

def urlnoticia(base, parrafo):
    palabras = parrafo.split()
    primera_palabra = palabras[0]
    segunda_palabra = palabras[1]
    ultima_palabra = palabras[-1]
    resultado = base + '#:~:text=' + primera_palabra + '%20' + segunda_palabra + ',' + ultima_palabra
    return resultado


def hashear(urlParrafo):
    hash_md5 = hashlib.md5()
    hash_md5.update(urlParrafo.encode('utf-8'))
    return hash_md5.hexdigest()



def contiene_p_o_m(string):
    pattern = r'[pm]'
    matches = re.search(pattern, string, re.IGNORECASE)
    return matches is not None

def generaJson(data, nombre_sarchivo, fecha_scraping):

    # Obtén la ruta del directorio actual (carpeta que contiene el archivo .py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta completa del directorio donde se guardará el archivo JSON
    folder_path = os.path.join(current_dir, "data/{}".format(fecha_scraping))

    # Verifica si el directorio no existe y crea la carpeta si es necesario
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Construye la ruta completa del archivo JSON dentro de la carpeta
    file_path = os.path.join(folder_path, "{}.json".format(nombre_sarchivo))

    # Abre el archivo en modo escritura y escribe el objeto JSON
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)

    print("Archivo JSON creado con éxito en:", file_path)



# print(contiene_p_o_m("01:54 p. m."))  # True
# print(contiene_p_o_m("08:30 a. m."))  # True
# print(contiene_p_o_m("10:00 a."))    # True
# print(contiene_p_o_m("11:45"))    