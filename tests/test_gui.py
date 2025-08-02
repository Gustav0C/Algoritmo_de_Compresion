#!/usr/bin/env python
"""
Script de prueba simple para la GUI
"""

import sys
import os
from pathlib import Path

# Añadir directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / 'src'
sys.path.insert(0, str(src_dir))

try:
    print("Importando módulos...")
    from gui_interface import InterfazHuffman, verificar_dependencias
    
    print("Verificando dependencias...")
    if verificar_dependencias():
        print("Dependencias OK, iniciando GUI...")
        app = InterfazHuffman()
        app.ejecutar()
    else:
        print("Dependencias no disponibles")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
