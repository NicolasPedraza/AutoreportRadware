# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 18:21:15 2025

@author: NicolasP1206
"""

import json
import os

def generate_json_file(data, output_directory, filename="output.json"):
    """
    Exporta un diccionario JSON a la ruta especificada.
    
    :param data: Diccionario a exportar.
    :param output_directory: Directorio donde se guardará el archivo.
    :param filename: Nombre del archivo (por defecto "output.json").
    """
    os.makedirs(output_directory, exist_ok=True)  # Crea el directorio si no existe
    
    file_path = os.path.join(output_directory, filename)
    
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    print(f"\nFile generated in: {file_path}\n")


