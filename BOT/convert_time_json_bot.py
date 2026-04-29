# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 18:30:00 2026

@author: NicolasP1206
"""

import json
from datetime import datetime, timedelta

def convert_time_json_bot(data_json):
    """
    Busca el campo 'time' en cada evento dentro de 'results' y convierte 
    el epoch (ms) al formato "Y-m-d H:M:S".
    """
    # Parseamos el JSON si es una cadena (basado en Código 1)
    if isinstance(data_json, str):
        data_json = json.loads(data_json)
    
    # Iteramos sobre los elementos en "results" (equivalente a "data" en Código 1)
    for evento in data_json.get("results", []):
        if "time" in evento:
            # Verificamos que sea un número antes de procesar
            epoch_ms = evento.get("time")
            if isinstance(epoch_ms, (int, float)):
                # Convertimos el timestamp de milisegundos a segundos
                timestamp = int(epoch_ms) // 1000
                
                # Formateamos usando la lógica de datetime.utc (más precisa para APIs)
                formatted_time = (datetime.utcfromtimestamp(timestamp) - timedelta(hours=0)).strftime("%Y-%m-%d %H:%M:%S")
                
                # Reemplazamos el valor original
                evento["time"] = formatted_time
    
    return data_json