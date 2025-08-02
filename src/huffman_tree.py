"""
Módulo de Estructuras de Datos para el Algoritmo de Huffman
==========================================================

Este módulo contiene las clases fundamentales para la implementación
del algoritmo de compresión de Huffman.

Autor: Proyecto Hans
Fecha: Agosto 2025
Versión: 1.0

Complejidad Temporal:
- Construcción del árbol: O(n log n) donde n es el número de caracteres únicos
- Generación de códigos: O(n) donde n es el número de nodos en el árbol

Complejidad Espacial:
- O(n) para almacenar el árbol y los códigos
"""

import heapq
from collections import Counter
from typing import Optional, Dict, Any


class NodoHuffman:
    """
    Nodo del árbol binario de Huffman.
    
    Representa tanto nodos internos como hojas del árbol de Huffman.
    Los nodos hoja contienen caracteres, mientras que los nodos internos
    solo contienen la frecuencia acumulada.
    
    Atributos:
        caracter (str, optional): Carácter almacenado (solo en hojas)
        frecuencia (int): Frecuencia del carácter o suma de frecuencias
        izquierdo (NodoHuffman, optional): Hijo izquierdo
        derecho (NodoHuffman, optional): Hijo derecho
    """
    
    def __init__(self, caracter: Optional[str] = None, frecuencia: int = 0, 
                 izquierdo: Optional['NodoHuffman'] = None, 
                 derecho: Optional['NodoHuffman'] = None):
        """
        Inicializa un nodo del árbol de Huffman.
        
        Args:
            caracter: Carácter a almacenar (None para nodos internos)
            frecuencia: Frecuencia del carácter o suma de frecuencias
            izquierdo: Nodo hijo izquierdo
            derecho: Nodo hijo derecho
        """
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierdo = izquierdo
        self.derecho = derecho
    
    def __lt__(self, otro: 'NodoHuffman') -> bool:
        """
        Operador de comparación para la cola de prioridad.
        
        Args:
            otro: Otro nodo a comparar
            
        Returns:
            True si este nodo tiene menor frecuencia
        """
        return self.frecuencia < otro.frecuencia
    
    def __eq__(self, otro: 'NodoHuffman') -> bool:
        """Operador de igualdad basado en frecuencia."""
        return self.frecuencia == otro.frecuencia
    
    def es_hoja(self) -> bool:
        """
        Determina si el nodo es una hoja.
        
        Returns:
            True si el nodo es una hoja (contiene un carácter)
        """
        return self.caracter is not None
    
    def __repr__(self) -> str:
        """Representación en cadena del nodo para debugging."""
        if self.es_hoja():
            return f"Hoja('{self.caracter}': {self.frecuencia})"
        else:
            return f"Interno({self.frecuencia})"


class ArbolHuffman:
    """
    Árbol de Huffman para codificación y decodificación.
    
    Esta clase maneja la construcción del árbol de Huffman basado en
    las frecuencias de caracteres, y proporciona métodos para generar
    códigos de Huffman y realizar la codificación/decodificación.
    
    Atributos:
        raiz (NodoHuffman): Nodo raíz del árbol
        codigos (Dict[str, str]): Mapeo de caracteres a códigos binarios
    """
    
    def __init__(self):
        """Inicializa un árbol de Huffman vacío."""
        self.raiz: Optional[NodoHuffman] = None
        self.codigos: Dict[str, str] = {}
    
    def construir_desde_frecuencias(self, frecuencias: Dict[str, int]) -> None:
        """
        Construye el árbol de Huffman a partir de frecuencias de caracteres.
        
        Utiliza un min-heap para construir el árbol de manera eficiente.
        
        Args:
            frecuencias: Diccionario con caracteres como claves y frecuencias como valores
            
        Complejidad Temporal: O(n log n) donde n = número de caracteres únicos
        Complejidad Espacial: O(n)
        """
        if not frecuencias:
            raise ValueError("No se pueden construir árboles con frecuencias vacías")
        
        if len(frecuencias) == 1:
            # Caso especial: solo un carácter único
            caracter = list(frecuencias.keys())[0]
            self.raiz = NodoHuffman(caracter, frecuencias[caracter])
            return
        
        # Crear cola de prioridad (min heap)
        heap = []
        for caracter, frecuencia in frecuencias.items():
            nodo = NodoHuffman(caracter, frecuencia)
            heapq.heappush(heap, nodo)
        
        # Construir árbol combinando nodos de menor frecuencia
        while len(heap) > 1:
            # Extraer los dos nodos con menor frecuencia
            izquierdo = heapq.heappop(heap)
            derecho = heapq.heappop(heap)
            
            # Crear nodo padre con la suma de frecuencias
            padre = NodoHuffman(
                frecuencia=izquierdo.frecuencia + derecho.frecuencia,
                izquierdo=izquierdo,
                derecho=derecho
            )
            
            # Insertar el nodo padre de vuelta al heap
            heapq.heappush(heap, padre)
        
        # El último nodo en el heap es la raíz
        self.raiz = heap[0]
    
    def generar_codigos(self) -> Dict[str, str]:
        """
        Genera los códigos de Huffman para todos los caracteres.
        
        Realiza un recorrido en profundidad del árbol para asignar
        códigos binarios. El recorrido hacia la izquierda agrega '0'
        y hacia la derecha agrega '1'.
        
        Returns:
            Diccionario con caracteres como claves y códigos binarios como valores
            
        Complejidad Temporal: O(n) donde n = número de nodos
        Complejidad Espacial: O(h) donde h = altura del árbol
        """
        if not self.raiz:
            return {}
        
        self.codigos = {}
        
        # Caso especial: solo un carácter
        if self.raiz.es_hoja():
            self.codigos[self.raiz.caracter] = "0"
            return self.codigos
        
        # Recorrido recursivo para generar códigos
        self._generar_codigos_recursivo(self.raiz, "")
        return self.codigos
    
    def _generar_codigos_recursivo(self, nodo: NodoHuffman, codigo: str) -> None:
        """
        Método auxiliar recursivo para generar códigos.
        
        Args:
            nodo: Nodo actual del árbol
            codigo: Código binario acumulado hasta este nodo
        """
        if nodo.es_hoja():
            self.codigos[nodo.caracter] = codigo
            return
        
        if nodo.izquierdo:
            self._generar_codigos_recursivo(nodo.izquierdo, codigo + "0")
        if nodo.derecho:
            self._generar_codigos_recursivo(nodo.derecho, codigo + "1")
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del árbol construido.
        
        Returns:
            Diccionario con estadísticas como altura, número de nodos, etc.
        """
        if not self.raiz:
            return {}
        
        return {
            "altura": self._calcular_altura(self.raiz),
            "num_hojas": self._contar_hojas(self.raiz),
            "num_nodos_internos": self._contar_nodos_internos(self.raiz),
            "longitud_promedio_codigo": self._calcular_longitud_promedio()
        }
    
    def _calcular_altura(self, nodo: NodoHuffman) -> int:
        """Calcula la altura del árbol."""
        if not nodo or nodo.es_hoja():
            return 0
        
        altura_izq = self._calcular_altura(nodo.izquierdo) if nodo.izquierdo else 0
        altura_der = self._calcular_altura(nodo.derecho) if nodo.derecho else 0
        
        return 1 + max(altura_izq, altura_der)
    
    def _contar_hojas(self, nodo: NodoHuffman) -> int:
        """Cuenta el número de hojas en el árbol."""
        if not nodo:
            return 0
        if nodo.es_hoja():
            return 1
        
        return (self._contar_hojas(nodo.izquierdo) + 
                self._contar_hojas(nodo.derecho))
    
    def _contar_nodos_internos(self, nodo: NodoHuffman) -> int:
        """Cuenta el número de nodos internos."""
        if not nodo or nodo.es_hoja():
            return 0
        
        return (1 + self._contar_nodos_internos(nodo.izquierdo) + 
                self._contar_nodos_internos(nodo.derecho))
    
    def _calcular_longitud_promedio(self) -> float:
        """Calcula la longitud promedio de los códigos."""
        if not self.codigos:
            return 0.0
        
        total_longitud = sum(len(codigo) for codigo in self.codigos.values())
        return total_longitud / len(self.codigos)
