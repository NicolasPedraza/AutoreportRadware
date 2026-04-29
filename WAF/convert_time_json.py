# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 17:59:32 2025

@author: NicolasP1206
"""

import json
from datetime import datetime, timedelta

def convert_time_json(input_json):
    # Parseamos el JSON si es una cadena
    if isinstance(input_json, str):
        input_json = json.loads(input_json)
    
    # Iteramos sobre los elementos en "data"
    for item in input_json.get("data", []):
        row = item.get("row", {})
        if "receivedTimeStamp" in row:
            # Convertimos el timestamp de milisegundos a segundos 
            timestamp = int(row["receivedTimeStamp"]) // 1000
            formatted_time = (datetime.utcfromtimestamp(timestamp) - timedelta(hours=0)).strftime("%Y-%m-%d %H:%M:%S")
            row["receivedTimeStamp"] = formatted_time
    
    return input_json