# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 15:03:32 2025

@author: NicolasP1206
"""

import requests

def get_json_waf(lower, upper, x_api_key, account_id, app_id):
    
    # URL del endpoint
    url = "https://api.radwarecloud.app/mgmt/monitor/reporter/reports-ext/APPWALL_REPORTS"
    
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
                "type": "orFilter",
                "filters": [
                    {
                    "type": "termFilter",
                    "inverseFilter": False,
                    "field": "action",
                    "value": "Blocked"
                    },
                    {
                    "type": "termFilter",
                    "inverseFilter": False,
                    "field": "action",
                    "value": "Reported"
                    }
                ]
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


