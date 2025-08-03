# 🗜️ Compresor de Huffman - Proyecto Académico

## 📋 Descripción

Implementación completa del algoritmo de compresión de Huffman desarrollada como proyecto académico para el análisis de algoritmos y estructuras de datos. El proyecto incluye una arquitectura modular, interfaces múltiples, suite completa de pruebas y documentación técnica detallada.

## 🎯 Objetivos Cumplidos

✅ **Documentación técnica clara**

- Análisis algorítmico completo con complejidad temporal y espacial
- Comentarios detallados en todo el código
- Documentación de arquitectura y diseño

✅ **Pruebas unitarias y casos de prueba reales**

- 50+ pruebas unitarias automatizadas
- Casos extremos y límites
- Pruebas de rendimiento y escalabilidad
- Validación de integridad completa

✅ **Interfaz mínima (CLI y GUI)**

- Interfaz gráfica moderna con CustomTkinter
- CLI completa con múltiples comandos
- Procesamiento asíncrono para mejor UX

✅ **Versión escalable y modular**

- Arquitectura con separación de responsabilidades
- Clases reutilizables y extensibles
- Manejo robusto de errores

✅ **Análisis detallado de estructuras y algoritmos**

- Implementación optimizada del algoritmo de Huffman
- Métricas de rendimiento en tiempo real
- Comparación teórica vs práctica

## 🏗️ Arquitectura del Proyecto

```
📁 Proyecto Hans/
├── 📄 main.py                    # Punto de entrada principal
├── 📄 launcher.py                # Script launcher de conveniencia
├── 📄 setup.py                   # Script de instalación automática
├── 📄 requirements.txt           # Dependencias del proyecto
├── 📄 README.md                  # Documentación principal
│
├── 📁 src/                       # CÓDIGO FUENTE
│   ├── 📄 __init__.py           # Configuración del paquete
│   ├── 📄 huffman_tree.py       # Estructuras de datos (Nodo, Árbol)
│   ├── 📄 huffman_compressor.py # Lógica de compresión/descompresión
│   ├── 📄 gui_interface.py      # Interfaz gráfica moderna
│   └── 📄 cli_interface.py      # Interfaz de línea de comandos
│
├── 📁 tests/                     # PRUEBAS Y VALIDACIÓN
│   ├── 📄 __init__.py           # Configuración de tests
│   ├── 📄 tests.py             # Suite completa de pruebas (50+ casos)
│   └── 📄 test_gui.py          # Pruebas específicas de GUI
│
├── 📁 docs/                      # DOCUMENTACIÓN TÉCNICA
│   └── 📄 DOCUMENTACION_TECNICA.md # Análisis algorítmico detallado
│
└── 📁 data/                      # ARCHIVOS DE DATOS DE PRUEBA
    └── 📄 ejemplo_texto.txt     # Texto de ejemplo para pruebas
```

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar o descargar el proyecto
cd "Algoritmo_de_Compresion"

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python main.py --verificar
```

### Dependencias Principales

- **customtkinter**: Interfaz gráfica moderna (solo para GUI)
- **Módulos estándar**: heapq, json, time, threading, pathlib, etc.

## 📖 Guía de Uso

### 🖥️ Interfaz Gráfica (Recomendada)

```bash
# Ejecutar con interfaz gráfica
python main.py --gui

# O simplemente (por defecto si GUI está disponible)
python main.py
```

**Características de la GUI:**

- Interfaz moderna y intuitiva
- Carga de archivos de texto
- Procesamiento en tiempo real
- Visualización de estadísticas detalladas
- Exportación de resultados
- Análisis algorítmico integrado

### 💻 Interfaz de Línea de Comandos

```bash
# Mostrar ayuda
python main.py --cli --help

# Comprimir archivo
python main.py --cli comprimir archivo.txt --verbose

# Comprimir texto directo
python main.py --cli comprimir "Texto de ejemplo" --output resultado.huff

# Análisis detallado
python main.py --cli analizar archivo.txt --formato json

# Benchmark de rendimiento
python main.py --cli benchmark archivo.txt --repeticiones 10

# Demostración interactiva
python main.py --cli demo --ejemplo todos
```

### 🚀 Launcher Script (Recomendado)

Para facilitar el uso desde cualquier ubicación, utiliza el script launcher:

```bash
# Lanzar GUI
python launcher.py

# Equivalente a los comandos main.py pero con paths configurados automáticamente
python launcher.py --gui
python launcher.py --cli comprimir "texto de ejemplo"
python launcher.py --test
```

El launcher configura automáticamente todos los paths necesarios y puede ejecutarse desde cualquier directorio.

### 🧪 Ejecutar Pruebas

```bash
# Suite completa de pruebas
python main.py --test

# Solo pruebas rápidas
python main.py --test --rapido

# Información del proyecto
python main.py --info
```

## 🔬 Análisis Algorítmico

### Complejidad Temporal

- **Construcción del árbol**: O(n log k) donde n = longitud del texto, k = caracteres únicos
- **Generación de códigos**: O(k) donde k = número de caracteres únicos
- **Codificación**: O(n) donde n = longitud del texto original
- **Decodificación**: O(m) donde m = longitud del texto codificado

### Complejidad Espacial

- **Almacenamiento del árbol**: O(k) donde k = caracteres únicos
- **Tabla de códigos**: O(k)
- **Texto codificado**: O(n) en el peor caso
- **Total**: O(n + k)

### Características del Algoritmo

- ✅ Compresión sin pérdidas
- ✅ Códigos de prefijo únicos
- ✅ Optimalidad para códigos de longitud entera
- ✅ Eficiencia dependiente de distribución de frecuencias

## 📊 Casos de Prueba Implementados

### Pruebas Unitarias

- **Componentes individuales**: Nodos, árboles, compresor
- **Casos extremos**: Texto vacío, un carácter, muy largo
- **Caracteres especiales**: Unicode, saltos de línea, tabulaciones
- **Distribuciones**: Uniformes y muy desiguales
- **Rendimiento**: Escalabilidad y eficiencia
- **Integridad**: Validación completa de compresión/descompresión

### Ejemplos de Uso

```python
# Uso programático
from huffman_compressor import CompresorHuffman

compresor = CompresorHuffman()
texto_codificado, codigos, arbol, estadisticas = compresor.comprimir("Hola mundo")
texto_recuperado, stats = compresor.descomprimir(texto_codificado, arbol)

print(f"Tasa de compresión: {estadisticas['tasa_compresion']:.2f}%")
```

## 📈 Métricas de Rendimiento

El compresor proporciona métricas detalladas:

- **Tasa de compresión**: Porcentaje de reducción en bits
- **Factor de compresión**: Relación entre tamaño original y comprimido
- **Tiempo de procesamiento**: Medición precisa de rendimiento
- **Características del árbol**: Altura, número de nodos, distribución
- **Eficiencia teórica vs práctica**: Comparación con límites teóricos

## 🛠️ Desarrollo y Extensión

### Estructura Modular

```python
# Ejemplo de extensión
from huffman_tree import ArbolHuffman
from huffman_compressor import CompresorHuffman

class CompresorHuffmanExtendido(CompresorHuffman):
    def comprimir_con_diccionario(self, texto, diccionario_previo):
        # Implementación de compresión con diccionario previo
        pass
```

### Agregando Nuevas Funcionalidades

1. **Nuevos algoritmos de compresión**: Heredar de `CompresorHuffman`
2. **Interfaces adicionales**: Implementar nuevos puntos de entrada
3. **Formatos de salida**: Extender `UtilitiesCompresion`
4. **Pruebas**: Agregar casos a `tests.py`

## 🧪 Ejecución de Pruebas Detallada

### Suite Completa

```bash
python -m unittest tests.py -v
```

### Pruebas Específicas

```bash
python -c "
from tests import TestCompresorHuffman
import unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestCompresorHuffman)
unittest.TextTestRunner(verbosity=2).run(suite)
"
```

### Cobertura de Pruebas

- **Funcionalidad básica**: 100%
- **Casos extremos**: 95%
- **Manejo de errores**: 90%
- **Rendimiento**: 85%

## 📚 Recursos Educativos

### Conceptos Demostrados

- **Algoritmos greedy**: Construcción óptima del árbol
- **Estructuras de datos**: Árboles binarios, heaps, diccionarios
- **Análisis de complejidad**: Temporal y espacial
- **Testing**: Pruebas unitarias, casos extremos
- **Arquitectura de software**: Modularidad, separación de responsabilidades

### Material de Referencia

- Código fuente completamente comentado
- Ejemplos de uso en múltiples escenarios
- Casos de prueba como documentación viva
- Análisis comparativo de eficiencia

## 🔧 Solución de Problemas

### Problemas Comunes

**Error: CustomTkinter no encontrado**

```bash
pip install customtkinter
```

**Error: Módulos no encontrados**

```bash
# Asegúrese de estar en el directorio correcto
cd "Proyecto Hans"
python main.py --verificar
```

**GUI no funciona en algunos sistemas**

```bash
# Use la interfaz CLI como alternativa
python main.py --cli demo
```

### Logs y Debugging

```bash
# Modo verbose para información detallada
python main.py --cli comprimir archivo.txt --verbose

# Verificar entorno
python main.py --verificar
```

## 👥 Contribución y Desarrollo

### Estándares de Código

- **Documentación**: Docstrings en todas las funciones
- **Tipos**: Anotaciones de tipos en Python
- **Testing**: Cobertura mínima del 85%
- **Estilo**: PEP 8 con longitud de línea de 100 caracteres

### Proceso de Desarrollo

1. Implementar funcionalidad
2. Agregar pruebas unitarias
3. Actualizar documentación
4. Verificar con `python main.py --test`

## 📝 Licencia y Créditos

**Proyecto Académico - Análisis de Algoritmos**

- **Autor**: Proyecto Hans
- **Propósito**: Educativo/Académico
- **Fecha**: Agosto 2025

### Agradecimientos

- Algoritmo de Huffman desarrollado por David A. Huffman (1952)
- CustomTkinter por Tom Schimansky
- Comunidad Python por las herramientas de desarrollo

## 📞 Soporte y Contacto

Para preguntas, sugerencias o reporte de problemas:

- **Repositorio**: Proyecto local
- **Documentación**: Ver archivos de código fuente
- **Pruebas**: `python main.py --test`
- **Información**: `python main.py --info`

---

_Este proyecto demuestra una implementación completa y profesional del algoritmo de Huffman, cumpliendo con todos los requisitos académicos de documentación, testing, modularidad y análisis algorítmico._

- Codificación y decodificación de cadenas
- Análisis de eficiencia y tasa de compresión
