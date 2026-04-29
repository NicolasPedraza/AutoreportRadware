# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 21:54:10 2025

@author: NicolasP1206
"""

import pycountry

def convert_country_waf(json_data):
    try:
        # Extraer la lista de datos
        data_list = json_data.get("data", [])
        
        # Iterar sobre los datos y extraer los códigos de país
        for item in data_list:
            row = item.get("row", {})
            country_code = row.get("countryCode")
            
            if country_code:
                # Manejo de excepciones específicas
                if country_code == "VE":
                    country_name = "Venezuela"
                elif country_code == "RU":
                    country_name = "Russia"
                elif country_code == "BO":
                    country_name = "Bolivia"
                else:
                    country = pycountry.countries.get(alpha_2=country_code)
                    country_name = country.name if country else "Código desconocido"
                
                row["countryName"] = country_name  # Agregar el nombre del país al JSON
        
        return json_data
    except Exception as e:
        return {"error": str(e)}