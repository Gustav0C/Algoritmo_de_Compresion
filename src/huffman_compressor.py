"""
Módulo de Compresión y Descompresión Huffman
===========================================

Este módulo implementa los algoritmos de compresión y descompresión
utilizando la codificación de Huffman.

Autor: Proyecto Hans
Fecha: Agosto 2025
Versión: 1.0

Características:
- Compresión sin pérdidas
- Códigos de longitud variable
- Optimización basada en frecuencias
- Manejo de casos especiales
"""

import time
from collections import Counter
from typing import Dict, Tuple, Optional, List

try:
    from .huffman_tree import ArbolHuffman, NodoHuffman
except ImportError:
    from huffman_tree import ArbolHuffman, NodoHuffman


class CompresorHuffman:
    """
    Implementación del algoritmo de compresión de Huffman.
    
    Esta clase proporciona métodos para comprimir y descomprimir texto
    utilizando la codificación de Huffman, que asigna códigos más cortos
    a caracteres más frecuentes.
    
    Atributos:
        arbol (ArbolHuffman): Árbol de Huffman para codificación
        estadisticas (Dict): Estadísticas de la última operación
    """
    
    def __init__(self):
        """Inicializa el compresor de Huffman."""
        self.arbol = ArbolHuffman()
        self.estadisticas = {}
    
    def calcular_frecuencias(self, texto: str) -> Dict[str, int]:
        """
        Calcula las frecuencias de aparición de cada carácter.
        
        Args:
            texto: Texto de entrada para analizar
            
        Returns:
            Diccionario con caracteres como claves y frecuencias como valores
            
        Complejidad Temporal: O(n) donde n = longitud del texto
        Complejidad Espacial: O(k) donde k = número de caracteres únicos
        """
        if not texto:
            return {}
        
        return dict(Counter(texto))
    
    def comprimir(self, texto: str) -> Tuple[str, Dict[str, str], NodoHuffman, Dict]:
        """
        Comprime un texto utilizando la codificación de Huffman.
        
        Args:
            texto: Texto a comprimir
            
        Returns:
            Tupla con:
            - texto_codificado: Cadena binaria comprimida
            - codigos: Diccionario de códigos de Huffman
            - raiz: Nodo raíz del árbol (necesario para descompresión)
            - estadisticas: Estadísticas de compresión
            
        Complejidad Temporal: O(n log k) donde n = longitud del texto, k = caracteres únicos
        Complejidad Espacial: O(n + k)
        """
        inicio_tiempo = time.time()
        
        if not texto:
            return "", {}, None, self._generar_estadisticas(texto, "", 0)
        
        # Paso 1: Calcular frecuencias de caracteres
        frecuencias = self.calcular_frecuencias(texto)
        
        # Paso 2: Construir árbol de Huffman
        self.arbol.construir_desde_frecuencias(frecuencias)
        
        # Paso 3: Generar códigos de Huffman
        codigos = self.arbol.generar_codigos()
        
        # Paso 4: Codificar el texto
        texto_codificado = self._codificar_texto(texto, codigos)
        
        tiempo_transcurrido = time.time() - inicio_tiempo
        
        # Generar estadísticas
        estadisticas = self._generar_estadisticas(texto, texto_codificado, tiempo_transcurrido)
        estadisticas.update(self.arbol.obtener_estadisticas())
        
        self.estadisticas = estadisticas
        
        return texto_codificado, codigos, self.arbol.raiz, estadisticas
    
    def _codificar_texto(self, texto: str, codigos: Dict[str, str]) -> str:
        """
        Codifica el texto utilizando los códigos de Huffman.
        
        Args:
            texto: Texto original
            codigos: Diccionario de códigos de Huffman
            
        Returns:
            Texto codificado como cadena binaria
        """
        return ''.join(codigos[caracter] for caracter in texto)
    
    def descomprimir(self, texto_codificado: str, raiz: NodoHuffman) -> Tuple[str, Dict]:
        """
        Descomprime un texto codificado utilizando el árbol de Huffman.
        
        Args:
            texto_codificado: Cadena binaria comprimida
            raiz: Nodo raíz del árbol de Huffman
            
        Returns:
            Tupla con:
            - texto_decodificado: Texto original recuperado
            - estadisticas: Estadísticas de descompresión
            
        Complejidad Temporal: O(m) donde m = longitud del texto codificado
        Complejidad Espacial: O(1) adicional (sin contar el texto de salida)
        """
        inicio_tiempo = time.time()
        
        if not texto_codificado or not raiz:
            return "", {"tiempo_descompresion": 0, "exito": False}
        
        texto_decodificado = ""
        nodo_actual = raiz
        
        # Caso especial: árbol con un solo carácter
        if raiz.es_hoja():
            texto_decodificado = raiz.caracter * len(texto_codificado)
        else:
            # Decodificación bit por bit
            for bit in texto_codificado:
                # Moverse por el árbol según el bit
                if bit == "0":
                    nodo_actual = nodo_actual.izquierdo
                else:
                    nodo_actual = nodo_actual.derecho
                
                # Si llegamos a una hoja, agregar el carácter y reiniciar
                if nodo_actual.es_hoja():
                    texto_decodificado += nodo_actual.caracter
                    nodo_actual = raiz
        
        tiempo_transcurrido = time.time() - inicio_tiempo
        
        estadisticas = {
            "tiempo_descompresion": tiempo_transcurrido,
            "longitud_decodificada": len(texto_decodificado),
            "exito": True
        }
        
        return texto_decodificado, estadisticas
    
    def _generar_estadisticas(self, texto_original: str, texto_codificado: str, 
                            tiempo_procesamiento: float) -> Dict:
        """
        Genera estadísticas completas de compresión.
        
        Args:
            texto_original: Texto original
            texto_codificado: Texto codificado
            tiempo_procesamiento: Tiempo de procesamiento en segundos
            
        Returns:
            Diccionario con estadísticas detalladas
        """
        if not texto_original:
            return {
                "longitud_original": 0,
                "longitud_comprimida": 0,
                "bits_originales": 0,
                "bits_comprimidos": 0,
                "tasa_compresion": 0,
                "factor_compresion": 0,
                "bits_ahorrados": 0,
                "tiempo_compresion": tiempo_procesamiento
            }
        
        # Cálculos básicos
        longitud_original = len(texto_original)
        longitud_comprimida = len(texto_codificado)
        bits_originales = longitud_original * 8  # ASCII = 8 bits por carácter
        bits_comprimidos = longitud_comprimida
        
        # Métricas de compresión
        tasa_compresion = 0
        factor_compresion = 0
        bits_ahorrados = bits_originales - bits_comprimidos
        
        if bits_originales > 0:
            tasa_compresion = (bits_ahorrados / bits_originales) * 100
            
        if bits_comprimidos > 0:
            factor_compresion = bits_originales / bits_comprimidos
        
        return {
            "longitud_original": longitud_original,
            "longitud_comprimida": longitud_comprimida,
            "bits_originales": bits_originales,
            "bits_comprimidos": bits_comprimidos,
            "tasa_compresion": tasa_compresion,
            "factor_compresion": factor_compresion,
            "bits_ahorrados": bits_ahorrados,
            "tiempo_compresion": tiempo_procesamiento
        }
    
    def validar_integridad(self, texto_original: str, texto_decodificado: str) -> bool:
        """
        Valida la integridad de la compresión/descompresión.
        
        Args:
            texto_original: Texto original
            texto_decodificado: Texto después de comprimir y descomprimir
            
        Returns:
            True si los textos son idénticos
        """
        return texto_original == texto_decodificado
    
    def obtener_eficiencia(self) -> Dict[str, float]:
        """
        Calcula métricas de eficiencia del algoritmo.
        
        Returns:
            Diccionario con métricas de eficiencia
        """
        if not self.estadisticas:
            return {}
        
        stats = self.estadisticas
        
        # Entropía de Shannon (aproximada)
        entropia = self._calcular_entropia_shannon()
        
        # Eficiencia teórica vs práctica
        eficiencia_teorica = entropia / 8 if entropia > 0 else 0
        eficiencia_practica = stats.get("tasa_compresion", 0) / 100
        
        return {
            "entropia_shannon": entropia,
            "eficiencia_teorica": eficiencia_teorica,
            "eficiencia_practica": eficiencia_practica,
            "diferencia_eficiencia": abs(eficiencia_teorica - eficiencia_practica)
        }
    
    def _calcular_entropia_shannon(self) -> float:
        """
        Calcula la entropía de Shannon del texto procesado.
        
        Returns:
            Entropía de Shannon en bits
        """
        # Esta es una implementación simplificada
        # En un proyecto real, se calcularía basado en las frecuencias
        return 0.0  # Placeholder para implementación futura


class UtilitiesCompresion:
    """Utilidades adicionales para análisis de compresión."""
    
    @staticmethod
    def comparar_con_otros_algoritmos(texto: str) -> Dict[str, Dict]:
        """
        Compara la eficiencia de Huffman con otros algoritmos teóricos.
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Diccionario con comparaciones de diferentes algoritmos
        """
        # Implementación simplificada para demostración
        longitud_original = len(texto) * 8
        
        return {
            "huffman": {"bits": 0, "tasa": 0},  # Se llenarían con datos reales
            "lz77_teorico": {"bits": longitud_original * 0.6, "tasa": 40},
            "lzw_teorico": {"bits": longitud_original * 0.7, "tasa": 30},
            "sin_compresion": {"bits": longitud_original, "tasa": 0}
        }
    
    @staticmethod
    def generar_reporte_detallado(estadisticas: Dict) -> str:
        """
        Genera un reporte detallado de las estadísticas de compresión.
        
        Args:
            estadisticas: Diccionario con estadísticas
            
        Returns:
            Reporte formateado como string
        """
        if not estadisticas:
            return "No hay estadísticas disponibles."
        
        reporte = f"""
REPORTE DE COMPRESIÓN HUFFMAN
============================

Datos Originales:
- Longitud del texto: {estadisticas.get('longitud_original', 0)} caracteres
- Bits originales: {estadisticas.get('bits_originales', 0)} bits

Datos Comprimidos:
- Longitud codificada: {estadisticas.get('longitud_comprimida', 0)} bits
- Bits comprimidos: {estadisticas.get('bits_comprimidos', 0)} bits

Métricas de Compresión:
- Tasa de compresión: {estadisticas.get('tasa_compresion', 0):.2f}%
- Factor de compresión: {estadisticas.get('factor_compresion', 0):.2f}x
- Bits ahorrados: {estadisticas.get('bits_ahorrados', 0)} bits

Características del Árbol:
- Altura del árbol: {estadisticas.get('altura', 0)}
- Número de hojas: {estadisticas.get('num_hojas', 0)}
- Nodos internos: {estadisticas.get('num_nodos_internos', 0)}
- Longitud promedio de código: {estadisticas.get('longitud_promedio_codigo', 0):.2f} bits

Rendimiento:
- Tiempo de compresión: {estadisticas.get('tiempo_compresion', 0):.4f} segundos
"""
        return reporte
