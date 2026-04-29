import requests

def get_app_id(domain, x_api_key, account_id):
    """
    Consumes the Radware API and searches for a domain to return its application ID.
    """
    url = "https://api.radwarecloud.app/v1/gms/applications"
    headers = {
        "x-api-key": x_api_key,
        "context": account_id,
        "Content-Type": "application/json"
    }

    try:
        # 1. Consumir la API
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return f"Error: Received status code {response.status_code} from API"

        data = response.json()
        
        # 2. Buscar el dominio en el contenido
        # Según example_apps.json, la lista está en la llave "content"
        applications = data.get("content", [])
        
        for app in applications:
            # Ruta solicitada: content.featuresData.wafFeatureData.mainDomain.mainDomain
            features = app.get("featuresData", {})
            waf_data = features.get("wafFeatureData", {})
            main_domain_obj = waf_data.get("mainDomain", {})
            actual_domain = main_domain_obj.get("mainDomain")

            if actual_domain == domain:
                # 3. Retornar el ID si hay coincidencia
                return app.get("id")

        # 4. Mensaje si no se encuentra
        return "Domain not found"

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
# --- BLOQUE DE PRUEBA (MAIN) ---
if __name__ == "__main__":
    # Configuración de prueba
    # Reemplaza estos valores con tus credenciales reales
    MI_API_KEY = "eyJhbGciOiJIUzM4NCJ9.eyJhY2NvdW50SWQiOnsidmFsdWUiOiI2N2FhMmU2OTc2ZDAwOTdkOTkxMTk5YTcifSwicm9sZUlkcyI6WyJyb2xfeFpuQUcxbXJQdkdWZmQ3cSIsInJvbF8ya1JqbEVJQnpjN05wRVVXIiwicm9sX2g2TUJWa1lHcXlTVzNNQjMiLCJyb2xfQTR6enE3dW5EYkRsdXdkVyIsInJvbF9tcjJKOFdlY0kyUXhTTVJnIiwicm9sX1FoQXF5cFAwOFFlNDZnZHAiLCJyb2xfWE1KR0ZyVTM0eEpnYklXMCIsInJvbF9UaGNJYTVQQW9vNkxaeUFJIl0sImV4cGlyeVRpbWVzdGFtcCI6MTc3NzUyNTIwMCwiaWQiOnsidmFsdWUiOiI2OWYxMTMzMjJhNzA3NTAzMTc5ZDViMGIifX0.O4V0FzwSLMJlnXsuFptERVLgLPGEm4_70MQysbNJng6QK-VxzBDyUijxQc3SUzvL"
    MI_ACCOUNT_ID = "dbfbcbb0-ca9d-43eb-93ac-4a8e44c0cfba"
    DOMINIO_A_BUSCAR = "solicitudes.cydsa.com"

    print("--- Iniciando búsqueda de Application ID ---")
    print(f"Buscando dominio: {DOMINIO_A_BUSCAR}...")

    resultado = get_app_id(DOMINIO_A_BUSCAR, MI_API_KEY, MI_ACCOUNT_ID)

    print("-" * 40)
    if "Error" in str(resultado) or resultado == "Domain not found":
        print(f"❌ Resultado: {resultado}")
    else:
        print(f"✅ Éxito! El ID de la aplicación es: {resultado}")
    print("-" * 40)