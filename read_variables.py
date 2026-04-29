# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 16:58:16 2025

@author: Radware CALA TAM
"""

def read_variables():
    # 1. Se solicita el dominio de primero
    domain = input("\n1. Domain: ").strip()
    x_api_key = input("\n2. x_api_key: ")
    account_id = input("\n3. account_id: ")
    lower_str = input("\n4. Start Time (format YYYY-MM-DD HH:MM:SS): ")
    upper_str = input("\n5. End Time (format YYYY-MM-DD HH:MM:SS): ")
    
    while True:
        action_filter = input("\n6. Only \"Blocked\" events? [Y]yes or [N]no: ")
        if action_filter.lower() in ("y", "n"):
            break
        else:
            print("Select a valid option [Y] or [N]")
            
    # El filename ahora se asigna automáticamente usando el domain
    filename = f"{domain}.json"

    return domain, x_api_key, account_id, lower_str, upper_str, action_filter, filename