import json

def count_events_bot(data_json):
    """
    Retorna el número real de elementos en la lista 'results'.
    """
    # Si recibes un string, lo convertimos a diccionario con manejo de errores
    if isinstance(data_json, str):
        try:
            data_json = json.loads(data_json)
        except json.JSONDecodeError:
            # Si el JSON es inválido, retornamos 0 para evitar que el programa falle
            return 0
    
    # Verificamos que data_json sea un diccionario antes de usar .get()
    # (Por si acaso el JSON era un valor válido pero no un objeto, como un número o null)
    if not isinstance(data_json, dict):
        return 0

    # Accedemos a la llave 'results' y contamos su longitud
    # Usamos .get() por seguridad en caso de que la llave no exista
    events = data_json.get("results", [])
    
    return len(events)