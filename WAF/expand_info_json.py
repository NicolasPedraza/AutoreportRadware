# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 21:47:34 2025

@author: NicolasP1206
"""

import json

def expand_info_json(data):
    for entry in data.get("data", []):
        row = entry.get("row", {})
        
        # Verificar si enrichmentContainer existe y es una cadena JSON válida
        if "enrichmentContainer" in row:
            try:
                #print(f"Decoding enrichmentContainer: {row['enrichmentContainer']}")  # Depuración
                enrichment_data = json.loads(row.pop("enrichmentContainer"))  # Eliminar y convertir
                
                # Extraer countryCode y colocarlo en el nivel de row
                country_code = enrichment_data.pop("geoLocation", {}).pop("countryCode", None)
                if country_code:
                    row["countryCode"] = country_code
                
                row.update(enrichment_data)  # Fusionar los datos en row
                
                # Eliminar geoLocation si aún existe
                row.pop("geoLocation", None)
            except json.JSONDecodeError:
                print("Error al decodificar enrichmentContainer")
    
    return data
