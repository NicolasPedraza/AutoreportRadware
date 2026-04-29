def min_time_waf(json_data, upper):

    # Validar si json_data es None o no contiene "data"
    if not json_data or "data" not in json_data:
        # Si no hay datos válidos, retornar el upper actual sin modificar
        print("latest_timestamp: json_data vacío o inválido. Retornando upper sin cambios...")
        return upper

    data_list = json_data.get("data")

    # Si data viene vacío también mantener upper
    if not data_list:
        return upper

    # Tomar solo datos con "receivedTimeStamp"
    timestamps = [
        int(entry["row"].get("receivedTimeStamp", upper))
        for entry in data_list if "row" in entry
    ]

    # Si quedaron timestamps válidos:
    return min(timestamps) if timestamps else upper
