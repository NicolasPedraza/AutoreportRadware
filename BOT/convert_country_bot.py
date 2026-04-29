import json
import pycountry

def convert_country_bot(data_json):
    """
    Convierte los códigos ISO de país a nombres completos en la lista 'results'.
    Maneja excepciones personalizadas para VE, RU y BO.
    """
    # Mapeo personalizado solicitado
    custom_mapping = {
        "VE": "Venezuela",
        "RU": "Russia",
        "BO": "Bolivia"
    }

    # Convertir a dict si es string
    data = json.loads(data_json) if isinstance(data_json, str) else data_json
    
    if "results" in data:
        for evento in data["results"]:
            codigo = evento.get("country_code")
            
            if codigo:
                # 1. Prioridad al mapeo personalizado
                if codigo in custom_mapping:
                    evento["country_code"] = custom_mapping[codigo]
                else:
                    # 2. Conversión normal usando pycountry
                    try:
                        pais = pycountry.countries.get(alpha_2=codigo)
                        if pais:
                            evento["country_code"] = pais.name
                    except Exception:
                        # Si falla o no se encuentra, se mantiene el código original
                        pass
                        
    return data