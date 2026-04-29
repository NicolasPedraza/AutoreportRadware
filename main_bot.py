# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 2026
@author: Radware CALA TAM - Nicolas Pedraza
"""

from BOT.get_json_bot import get_json_bot
from BOT.get_json_bot_blocked import get_json_bot_blocked
from BOT.min_time_bot import min_time_bot
from BOT.count_events_bot import count_events_bot
from BOT.concat_json_bot import concat_json_bot
from BOT.convert_country_bot import convert_country_bot
from BOT.convert_time_json_bot import convert_time_json_bot

from human2epoch import human2epoch
from generate_json_file import generate_json_file
from get_app_id import get_app_id
from output_path import output_path

def main_bot(config):
    """
    Procesa eventos de Bot Manager usando la configuración de la interfaz.
    """
    # 1. Extracción de parámetros
    domain = config["domain"]
    x_api_key = config["x_api_key"]
    account_id = config["account_id"]
    lower_str = config["start"]
    upper_str = config["end"]
    action_filter = config["only_blocked"]
    filename = f"{domain}_bot.json"

    app_id = get_app_id(domain, x_api_key, account_id) 
    output_directory = output_path()

    # 2. Tiempos
    lower = human2epoch(lower_str)
    upper = human2epoch(upper_str)

    # 3. Lógica de filtrado
    if action_filter.lower() == "y":
        get_json = get_json_bot_blocked
    else:
        get_json = get_json_bot

    output_json = {}
    events = 1
    i = 0

    # 4. Extracción
    while events > 0:
        current_json = get_json(lower, upper, x_api_key, account_id, app_id)
        output_json = concat_json_bot(output_json, current_json)
        
        upper = min_time_bot(output_json, upper)
        events = count_events_bot(current_json)
        
        i += 1
        #print(f"\rPaginated BOT requests: {i}", end="", flush=True)

    # 5. Post-procesamiento
    if output_json:
        output_json = convert_time_json_bot(output_json)
        output_json = convert_country_bot(output_json)

        # 6. Exportación
        generate_json_file(output_json, output_directory, filename)
    else:
        raise Exception("No Bot events found.")