# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 16:16:36 2025

@author: NicolasP1206
"""
from datetime import datetime, timezone, timedelta

def human2epoch(date_str):
    """Convierte una fecha en formato 'YYYY-MM-DD HH:MM:SS' a timestamp en milisegundos en UTC-5."""
    utc_minus_5 = timezone(timedelta(hours=-5))
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=utc_minus_5)  # Asigna la zona horaria UTC-5
    return int(dt.timestamp() * 1000)
