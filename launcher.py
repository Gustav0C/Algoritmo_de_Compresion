#!/usr/bin/env python3
"""
Launcher Script para el Compresor de Huffman
==========================================

Script de conveniencia para lanzar la aplicación desde cualquier ubicación.
Configura automáticamente los paths y dependencias.

Uso:
    python launcher.py          # Lanza la GUI
    python launcher.py --cli    # Lanza el CLI
    python launcher.py --test   # Ejecuta tests
"""

import sys
import os
from pathlib import Path

def configurar_paths():
    """Configura los paths necesarios para importar módulos."""
    current_dir = Path(__file__).parent.absolute()
    src_dir = current_dir / 'src'
    
    # Agregar src/ al path de Python
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    # Cambiar directorio de trabajo al directorio del proyecto
    os.chdir(current_dir)
    
    return current_dir

def main():
    """Función principal del launcher."""
    # Configurar paths
    project_dir = configurar_paths()
    
    try:
        # Importar main desde el directorio del proyecto
        sys.path.insert(0, str(project_dir))
        from main import main as main_app
        
        # Ejecutar la aplicación principal
        main_app()
        
    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        print(f"🔧 Asegúrate de estar en el directorio del proyecto: {project_dir}")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
