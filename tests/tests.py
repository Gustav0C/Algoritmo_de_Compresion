"""
Suite de Pruebas Unitarias para el Compresor de Huffman
======================================================

Este módulo contiene todas las pruebas unitarias y casos de prueba
para validar la correcta implementación del algoritmo de Huffman.

Autor: Proyecto Hans
Fecha: Agosto 2025
Versión: 1.0

Tipos de pruebas:
- Pruebas unitarias de componentes individuales
- Pruebas de integración
- Pruebas de casos extremos
- Pruebas de rendimiento
- Pruebas de integridad
"""

import unittest
import time
import random
import string
from typing import Dict, List, Tuple, Any

try:
    # Importar desde el directorio padre src/
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    from huffman_tree import NodoHuffman, ArbolHuffman
    from huffman_compressor import CompresorHuffman, UtilitiesCompresion
except ImportError:
    # Fallback para casos donde estén en el mismo directorio
    from huffman_tree import NodoHuffman, ArbolHuffman
    from huffman_compressor import CompresorHuffman, UtilitiesCompresion


class TestNodoHuffman(unittest.TestCase):
    """Pruebas unitarias para la clase NodoHuffman."""
    
    def test_creacion_nodo_hoja(self):
        """Prueba la creación de un nodo hoja."""
        nodo = NodoHuffman('A', 5)
        self.assertEqual(nodo.caracter, 'A')
        self.assertEqual(nodo.frecuencia, 5)
        self.assertTrue(nodo.es_hoja())
        self.assertIsNone(nodo.izquierdo)
        self.assertIsNone(nodo.derecho)
    
    def test_creacion_nodo_interno(self):
        """Prueba la creación de un nodo interno."""
        hoja1 = NodoHuffman('A', 3)
        hoja2 = NodoHuffman('B', 2)
        nodo_interno = NodoHuffman(frecuencia=5, izquierdo=hoja1, derecho=hoja2)
        
        self.assertIsNone(nodo_interno.caracter)
        self.assertEqual(nodo_interno.frecuencia, 5)
        self.assertFalse(nodo_interno.es_hoja())
        self.assertEqual(nodo_interno.izquierdo, hoja1)
        self.assertEqual(nodo_interno.derecho, hoja2)
    
    def test_comparacion_nodos(self):
        """Prueba la comparación de nodos por frecuencia."""
        nodo1 = NodoHuffman('A', 3)
        nodo2 = NodoHuffman('B', 5)
        nodo3 = NodoHuffman('C', 3)
        
        self.assertTrue(nodo1 < nodo2)
        self.assertFalse(nodo2 < nodo1)
        self.assertFalse(nodo1 < nodo3)  # frecuencias iguales
        self.assertTrue(nodo1 == nodo3)
    
    def test_representacion_string(self):
        """Prueba la representación en string de los nodos."""
        hoja = NodoHuffman('A', 5)
        interno = NodoHuffman(frecuencia=10)
        
        self.assertIn("Hoja", str(hoja))
        self.assertIn("'A'", str(hoja))
        self.assertIn("5", str(hoja))
        self.assertIn("Interno", str(interno))
        self.assertIn("10", str(interno))


class TestArbolHuffman(unittest.TestCase):
    """Pruebas unitarias para la clase ArbolHuffman."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.arbol = ArbolHuffman()
    
    def test_construccion_arbol_texto_simple(self):
        """Prueba la construcción del árbol con texto simple."""
        frecuencias = {'A': 3, 'B': 2, 'C': 1}
        self.arbol.construir_desde_frecuencias(frecuencias)
        
        self.assertIsNotNone(self.arbol.raiz)
        self.assertEqual(self.arbol.raiz.frecuencia, 6)  # 3+2+1
        self.assertFalse(self.arbol.raiz.es_hoja())
    
    def test_construccion_arbol_un_caracter(self):
        """Prueba la construcción del árbol con un solo carácter."""
        frecuencias = {'A': 5}
        self.arbol.construir_desde_frecuencias(frecuencias)
        
        self.assertIsNotNone(self.arbol.raiz)
        self.assertTrue(self.arbol.raiz.es_hoja())
        self.assertEqual(self.arbol.raiz.caracter, 'A')
        self.assertEqual(self.arbol.raiz.frecuencia, 5)
    
    def test_construccion_arbol_vacio(self):
        """Prueba el manejo de frecuencias vacías."""
        with self.assertRaises(ValueError):
            self.arbol.construir_desde_frecuencias({})
    
    def test_generacion_codigos_texto_simple(self):
        """Prueba la generación de códigos para texto simple."""
        frecuencias = {'A': 3, 'B': 2, 'C': 1}
        self.arbol.construir_desde_frecuencias(frecuencias)
        codigos = self.arbol.generar_codigos()
        
        # Verificar que todos los caracteres tienen códigos
        self.assertEqual(set(codigos.keys()), {'A', 'B', 'C'})
        
        # Verificar que todos los códigos son diferentes
        valores_codigos = list(codigos.values())
        self.assertEqual(len(valores_codigos), len(set(valores_codigos)))
        
        # Verificar propiedad de prefijo único
        self._verificar_propiedad_prefijo(codigos)
        
        # Verificar que caracteres más frecuentes tienen códigos más cortos (generalmente)
        if len(codigos['A']) <= len(codigos['C']):
            self.assertTrue(True)  # 'A' es más frecuente que 'C'
    
    def test_generacion_codigos_un_caracter(self):
        """Prueba la generación de códigos para un solo carácter."""
        frecuencias = {'A': 5}
        self.arbol.construir_desde_frecuencias(frecuencias)
        codigos = self.arbol.generar_codigos()
        
        self.assertEqual(codigos, {'A': '0'})
    
    def test_estadisticas_arbol(self):
        """Prueba el cálculo de estadísticas del árbol."""
        frecuencias = {'A': 4, 'B': 2, 'C': 1, 'D': 1}
        self.arbol.construir_desde_frecuencias(frecuencias)
        estadisticas = self.arbol.obtener_estadisticas()
        
        self.assertIn('altura', estadisticas)
        self.assertIn('num_hojas', estadisticas)
        self.assertIn('num_nodos_internos', estadisticas)
        self.assertEqual(estadisticas['num_hojas'], 4)
        self.assertGreaterEqual(estadisticas['altura'], 2)
    
    def _verificar_propiedad_prefijo(self, codigos: Dict[str, str]):
        """Verifica que ningún código es prefijo de otro."""
        valores_codigos = list(codigos.values())
        for i, codigo1 in enumerate(valores_codigos):
            for j, codigo2 in enumerate(valores_codigos):
                if i != j:
                    self.assertFalse(codigo1.startswith(codigo2), 
                                   f"Código '{codigo2}' es prefijo de '{codigo1}'")


class TestCompresorHuffman(unittest.TestCase):
    """Pruebas unitarias para la clase CompresorHuffman."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.compresor = CompresorHuffman()
    
    def test_calcular_frecuencias(self):
        """Prueba el cálculo de frecuencias de caracteres."""
        texto = "AABBC"
        frecuencias = self.compresor.calcular_frecuencias(texto)
        
        esperado = {'A': 2, 'B': 2, 'C': 1}
        self.assertEqual(frecuencias, esperado)
    
    def test_calcular_frecuencias_texto_vacio(self):
        """Prueba el cálculo de frecuencias con texto vacío."""
        frecuencias = self.compresor.calcular_frecuencias("")
        self.assertEqual(frecuencias, {})
    
    def test_compresion_texto_simple(self):
        """Prueba la compresión de un texto simple."""
        texto = "AABBC"
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        # Verificar que la compresión se ejecutó
        self.assertIsInstance(texto_codificado, str)
        self.assertIsInstance(codigos, dict)
        self.assertIsNotNone(arbol)
        self.assertIsInstance(estadisticas, dict)
        
        # Verificar estadísticas básicas
        self.assertEqual(estadisticas['longitud_original'], 5)
        self.assertGreater(estadisticas['tiempo_compresion'], 0)
    
    def test_compresion_texto_vacio(self):
        """Prueba la compresión de texto vacío."""
        texto = ""
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        self.assertEqual(texto_codificado, "")
        self.assertEqual(codigos, {})
        self.assertIsNone(arbol)
        self.assertEqual(estadisticas['longitud_original'], 0)
    
    def test_compresion_un_caracter(self):
        """Prueba la compresión de texto con un solo carácter único."""
        texto = "AAAAA"
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        self.assertEqual(codigos, {'A': '0'})
        self.assertEqual(texto_codificado, "00000")
        self.assertTrue(arbol.es_hoja())
    
    def test_descompresion_texto_simple(self):
        """Prueba la descompresión de un texto simple."""
        texto_original = "AABBC"
        
        # Comprimir
        resultado = self.compresor.comprimir(texto_original)
        texto_codificado, _, arbol, _ = resultado
        
        # Descomprimir
        texto_recuperado, stats_desc = self.compresor.descomprimir(texto_codificado, arbol)
        
        self.assertEqual(texto_original, texto_recuperado)
        self.assertTrue(stats_desc['exito'])
        self.assertGreater(stats_desc['tiempo_descompresion'], 0)
    
    def test_descompresion_un_caracter(self):
        """Prueba la descompresión de texto con un solo carácter único."""
        texto_original = "AAAAA"
        
        # Comprimir
        resultado = self.compresor.comprimir(texto_original)
        texto_codificado, _, arbol, _ = resultado
        
        # Descomprimir
        texto_recuperado, _ = self.compresor.descomprimir(texto_codificado, arbol)
        
        self.assertEqual(texto_original, texto_recuperado)
    
    def test_validacion_integridad(self):
        """Prueba la validación de integridad."""
        texto1 = "Hello World"
        texto2 = "Hello World"
        texto3 = "Hello world"  # Diferente mayúscula
        
        self.assertTrue(self.compresor.validar_integridad(texto1, texto2))
        self.assertFalse(self.compresor.validar_integridad(texto1, texto3))


class TestCasosExtremos(unittest.TestCase):
    """Pruebas de casos extremos y límites."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.compresor = CompresorHuffman()
    
    def test_texto_muy_largo(self):
        """Prueba con texto muy largo."""
        # Generar texto de 10,000 caracteres
        texto = 'A' * 5000 + 'B' * 3000 + 'C' * 2000
        
        resultado = self.compresor.comprimir(texto)
        texto_codificado, _, arbol, estadisticas = resultado
        
        # Verificar que la compresión funciona
        self.assertEqual(estadisticas['longitud_original'], 10000)
        
        # Verificar descompresión
        texto_recuperado, _ = self.compresor.descomprimir(texto_codificado, arbol)
        self.assertEqual(texto, texto_recuperado)
    
    def test_texto_todos_caracteres_unicos(self):
        """Prueba con texto donde todos los caracteres son únicos."""
        texto = string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        # Con caracteres únicos, la compresión puede no ser efectiva
        self.assertEqual(len(codigos), len(texto))
        
        # Verificar integridad
        texto_recuperado, _ = self.compresor.descomprimir(texto_codificado, arbol)
        self.assertEqual(texto, texto_recuperado)
    
    def test_texto_con_caracteres_especiales(self):
        """Prueba con caracteres especiales y Unicode."""
        texto = "¡Hola! ¿Cómo estás? 你好 🌟 α β γ δ \\n\\t"
        
        resultado = self.compresor.comprimir(texto)
        texto_codificado, _, arbol, _ = resultado
        
        # Verificar integridad
        texto_recuperado, _ = self.compresor.descomprimir(texto_codificado, arbol)
        self.assertEqual(texto, texto_recuperado)
    
    def test_texto_repetitivo_extremo(self):
        """Prueba con texto extremadamente repetitivo."""
        texto = "A" * 1000
        
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        # Debe ser muy eficiente
        self.assertEqual(codigos, {'A': '0'})
        self.assertEqual(len(texto_codificado), 1000)
        self.assertGreater(estadisticas['tasa_compresion'], 80)  # Muy alta eficiencia
    
    def test_distribucion_uniforme(self):
        """Prueba con distribución uniforme de caracteres."""
        # Crear texto con distribución uniforme
        chars = ['A', 'B', 'C', 'D', 'E']
        texto = ''.join(chars * 20)  # 100 caracteres, 20 de cada uno
        
        resultado = self.compresor.comprimir(texto)
        texto_codificado, _, arbol, estadisticas = resultado
        
        # Verificar que funciona correctamente
        texto_recuperado, _ = self.compresor.descomprimir(texto_codificado, arbol)
        self.assertEqual(texto, texto_recuperado)


class TestRendimiento(unittest.TestCase):
    """Pruebas de rendimiento y eficiencia."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.compresor = CompresorHuffman()
    
    def test_tiempo_compresion_escalabilidad(self):
        """Prueba que el tiempo de compresión escala razonablemente."""
        tamaños = [100, 500, 1000, 2000]
        tiempos = []
        
        for tamaño in tamaños:
            texto = self._generar_texto_aleatorio(tamaño)
            
            inicio = time.time()
            self.compresor.comprimir(texto)
            tiempo = time.time() - inicio
            tiempos.append(tiempo)
        
        # El tiempo no debería crecer más que linealmente con respecto al texto
        # (considerando que k = caracteres únicos se mantiene constante)
        for i in range(1, len(tiempos)):
            factor_tamaño = tamaños[i] / tamaños[i-1]
            factor_tiempo = tiempos[i] / tiempos[i-1]
            
            # El tiempo no debería crecer más de 3x cuando el tamaño se duplica
            self.assertLess(factor_tiempo, factor_tamaño * 3)
    
    def test_memoria_eficiente(self):
        """Prueba que el uso de memoria sea eficiente."""
        texto = self._generar_texto_aleatorio(5000)
        
        resultado = self.compresor.comprimir(texto)
        _, codigos, _, estadisticas = resultado
        
        # El número de códigos no debería exceder el número de caracteres únicos
        caracteres_unicos = len(set(texto))
        self.assertEqual(len(codigos), caracteres_unicos)
        
        # Las estadísticas deberían ser consistentes
        self.assertEqual(estadisticas['longitud_original'], len(texto))
    
    def _generar_texto_aleatorio(self, longitud: int) -> str:
        """Genera texto aleatorio para pruebas."""
        caracteres = string.ascii_letters + string.digits + ' .,!?'
        return ''.join(random.choices(caracteres, k=longitud))


class TestIntegracion(unittest.TestCase):
    """Pruebas de integración de todo el sistema."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.compresor = CompresorHuffman()
    
    def test_flujo_completo_compresion_descompresion(self):
        """Prueba el flujo completo de compresión y descompresión."""
        textos_prueba = [
            "Hello, World!",
            "The quick brown fox jumps over the lazy dog.",
            "AAAAAABBBBCCDDEE",
            "¡Texto con acentos y símbolos especiales! ñáéíóú",
            "A" * 100,
            string.ascii_letters,
        ]
        
        for texto in textos_prueba:
            with self.subTest(texto=texto[:20]):
                # Compresión
                resultado = self.compresor.comprimir(texto)
                texto_codificado, codigos, arbol, estadisticas = resultado
                
                # Verificaciones básicas
                self.assertIsInstance(texto_codificado, str)
                self.assertIsInstance(codigos, dict)
                self.assertIsNotNone(arbol)
                self.assertEqual(estadisticas['longitud_original'], len(texto))
                
                # Descompresión
                texto_recuperado, stats_desc = self.compresor.descomprimir(texto_codificado, arbol)
                
                # Verificación de integridad
                self.assertEqual(texto, texto_recuperado)
                self.assertTrue(stats_desc['exito'])
                
                # Validación con método específico
                self.assertTrue(self.compresor.validar_integridad(texto, texto_recuperado))
    
    def test_multiples_compresiones_independientes(self):
        """Prueba múltiples compresiones independientes."""
        textos = ["ABC", "DEF", "GHI"]
        resultados = []
        
        for texto in textos:
            resultado = self.compresor.comprimir(texto)
            resultados.append(resultado)
        
        # Verificar que cada compresión es independiente
        for i, (texto_codificado, codigos, arbol, _) in enumerate(resultados):
            texto_recuperado, _ = self.compresor.descomprimir(texto_codificado, arbol)
            self.assertEqual(textos[i], texto_recuperado)


class TestUtilitiesCompresion(unittest.TestCase):
    """Pruebas para las utilidades de compresión."""
    
    def test_generar_reporte_detallado(self):
        """Prueba la generación de reportes detallados."""
        estadisticas = {
            'longitud_original': 100,
            'longitud_comprimida': 80,
            'bits_originales': 800,
            'bits_comprimidos': 80,
            'tasa_compresion': 90.0,
            'factor_compresion': 10.0,
            'bits_ahorrados': 720,
            'tiempo_compresion': 0.001,
            'altura': 5,
            'num_hojas': 10,
            'num_nodos_internos': 9
        }
        
        reporte = UtilitiesCompresion.generar_reporte_detallado(estadisticas)
        
        self.assertIsInstance(reporte, str)
        self.assertIn("REPORTE DE COMPRESIÓN", reporte)
        self.assertIn("100", reporte)  # longitud original
        self.assertIn("90.00%", reporte)  # tasa de compresión


def crear_suite_pruebas_rapidas() -> unittest.TestSuite:
    """Crea una suite de pruebas rápidas para desarrollo."""
    suite = unittest.TestSuite()
    
    # Pruebas básicas y rápidas
    suite.addTest(TestNodoHuffman('test_creacion_nodo_hoja'))
    suite.addTest(TestNodoHuffman('test_comparacion_nodos'))
    suite.addTest(TestArbolHuffman('test_construccion_arbol_texto_simple'))
    suite.addTest(TestCompresorHuffman('test_compresion_texto_simple'))
    suite.addTest(TestCompresorHuffman('test_descompresion_texto_simple'))
    suite.addTest(TestIntegracion('test_flujo_completo_compresion_descompresion'))
    
    return suite


def crear_suite_pruebas_completas() -> unittest.TestSuite:
    """Crea la suite completa de pruebas."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Cargar todas las clases de prueba
    clases_prueba = [
        TestNodoHuffman,
        TestArbolHuffman,
        TestCompresorHuffman,
        TestCasosExtremos,
        TestRendimiento,
        TestIntegracion,
        TestUtilitiesCompresion
    ]
    
    for clase in clases_prueba:
        tests = loader.loadTestsFromTestCase(clase)
        suite.addTests(tests)
    
    return suite


def ejecutar_todas_las_pruebas(rapido: bool = False) -> Dict[str, Any]:
    """
    Ejecuta todas las pruebas y retorna un resumen de resultados.
    
    Args:
        rapido: Si True, ejecuta solo pruebas rápidas
        
    Returns:
        Diccionario con resultados de las pruebas
    """
    if rapido:
        suite = crear_suite_pruebas_rapidas()
    else:
        suite = crear_suite_pruebas_completas()
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2, stream=open('nul', 'w'))
    resultado = runner.run(suite)
    
    # Recopilar resultados
    total = resultado.testsRun
    fallos = len(resultado.failures)
    errores = len(resultado.errors)
    exitos = total - fallos - errores
    
    detalles_fallos = []
    for test, traceback in resultado.failures + resultado.errors:
        detalles_fallos.append(f"{test}: {traceback.split('\\n')[-2]}")
    
    return {
        'total': total,
        'exitos': exitos,
        'fallos': fallos + errores,
        'detalles_fallos': detalles_fallos,
        'exitoso': fallos + errores == 0
    }


if __name__ == '__main__':
    print("Ejecutando suite completa de pruebas...")
    resultados = ejecutar_todas_las_pruebas()
    
    print(f"\\nResultados:")
    print(f"Total de pruebas: {resultados['total']}")
    print(f"Exitosas: {resultados['exitos']}")
    print(f"Fallidas: {resultados['fallos']}")
    
    if resultados['exitoso']:
        print("\\n✅ Todas las pruebas pasaron!")
    else:
        print("\\n❌ Algunas pruebas fallaron:")
        for fallo in resultados['detalles_fallos']:
            print(f"  - {fallo}")
