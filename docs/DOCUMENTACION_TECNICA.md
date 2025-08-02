"""
Documentación Técnica del Compresor de Huffman
=============================================

ANÁLISIS ALGORÍTMICO DETALLADO
==============================

1. INTRODUCCIÓN
--------------

El algoritmo de compresión de Huffman es un método de compresión sin pérdidas 
desarrollado por David A. Huffman en 1952. Se basa en la creación de códigos 
de longitud variable para caracteres, donde los caracteres más frecuentes 
reciben códigos más cortos.

2. COMPLEJIDAD ALGORÍTMICA
--------------------------

2.1 Complejidad Temporal
------------------------

Fase de Análisis:
- Cálculo de frecuencias: O(n)
  donde n = longitud del texto de entrada

Fase de Construcción:
- Creación del heap inicial: O(k)
- Construcción del árbol: O(k log k)
  donde k = número de caracteres únicos

Fase de Codificación:
- Generación de códigos: O(k)
- Codificación del texto: O(n)

Fase de Decodificación:
- Decodificación: O(m)
  donde m = longitud del texto codificado

COMPLEJIDAD TOTAL: O(n + k log k)

En el caso promedio, k << n, por lo que la complejidad se aproxima a O(n).

2.2 Complejidad Espacial
-------------------------

- Tabla de frecuencias: O(k)
- Heap para construcción: O(k)
- Árbol de Huffman: O(k) nodos
- Tabla de códigos: O(k)
- Texto codificado: O(n) en el peor caso

COMPLEJIDAD ESPACIAL TOTAL: O(n + k)

3. ESTRUCTURAS DE DATOS UTILIZADAS
----------------------------------

3.1 Nodo de Huffman
-------------------
```python
class NodoHuffman:
    - caracter: str | None
    - frecuencia: int
    - izquierdo: NodoHuffman | None
    - derecho: NodoHuffman | None
```

Invariantes:
- Los nodos hoja contienen caracteres (caracter != None)
- Los nodos internos no contienen caracteres (caracter == None)
- La frecuencia de un nodo interno es la suma de sus hijos

3.2 Árbol Binario de Huffman
----------------------------
- Árbol binario completo donde cada hoja representa un carácter
- Caminos desde la raíz hasta las hojas definen los códigos
- Propiedad de prefijo: ningún código es prefijo de otro

3.3 Min-Heap (Cola de Prioridad)
--------------------------------
- Utilizado para seleccionar eficientemente los nodos con menor frecuencia
- Operaciones principales: insert O(log k), extract-min O(log k)
- Implementado usando el módulo heapq de Python

4. ANÁLISIS DE CASOS
--------------------

4.1 Mejor Caso
--------------
- Texto con distribución muy desigual de caracteres
- Un carácter muy frecuente, otros muy raros
- Ejemplo: "AAAAAAABC" → alta compresión

Complejidad: O(n) (k es muy pequeño)
Eficiencia: Hasta 87.5% de compresión

4.2 Caso Promedio
-----------------
- Distribución natural de caracteres (texto en lenguaje natural)
- Sigue aproximadamente la ley de Zipf
- Ejemplo: Texto en español o inglés

Complejidad: O(n + k log k) donde k ≈ 26-100
Eficiencia: 20-60% de compresión típica

4.3 Peor Caso
-------------
- Distribución uniforme de caracteres
- Todos los caracteres aparecen con la misma frecuencia
- Ejemplo: "ABCDEFGHIJKLMNOP" (cada letra una vez)

Complejidad: O(n + k log k) donde k ≈ n
Eficiencia: Puede expandir el texto (códigos más largos que 8 bits)

5. OPTIMIZACIONES IMPLEMENTADAS
-------------------------------

5.1 Optimización de Memoria
---------------------------
- Uso de generators donde es posible
- Liberación temprana de objetos temporales
- Compartir referencias en lugar de copiar

5.2 Optimización de Tiempo
--------------------------
- Uso de Counter() para frecuencias (implementado en C)
- Heap operations nativas de Python
- Evitar recursión excesiva en árboles grandes

5.3 Casos Especiales Optimizados
--------------------------------
- Texto vacío: retorno inmediato
- Un solo carácter: código fijo "0"
- Validación temprana de entrada inválida

6. MÉTRICAS DE RENDIMIENTO
--------------------------

6.1 Métricas de Compresión
-------------------------
- Tasa de compresión = (1 - bits_comprimidos/bits_originales) × 100%
- Factor de compresión = bits_originales / bits_comprimidos
- Bits ahorrados = bits_originales - bits_comprimidos

6.2 Métricas de Calidad del Árbol
---------------------------------
- Altura del árbol: indicador de eficiencia de códigos
- Longitud promedio de código
- Distribución de longitudes de códigos

6.3 Métricas de Rendimiento
---------------------------
- Tiempo de compresión por carácter
- Tiempo de descompresión por bit
- Memoria utilizada por carácter único

7. COMPARACIÓN CON OTROS ALGORITMOS
-----------------------------------

7.1 vs. Códigos de Longitud Fija (ASCII)
----------------------------------------
- ASCII: 8 bits por carácter (fijo)
- Huffman: Variable, optimizado por frecuencia
- Ventaja: Huffman adapta al contenido

7.2 vs. Algoritmos Modernos
---------------------------
- LZ77/LZ78: Mejor para patrones repetitivos
- DEFLATE: Combina Huffman + LZ77
- Huffman: Optimal para códigos de símbolo único

8. CASOS DE PRUEBA CRÍTICOS
---------------------------

8.1 Casos Extremos
------------------
```
- Texto vacío: ""
- Un carácter: "A"
- Dos caracteres: "AB"
- Muy repetitivo: "A" × 1000
- Uniforme: "ABCDEFGH" × 100
```

8.2 Casos Reales
----------------
```
- Código fuente (Python, JavaScript)
- Texto natural (español, inglés)
- Datos estructurados (JSON, XML)
- Caracteres especiales y Unicode
```

8.3 Validaciones de Integridad
------------------------------
- Propiedad de prefijo en códigos
- Reconstrucción exacta del texto original
- Consistencia de frecuencias
- Validez de la estructura del árbol

9. LÍMITES TEÓRICOS
-------------------

9.1 Límite de Shannon
--------------------
La entropía de Shannon define el límite teórico inferior para la compresión:

H(X) = -∑ p(x) log₂ p(x)

donde p(x) es la probabilidad del carácter x.

9.2 Eficiencia de Huffman
-------------------------
- Huffman es optimal para códigos de longitud entera
- Puede estar hasta 1 bit por símbolo por encima del límite de Shannon
- En la práctica, muy cerca del óptimo teórico

10. ANÁLISIS DE ESTABILIDAD
---------------------------

10.1 Sensibilidad a Entrada
---------------------------
- Pequeños cambios en frecuencias pueden cambiar el árbol completamente
- El algoritmo es determinístico para una entrada dada
- Orden de construcción puede afectar la forma del árbol (pero no la optimalidad)

10.2 Escalabilidad
------------------
- Lineal en longitud del texto: O(n)
- Logarítmica en vocabulario: O(k log k)
- Memoria proporcional al vocabulario: O(k)

11. CONCLUSIONES
---------------

El algoritmo de Huffman implementado demuestra:

✅ Optimalidad teórica para códigos de prefijo
✅ Eficiencia práctica en casos comunes
✅ Robustez en casos extremos
✅ Escalabilidad apropiada
✅ Implementación correcta y completa

El análisis de complejidad confirma que la implementación cumple con las
expectativas teóricas, y las pruebas validan la correctitud en todos los
casos considerados.

REFERENCIAS
-----------
- Huffman, D. A. (1952). "A Method for the Construction of Minimum-Redundancy Codes"
- Cormen, T. et al. "Introduction to Algorithms" (Sección sobre códigos de Huffman)
- Salomon, D. "Data Compression: The Complete Reference"
"""
