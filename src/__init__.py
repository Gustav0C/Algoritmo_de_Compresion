"""
Archivo de inicialización del paquete del Compresor de Huffman
============================================================

Este archivo convierte el directorio en un paquete Python y define
las exportaciones públicas del módulo.

Autor: Gustav0C
Fecha: Agosto 2025
Versión: 1.0
"""

# Información del paquete
__version__ = "1.0.0"
__author__ = "Gustav0C"
__email__ = "gcanales58@gmail.com"
__description__ = "Implementación completa del algoritmo de compresión de Huffman"

# Exportaciones principales
from .huffman_tree import NodoHuffman, ArbolHuffman
from .huffman_compressor import CompresorHuffman, UtilitiesCompresion

# Exportaciones condicionales (dependen de dependencias)
try:
    from .gui_interface import InterfazHuffman
    GUI_DISPONIBLE = True
except ImportError:
    GUI_DISPONIBLE = False

try:
    from .cli_interface import CLIHuffman
    CLI_DISPONIBLE = True
except ImportError:
    CLI_DISPONIBLE = False

# Lista de exportaciones públicas
__all__ = [
    'NodoHuffman',
    'ArbolHuffman',
    'CompresorHuffman',
    'UtilitiesCompresion',
    'GUI_DISPONIBLE',
    'CLI_DISPONIBLE'
]

# Agregar exportaciones condicionales
if GUI_DISPONIBLE:
    __all__.append('InterfazHuffman')

if CLI_DISPONIBLE:
    __all__.append('CLIHuffman')


def obtener_info_paquete():
    """
    Obtiene información básica del paquete.
    
    Returns:
        Dict con información del paquete
    """
    return {
        'nombre': 'huffman_compressor',
        'version': __version__,
        'autor': __author__,
        'descripcion': __description__,
        'gui_disponible': GUI_DISPONIBLE,
        'cli_disponible': CLI_DISPONIBLE
    }


def verificar_instalacion():
    """
    Verifica que el paquete esté correctamente instalado.
    
    Returns:
        Bool indicando si la instalación es correcta
    """
    try:
        # Verificar importaciones básicas
        from .huffman_tree import NodoHuffman, ArbolHuffman
        from .huffman_compressor import CompresorHuffman
        
        # Prueba básica de funcionalidad
        compresor = CompresorHuffman()
        resultado = compresor.comprimir("test")
        texto_codificado, codigos, arbol, _ = resultado
        
        if texto_codificado and codigos and arbol:
            return True
        
    except Exception:
        pass
    
    return False
