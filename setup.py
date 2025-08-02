#!/usr/bin/env python3
"""
Script de Instalación para el Compresor de Huffman
=================================================

Instala automáticamente las dependencias necesarias y verifica
que el entorno esté configurado correctamente.

Uso:
    python setup.py
"""

import subprocess
import sys
import os
from pathlib import Path

def verificar_python():
    """Verifica que la versión de Python sea compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def instalar_dependencias():
    """Instala las dependencias del archivo requirements.txt."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Archivo requirements.txt no encontrado")
        return False
    
    try:
        print("📦 Instalando dependencias...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True, check=True)
        
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        print(f"   Salida del error: {e.stderr}")
        return False

def verificar_instalacion():
    """Verifica que todas las dependencias estén correctamente instaladas."""
    try:
        import customtkinter
        print("✅ customtkinter - Instalado correctamente")
        
        # Importar módulos del proyecto
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from huffman_tree import ArbolHuffman
        from huffman_compressor import CompresorHuffman
        from gui_interface import verificar_dependencias
        
        print("✅ Módulos del proyecto - Importados correctamente")
        
        if verificar_dependencias():
            print("✅ GUI - Funcionando correctamente")
        else:
            print("⚠️  GUI - Algunas dependencias pueden faltar")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error en verificación: {e}")
        return False

def main():
    """Función principal del script de instalación."""
    print("🔧 INSTALACIÓN DEL COMPRESOR DE HUFFMAN")
    print("=" * 50)
    
    # Verificar Python
    if not verificar_python():
        return 1
    
    # Instalar dependencias
    if not instalar_dependencias():
        return 1
    
    # Verificar instalación
    if not verificar_instalacion():
        print("⚠️  La instalación se completó pero hay advertencias")
        print("   El programa debería funcionar, pero algunas características pueden no estar disponibles")
    else:
        print("\n🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("\n🚀 Para empezar a usar el programa:")
        print("   python main.py --gui        # Interfaz gráfica")
        print("   python main.py --cli        # Línea de comandos")
        print("   python launcher.py          # Script launcher")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
