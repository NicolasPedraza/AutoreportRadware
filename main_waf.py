# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 15:48:38 2025
@author: Radware CALA TAM - Nicolas Pedraza
"""

from WAF.get_json_waf import get_json_waf
from WAF.get_json_waf_blocked import get_json_waf_blocked
from WAF.min_time_waf import min_time_waf
from WAF.concat_json import concat_json
from WAF.expand_info_json import expand_info_json
from WAF.convert_country_waf import convert_country_waf
from WAF.count_events_waf import count_events_waf
from WAF.convert_time_json import convert_time_json

from human2epoch import human2epoch
from generate_json_file import generate_json_file
from get_app_id import get_app_id
from output_path import output_path

def main_waf(config):
    """
    Procesa eventos de WAF usando la configuración recibida desde la interfaz.
    """
    # 1. Extracción de parámetros desde el diccionario de la UI
    domain = config["domain"]
    x_api_key = config["x_api_key"]
    account_id = config["account_id"]
    lower_str = config["start"]
    upper_str = config["end"]
    action_filter = config["only_blocked"]
    filename = f"{domain}.json"
    
    # Obtener ID de aplicación dinámicamente
    app_id = get_app_id(domain, x_api_key, account_id) 
    output_directory = output_path()

    # 2. Conversión de tiempos
    lower = human2epoch(lower_str)
    upper = human2epoch(upper_str)

    # 3. Selección de función de API
    if action_filter.lower() == "y":
        get_json = get_json_waf_blocked
    else:
        get_json = get_json_waf

    output_json = {}
    events = 1
    i = 0

    # 4. Bucle de extracción con paginación inversa
    while events > 0:
        current_json = get_json(lower, upper, x_api_key, account_id, app_id)
        output_json = concat_json(output_json, current_json)
        
        # Actualizar el tope de tiempo para la siguiente página
        upper = min_time_waf(output_json, upper)
        events = count_events_waf(current_json)
        
        # Feedback en consola (opcional, ya que la UI tiene su barra)
        i += 1
        #print(f"\rPaginated WAF requests: {i}", end="", flush=True)

    # 5. Transformación de datos
    if output_json:
        output_json = convert_time_json(output_json)
        output_json = expand_info_json(output_json)
        output_json = convert_country_waf(output_json)

        # 6. Guardar archivo localmente
        generate_json_file(output_json, output_directory, filename)
    else:
        raise Exception("No events found for the selected period.")