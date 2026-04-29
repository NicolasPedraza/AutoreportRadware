# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 16:51:25 2025

@author: NicolasP1206
"""

def concat_json(json1, json2):
    # Manejo de JSON vacío
    if not json1:
        return json2
    if not json2:
        return json1
    
    # Convertir totalHits a enteros y sumarlos
    total_hits_1 = int(json1["metaData"]["totalHits"])
    total_hits_2 = int(json2["metaData"]["totalHits"])
    new_total_hits = total_hits_1 + total_hits_2
    
    # Concatenar la data
    new_data = json1["data"] + json2["data"]
    
    # Construir el nuevo JSON
    new_json = {
        "metaData": {
            "totalHits": str(new_total_hits)  # Convertir de nuevo a string
        },
        "data": new_data
    }
    
    return new_json