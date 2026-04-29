import requests
import json

def get_json_bot_blocked(lower, upper, x_api_key, account_id, app_id):
    # URL del endpoint
    url = "https://api.radwarecloud.app/antibot/reports/v2/fetch/bad-bot/iia-list"
    
    # Encabezados de la solicitud
    headers = {
        "x-api-key": x_api_key,
        "context": account_id,
        "Content-Type": "application/json"
    }
    
    # Cuerpo de la solicitud (Corregido: se eliminó la doble llave innecesaria)
    body = {
        "applicationIds": [
            {
                "applicationId": app_id
            }
        ],
        "requestParameters": {
            "status": "Mitigated",
            "sort_order": "desc",
            "page_size": 10000,
            "page": 1,
            "starttime": lower,  
            "endtime": upper     
        }
    }
    
    # Realizar la solicitud POST
    try:
        response = requests.post(url, headers=headers, json=body)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la solicitud: {response.status_code}")
            print(f"Detalle: {response.text}")
            return None
    except Exception as e:
        print(f"Ocurrió un error de conexión: {e}")
        return None