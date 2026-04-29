import json

def count_events_waf(data_json):
    """
    Retorna el número real de elementos en la lista 'data'.
    """
    # Si recibes un string (como en este ejemplo de prueba), lo convertimos a diccionario
    if isinstance(data_json, str):
        try:
            data_json = json.loads(data_json)
        except json.JSONDecodeError:
            return 0
    
    # Accedemos a la llave 'data' y contamos su longitud
    events = data_json.get("data", [])
    
    return len(events)
