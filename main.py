# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 2026
@author: Radware CALA TAM - Nicolas Pedraza

Este es el archivo principal de ejecución. 
Ahora inicia la interfaz gráfica (GUI) la cual centraliza la lógica 
que antes se manejaba por consola.
"""

from interface import AutoreportRadware

def main():
    # Inicializamos la instancia de la aplicación personalizada de CustomTkinter
    app = AutoreportRadware()
    
    # El método mainloop mantiene la ventana abierta y escuchando eventos
    app.mainloop()

if __name__ == "__main__":
    main()