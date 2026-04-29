# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 10:39:23 2025

@author: NicolasP1206
"""

import requests

def obtener_json_web_ddos(lower, upper, x_api_key, account_id, app_id):
  
    # URL del endpoint
    url = "https://api.radwarecloud.app/mgmt/monitor/reporter/reports-ext/L7_DDOS_ATTACK_REPORT"
    
    # Encabezados de la solicitud
    headers = {
        "x-api-key": x_api_key,
        "context": account_id,
        "Content-Type": "application/json"
    }
    
    # Cuerpo de la solicitud
    body = {
        "criteria": [
            {
                "type": "timeFilter",
                "field": "receivedTimeStamp",
                "includeLower": True,
                "includeUpper": True,
                "upper": upper,
                "lower": lower
            },
            {
			"field":"enrichmentContainer.applicationId",
			"inverseFilter": False,
			"type":"termFilter",
			"value": app_id
		    }
        ],
        "pagination": {
            "page": 0,
            "size": 10000 # Siempre va a forrzar al maximo valor (10k eventos)
        },
        "order": [
            {
                "type": "Order",
                "order": "DESC",
                "field": "receivedTimeStamp",
                "sortingType": "STRING"
            }
        ]
    }
    
    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=body)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        output_json = response.json()
        return output_json
    else:
        print(f"Error en la solicitud: {response.status_code}")
        print(response.text)
        return None
