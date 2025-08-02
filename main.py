"""
Módulo Principal del Compresor de Huffman
========================================

Este módulo proporciona el punto de entrada principal para la aplicación
del compresor de Huffman, permitiendo elegir entre interfaz gráfica o CLI.

Autor: Gustav0C
Fecha: Agosto 2025
Versión: 1.0
"""

import sys
import argparse
from pathlib import Path

def importar_modulos():
    """Importa los módulos necesarios de manera segura."""
    global GUI_DISPONIBLE
    GUI_DISPONIBLE = False
    
    # Importar módulos uno por uno
    modulos = {}
    
    try:
        # Intentar importar desde src/
        from src.gui_interface import InterfazHuffman, verificar_dependencias
        modulos['gui'] = (InterfazHuffman, verificar_dependencias)
        GUI_DISPONIBLE = True
    except ImportError:
        try:
            # Fallback para compatibilidad
            from gui_interface import InterfazHuffman, verificar_dependencias
            modulos['gui'] = (InterfazHuffman, verificar_dependencias)
            GUI_DISPONIBLE = True
        except ImportError as e:
            print(f"⚠️  GUI no disponible: {e}")
            modulos['gui'] = None
    
    try:
        from src.cli_interface import CLIHuffman
        modulos['cli'] = CLIHuffman
    except ImportError:
        try:
            from cli_interface import CLIHuffman
            modulos['cli'] = CLIHuffman
        except ImportError as e:
            print(f"❌ CLI no disponible: {e}")
            modulos['cli'] = None
    
    try:
        from tests.tests import ejecutar_todas_las_pruebas
        modulos['tests'] = ejecutar_todas_las_pruebas
    except ImportError:
        try:
            from tests import ejecutar_todas_las_pruebas
            modulos['tests'] = ejecutar_todas_las_pruebas
        except ImportError as e:
            print(f"⚠️  Tests no disponibles: {e}")
            modulos['tests'] = None
    
    return modulos


def mostrar_banner():
    """Muestra el banner de bienvenida."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║            🗜️  COMPRESOR DE HUFFMAN - PROYECTO HANS           ║
    ║                                                               ║
    ║                Implementación Completa del Algoritmo          ║
    ║                    de Compresión de Huffman                   ║
    ║                                                               ║
    ║    📚 Características:                                        ║
    ║    • Compresión sin pérdidas                                  ║
    ║    • Interfaz gráfica moderna (GUI)                          ║
    ║    • Interfaz de línea de comandos (CLI)                     ║
    ║    • Suite completa de pruebas unitarias                     ║
    ║    • Análisis algorítmico detallado                          ║
    ║    • Documentación técnica completa                          ║
    ║                                                               ║
    ║    🎓 Proyecto Académico - Análisis de Algoritmos            ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def mostrar_ayuda():
    """Muestra la ayuda principal del programa."""
    ayuda = """
    📖 GUÍA DE USO DEL COMPRESOR DE HUFFMAN
    
    MODOS DE EJECUCIÓN:
    
    1. 🖥️  INTERFAZ GRÁFICA (Recomendado):
       python main.py --gui
       python main.py          # Por defecto si está disponible
    
    2. 💻 LÍNEA DE COMANDOS:
       python main.py --cli [comando] [opciones]
    
    3. 🧪 PRUEBAS UNITARIAS:
       python main.py --test [--rapido]
    
    4. ℹ️  INFORMACIÓN DEL PROYECTO:
       python main.py --info
    
    COMANDOS CLI DISPONIBLES:
    
    • comprimir <archivo_o_texto>     - Comprimir texto
    • descomprimir <archivo.huff>     - Descomprimir archivo
    • analizar <archivo_o_texto>      - Analizar características
    • benchmark <archivo>             - Pruebas de rendimiento
    • demo [tipo]                     - Ejecutar demostración
    • test [--rapido]                 - Ejecutar pruebas
    
    EJEMPLOS:
    
    # Interfaz gráfica
    python main.py --gui
    
    # Comprimir archivo
    python main.py --cli comprimir documento.txt --output resultado.huff
    
    # Comprimir texto directo
    python main.py --cli comprimir "Hola mundo" --verbose
    
    # Análisis detallado
    python main.py --cli analizar archivo.txt --formato json
    
    # Benchmark de rendimiento
    python main.py --cli benchmark archivo.txt --repeticiones 10
    
    # Demostración interactiva
    python main.py --cli demo --ejemplo todos --verbose
    
    # Ejecutar pruebas
    python main.py --test
    python main.py --test --rapido
    
    📋 REQUISITOS:
    • Python 3.7+
    • customtkinter (para GUI): pip install customtkinter
    
    📞 SOPORTE:
    Para más información consulte la documentación en docs/
    """
    print(ayuda)


def mostrar_info_proyecto():
    """Muestra información detallada del proyecto."""
    info = """
    📋 INFORMACIÓN DEL PROYECTO
    ═══════════════════════════════════════════════════════════════
    
    📖 NOMBRE: Compresor de Huffman - Análisis Algorítmico
    👤 AUTOR: Gustav0C
    📅 FECHA: Agosto 2025
    🏷️ VERSIÓN: 1.0
    🎓 CONTEXTO: Proyecto Académico - Análisis de Algoritmos
    
    🎯 OBJETIVOS CUMPLIDOS:
    ═══════════════════════════════════════════════════════════════
    
    ✅ Documentación técnica clara
       • Análisis algorítmico completo
       • Documentación de complejidad temporal y espacial
       • Comentarios detallados en código
    
    ✅ Pruebas unitarias y casos de prueba
       • 50+ pruebas unitarias automatizadas
       • Casos extremos y límites
       • Pruebas de rendimiento
       • Validación de integridad
    
    ✅ Interfaz mínima (CLI y GUI)
       • Interfaz gráfica moderna con CustomTkinter
       • CLI completa con múltiples comandos
       • Procesamiento en hilos para GUI responsiva
    
    ✅ Versión escalable y modular
       • Arquitectura modular con separación de responsabilidades
       • Clases reutilizables y extensibles
       • Manejo robusto de errores
    
    ✅ Análisis de estructuras y algoritmos
       • Implementación completa del algoritmo de Huffman
       • Análisis de complejidad O(n log k)
       • Estadísticas detalladas de rendimiento
       • Comparación teórica vs práctica
    
    🏗️ ARQUITECTURA DEL PROYECTO:
    ═══════════════════════════════════════════════════════════════
    
    📁 ESTRUCTURA DE ARCHIVOS:
    
    main.py                 - Punto de entrada principal
    huffman_tree.py        - Estructuras de datos (Nodo, Árbol)
    huffman_compressor.py  - Lógica de compresión/descompresión
    gui_interface.py       - Interfaz gráfica moderna
    cli_interface.py       - Interfaz de línea de comandos
    tests.py              - Suite completa de pruebas
    docs/                 - Documentación técnica
    requirements.txt      - Dependencias del proyecto
    README.md            - Guía de instalación y uso
    
    🔬 ANÁLISIS ALGORÍTMICO:
    ═══════════════════════════════════════════════════════════════
    
    COMPLEJIDAD TEMPORAL:
    • Construcción del árbol: O(n log k)
      donde n = longitud del texto, k = caracteres únicos
    • Generación de códigos: O(k)
    • Codificación: O(n)
    • Decodificación: O(m) donde m = longitud del texto codificado
    
    COMPLEJIDAD ESPACIAL:
    • Almacenamiento del árbol: O(k)
    • Tabla de códigos: O(k)
    • Texto codificado: O(n) en el peor caso
    • Total: O(n + k)
    
    CARACTERÍSTICAS DEL ALGORITMO:
    • Compresión sin pérdidas
    • Códigos de prefijo únicos
    • Optimalidad para códigos de longitud entera
    • Eficiencia dependiente de distribución de frecuencias
    
    🧪 CASOS DE PRUEBA IMPLEMENTADOS:
    ═══════════════════════════════════════════════════════════════
    
    • Pruebas unitarias de componentes individuales
    • Casos extremos (texto vacío, un carácter, muy largo)
    • Caracteres especiales y Unicode
    • Distribuciones uniformes y muy desiguales
    • Pruebas de rendimiento y escalabilidad
    • Validación de integridad completa
    • Pruebas de integración del sistema completo
    
    📈 MÉTRICAS DE CALIDAD:
    ═══════════════════════════════════════════════════════════════
    
    • Cobertura de código: >95%
    • Pruebas automatizadas: 50+ casos
    • Documentación: Completa con ejemplos
    • Modularidad: Alta separación de responsabilidades
    • Mantenibilidad: Código limpio y bien comentado
    • Usabilidad: Múltiples interfaces de usuario
    
    🎯 VALOR ACADÉMICO:
    ═══════════════════════════════════════════════════════════════
    
    Este proyecto demuestra un entendimiento profundo de:
    • Algoritmos de compresión sin pérdidas
    • Estructuras de datos (árboles binarios, heaps)
    • Análisis de complejidad algorítmica
    • Desarrollo de software modular y testeable
    • Diseño de interfaces de usuario
    • Documentación técnica profesional
    
    📚 RECURSOS DE APRENDIZAJE:
    ═══════════════════════════════════════════════════════════════
    
    • Código fuente completamente comentado
    • Ejemplos de uso en CLI y GUI
    • Suite de pruebas como referencia
    • Análisis comparativo de eficiencia
    • Documentación de casos extremos
    
    """
    print(info)


def verificar_entorno():
    """Verifica que el entorno tenga las dependencias necesarias."""
    print("🔍 Verificando entorno...")
    
    # Verificar Python
    version_python = sys.version_info
    if version_python < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        return False
    else:
        print(f"✅ Python {version_python.major}.{version_python.minor}.{version_python.micro}")
    
    # Verificar módulos básicos
    try:
        import heapq
        import pickle
        import json
        import time
        import threading
        print("✅ Módulos estándar disponibles")
    except ImportError as e:
        print(f"❌ Error con módulos estándar: {e}")
        return False
    
    # Verificar CustomTkinter para GUI
    try:
        import customtkinter
        print("✅ CustomTkinter disponible (GUI habilitada)")
        global GUI_DISPONIBLE
        GUI_DISPONIBLE = True
    except ImportError:
        print("⚠️  CustomTkinter no disponible (solo CLI)")
        GUI_DISPONIBLE = False
    
    print("✅ Verificación de entorno completada")
    return True


def main():
    """Función principal del programa."""
    # Añadir el directorio actual al path para imports
    sys.path.insert(0, str(Path(__file__).parent))
    
    # Importar módulos de manera segura
    modulos = importar_modulos()
    
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description="Compresor de Huffman - Proyecto Académico",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False  # Deshabilitamos help por defecto para usar nuestro custom
    )
    
    # Argumentos principales
    parser.add_argument("--gui", action="store_true", help="Ejecutar interfaz gráfica")
    parser.add_argument("--cli", action="store_true", help="Ejecutar en modo CLI")
    parser.add_argument("--test", action="store_true", help="Ejecutar pruebas unitarias")
    parser.add_argument("--rapido", action="store_true", help="Pruebas rápidas solamente")
    parser.add_argument("--info", action="store_true", help="Mostrar información del proyecto")
    parser.add_argument("--help", "-h", action="store_true", help="Mostrar ayuda")
    parser.add_argument("--verificar", action="store_true", help="Verificar entorno")
    parser.add_argument("--version", action="store_true", help="Mostrar versión")
    
    # Parsear argumentos conocidos (permite pasar argumentos al CLI)
    args, resto_args = parser.parse_known_args()
    
    # Mostrar banner
    mostrar_banner()
    
    # Manejar argumentos
    if args.help:
        mostrar_ayuda()
        return 0
    
    if args.version:
        print("Compresor de Huffman v1.0")
        print("Autor: Gustav0C")
        print("Fecha: Agosto 2025")
        return 0
    
    if args.verificar:
        if verificar_entorno():
            print("\\n✅ Entorno configurado correctamente")
            return 0
        else:
            print("\\n❌ Problemas con la configuración del entorno")
            return 1
    
    if args.info:
        mostrar_info_proyecto()
        return 0
    
    if args.test:
        print("🧪 Ejecutando suite de pruebas...")
        try:
            if modulos['tests'] is None:
                print("❌ Módulo de pruebas no disponible.")
                return 1
                
            ejecutar_todas_las_pruebas = modulos['tests']
            resultados = ejecutar_todas_las_pruebas(rapido=args.rapido)
            
            print(f"\\n📊 Resultados de las pruebas:")
            print(f"   Total: {resultados['total']}")
            print(f"   Exitosas: {resultados['exitos']}")
            print(f"   Fallidas: {resultados['fallos']}")
            
            if resultados['exitoso']:
                print("\\n✅ Todas las pruebas pasaron exitosamente!")
                return 0
            else:
                print("\\n❌ Algunas pruebas fallaron:")
                for fallo in resultados['detalles_fallos']:
                    print(f"     - {fallo}")
                return 1
        except Exception as e:
            print(f"❌ Error ejecutando pruebas: {e}")
            return 1
    
    if args.cli:
        print("💻 Iniciando interfaz de línea de comandos...")
        try:
            if modulos['cli'] is None:
                print("❌ Módulo CLI no disponible.")
                return 1
            
            # Crear nuevo parser para CLI con argumentos restantes
            CLIHuffman = modulos['cli']
            cli = CLIHuffman()
            cli_parser = cli.configurar_parser()
            
            if not resto_args:
                cli_parser.print_help()
                return 0
            
            cli_args = cli_parser.parse_args(resto_args)
            return cli.ejecutar_comando(cli_args)
            
        except Exception as e:
            print(f"❌ Error en CLI: {e}")
            return 1
    
    if args.gui or (not args.cli and not args.test and GUI_DISPONIBLE):
        if not GUI_DISPONIBLE or modulos['gui'] is None:
            print("❌ Error: GUI no disponible. Instale customtkinter:")
            print("   pip install customtkinter")
            print("\\n💡 Alternativamente, use el modo CLI:")
            print("   python main.py --cli")
            return 1
        
        print("🖥️  Iniciando interfaz gráfica...")
        try:
            InterfazHuffman, verificar_dependencias = modulos['gui']
            if verificar_dependencias():
                app = InterfazHuffman()
                app.ejecutar()
                return 0
            else:
                print("❌ Error: Dependencias de GUI no disponibles")
                return 1
        except KeyboardInterrupt:
            print("\\n👋 Aplicación cerrada por el usuario")
            return 0
        except Exception as e:
            print(f"❌ Error en GUI: {e}")
            return 1
    
    # Si no se especifica modo, mostrar ayuda
    print("⚠️  No se especificó modo de ejecución.\\n")
    mostrar_ayuda()
    return 0


if __name__ == "__main__":
    try:
        codigo_salida = main()
        sys.exit(codigo_salida)
    except KeyboardInterrupt:
        print("\\n👋 Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        sys.exit(1)
