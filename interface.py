# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 2026
@author: Radware CALA TAM - Nicolas Pedraza
"""

import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import threading
import shutil
import os
from tkinter import filedialog

# Importar las funciones de ejecución
from main_waf import main_waf
from main_bot import main_bot

# --- Paleta de Colores ---
COLOR_AMARILLO_BORDE = "#ffaa01"
COLOR_AZUL_TITULO = "#1c5573"
COLOR_AZUL_CLARO_BORDE = "#348097"
COLOR_ROJO_RADWARE = "#ed1b24"
COLOR_GRIS_TEXTO = "#636466"
COLOR_BLANCO = "#ffffff"
COLOR_FONDO_APP = "#f2f2f2"

ctk.set_appearance_mode("Light")

class AutoreportRadware(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Autoreport Radware")
        self.geometry("600x850") # Un poco más alto para el nuevo botón
        self.configure(fg_color=COLOR_FONDO_APP)

        # Fuentes
        self.font_titulo = ("Segoe UI Semibold", 28)
        self.font_label = ("Segoe UI Semibold", 13)
        self.font_input = ("Segoe UI", 12)
        self.font_calendario = ("Segoe UI", 13)

        self.archivo_generado = None

        # --- Título ---
        self.label_titulo = ctk.CTkLabel(self, text="AUTOREPORT RADWARE", 
                                         font=self.font_titulo, text_color=COLOR_AZUL_TITULO)
        self.label_titulo.pack(pady=(30, 10))

        # --- Contenedor Principal ---
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BLANCO, corner_radius=15,
                                       border_width=2, border_color=COLOR_AMARILLO_BORDE)
        self.main_frame.pack(pady=10, padx=50, fill="both", expand=True)

        # --- Inputs ---
        self.entry_domain = self.crear_campo_limpio("Application (Domain)", "🌐", "example.com")
        self.entry_key = self.crear_campo_limpio("X-API-KEY", "🔑", "Insert your key", is_password=True)
        self.entry_account = self.crear_campo_limpio("Account ID", "🏢", "ID")

        # --- Rango de Tiempo ---
        lbl_rango = ctk.CTkLabel(self.main_frame, text="Time Range", font=self.font_label, text_color=COLOR_AZUL_TITULO)
        lbl_rango.pack(pady=(15, 5), padx=40, anchor="w")

        self.date_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.date_frame.pack(fill="x", padx=40)

        style_cal = {"background": COLOR_AZUL_TITULO, "foreground": "white", "headersbackground": COLOR_GRIS_TEXTO}
        
        self.cal_start = DateEntry(self.date_frame, **style_cal, date_pattern='yyyy-mm-dd', font=self.font_calendario)
        self.cal_start.pack(side="left", padx=(10, 5), expand=True)

        ctk.CTkLabel(self.date_frame, text="to", text_color=COLOR_AZUL_TITULO, font=self.font_label).pack(side="left")

        self.cal_end = DateEntry(self.date_frame, **style_cal, date_pattern='yyyy-mm-dd', font=self.font_calendario)
        self.cal_end.pack(side="left", padx=(5, 10), expand=True)

        # --- Tipo de Servicio ---
        lbl_serv = ctk.CTkLabel(self.main_frame, text="Service", font=self.font_label, text_color=COLOR_AZUL_TITULO)
        lbl_serv.pack(pady=(20, 5), padx=40, anchor="w")
        
        self.combo_tipo = ctk.CTkComboBox(self.main_frame, values=["WAF", "BOT"], 
                                          command=self.actualizar_restriccion_fechas)
        self.combo_tipo.set("WAF")
        self.combo_tipo.pack(pady=(0, 20), padx=40, fill="x")

        # --- Filtro ---
        self.check_blocked = ctk.CTkCheckBox(self.main_frame, text="Only Blocked Events", 
                                             fg_color=COLOR_AZUL_TITULO, text_color="black")
        self.check_blocked.pack(pady=10)
        self.check_blocked.select()

        # --- Botones y Status ---
        self.btn_ejecutar = ctk.CTkButton(self, text="Generate Report", font=("Segoe UI semibold", 16),
                                          fg_color=COLOR_AZUL_TITULO, height=50, corner_radius=10,
                                          command=self.iniciar_hilo_proceso)
        self.btn_ejecutar.pack(pady=(20, 10), padx=50, fill="x")

        self.label_status = ctk.CTkLabel(self, text="", font=("Segoe UI Semibold", 12), text_color=COLOR_AZUL_TITULO)
        self.label_status.pack(pady=(0, 5))

        self.btn_descargar = ctk.CTkButton(self, text="📥 Download JSON", fg_color="#28a745", 
                                           hover_color="#218838", command=self.descargar_archivo)
        
        self.actualizar_restriccion_fechas("WAF")

    def crear_campo_limpio(self, label_text, icono, placeholder, is_password=False):
        lbl = ctk.CTkLabel(self.main_frame, text=label_text, font=self.font_label, text_color=COLOR_AZUL_TITULO)
        lbl.pack(pady=(15, 2), padx=40, anchor="w")
        container = ctk.CTkFrame(self.main_frame, fg_color=COLOR_BLANCO, height=40)
        container.pack(padx=40, fill="x")
        ico_lbl = ctk.CTkLabel(container, text=icono, font=("Segoe UI Symbol", 18), text_color=COLOR_AZUL_TITULO)
        ico_lbl.pack(side="left", padx=(10, 5))
        entry = ctk.CTkEntry(container, placeholder_text=placeholder, border_width=0,
                             fg_color="transparent", font=self.font_input, text_color="black")
        entry.pack(side="left", fill="both", expand=True, padx=5)
        if is_password: entry.configure(show="*")
        return entry

    def actualizar_restriccion_fechas(self, seleccion):
        hoy = datetime.now()
        dias = 30 if seleccion == "WAF" else 7
        fecha_min = hoy - timedelta(days=dias)
        self.cal_start.config(mindate=fecha_min, maxdate=hoy)
        self.cal_end.config(mindate=fecha_min, maxdate=hoy)

    def iniciar_hilo_proceso(self):
        # Recopilar configuración
        config = {
            "domain": self.entry_domain.get(),
            "x_api_key": self.entry_key.get(),
            "account_id": self.entry_account.get(),
            "start": f"{self.cal_start.get_date()} 00:00:00",
            "end": f"{self.cal_end.get_date()} 23:59:59",
            "service": self.combo_tipo.get(),
            "only_blocked": "y" if self.check_blocked.get() else "n"
        }
        
        self.btn_descargar.pack_forget() # Ocultar botón si estaba visible
        self.mostrar_carga()
        
        # Lanzar proceso en segundo plano
        thread = threading.Thread(target=self.ejecutar_reporte, args=(config,))
        thread.start()

    def ejecutar_reporte(self, config):
        try:
            if config["service"] == "WAF":
                main_waf(config)
                self.archivo_generado = f"{config['domain']}.json"
            else:
                main_bot(config)
                self.archivo_generado = f"{config['domain']}_bot.json"
            
            self.after(0, lambda: self.finalizar_proceso(True))
        except Exception as e:
            print(f"Error: {e}")
            self.after(0, lambda: self.finalizar_proceso(False, str(e)))

    def mostrar_carga(self):
        self.label_status.configure(text="Processing data...")
        self.ventana_carga = ctk.CTkToplevel(self)
        self.ventana_carga.title("Generating")
        self.ventana_carga.geometry("300x150")
        self.ventana_carga.transient(self)
        self.ventana_carga.grab_set()
        
        ctk.CTkLabel(self.ventana_carga, text="Requesting to Radware API...", font=self.font_label).pack(pady=20)
        self.progreso = ctk.CTkProgressBar(self.ventana_carga, mode="indeterminate", progress_color=COLOR_AMARILLO_BORDE)
        self.progreso.pack(pady=10, padx=30, fill="x")
        self.progreso.start()

    def finalizar_proceso(self, exito, error_msg=""):
        self.progreso.stop()
        self.ventana_carga.destroy()
        if exito:
            self.label_status.configure(text="✅ Report Generated Successfully", text_color="green")
            self.btn_descargar.pack(pady=10, padx=50, fill="x")
        else:
            self.label_status.configure(text=f"❌ Error: {error_msg[:30]}...", text_color="red")

    def descargar_archivo(self):
        if self.archivo_generado and os.path.exists(self.archivo_generado):
            destino = filedialog.asksaveasfilename(defaultextension=".json",
                                                   initialfile=self.archivo_generado,
                                                   title="Save JSON Report")
            if destino:
                shutil.copy(self.archivo_generado, destino)
                self.label_status.configure(text=f"Saved to: {os.path.basename(destino)}")
