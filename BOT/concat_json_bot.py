# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 17:15:00 2026

@author: NicolasP1206
"""

import json

def concat_json_bot(json1, json2):
    # Manejo de JSON vacío (Basado en Código 1)
    if not json1:
        return json2
    if not json2:
        return json1

    # Convertir a dict si la entrada es un string (Mantenemos flexibilidad)
    data1 = json.loads(json1) if isinstance(json1, str) else json1
    data2 = json.loads(json2) if isinstance(json2, str) else json2

    # Concatenar la data (Basado en la lógica de 'data' del Código 1)
    # Se asume que 'results' es la lista principal de elementos
    new_results = data1.get("results", []) + data2.get("results", [])

    # Recalcular total_count basado en la suma de los conteos originales
    # similar a la lógica de 'totalHits' del Código 1
    total_count_1 = int(data1.get("total_count", 0))
    total_count_2 = int(data2.get("total_count", 0))
    new_total_count = total_count_1 + total_count_2

    # Construir el nuevo JSON (Siguiendo la estructura del Código 2)
    new_json = {
        "results": new_results,
        "total_count": new_total_count,
        "page": 1,
        "next": "",
        "previous": ""
    }

    return new_json
