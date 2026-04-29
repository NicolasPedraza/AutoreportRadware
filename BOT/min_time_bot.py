import json

def min_time_bot(data_json, upper):
    # 1. Si el input es un string (JSON crudo), lo convertimos a diccionario
    if isinstance(data_json, str):
        try:
            data_json = json.loads(data_json)
        except json.JSONDecodeError:
            print("min_time_bot: Error decodificando JSON. Retornando upper...")
            return upper

    # 2. Validar si data_json es None o no contiene "results" (siguiendo estructura de Codigo 1)
    if not data_json or "results" not in data_json:
        print("min_time_bot: data_json vacío o sin llave 'results'. Retornando upper...")
        return upper

    eventos = data_json.get("results")

    # 3. Si la lista viene vacía, mantener upper
    if not eventos:
        return upper

    # 4. Extraer timestamps usando la misma lógica de filtrado que el Código 1
    # Se asegura de que el campo "time" exista, de lo contrario usa upper por defecto
    timestamps = [
        int(e.get("time", upper))
        for e in eventos if isinstance(e, dict)
    ]

    # 5. Retornar el mínimo si existen datos, de lo contrario retornar upper
    return min(timestamps) if timestamps else upper