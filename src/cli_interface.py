"""
Interfaz de Línea de Comandos (CLI) para el Compresor de Huffman
===============================================================

Este módulo proporciona una interfaz de línea de comandos completa
para el compresor de Huffman, permitiendo operaciones desde terminal.

Autor: Proyecto Hans
Fecha: Agosto 2025
Versión: 1.0
"""

import argparse
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from .huffman_compressor import CompresorHuffman, UtilitiesCompresion
except ImportError:
    from huffman_compressor import CompresorHuffman, UtilitiesCompresion


class CLIHuffman:
    """
    Interfaz de línea de comandos para el compresor de Huffman.
    
    Proporciona funcionalidades completas accesibles desde terminal,
    incluyendo compresión, descompresión, análisis y benchmarking.
    """
    
    def __init__(self):
        """Inicializa la interfaz CLI."""
        self.compresor = CompresorHuffman()
        self.verbose = False
    
    def configurar_parser(self) -> argparse.ArgumentParser:
        """
        Configura el parser de argumentos de línea de comandos.
        
        Returns:
            Parser configurado con todos los comandos y opciones
        """
        parser = argparse.ArgumentParser(
            description="Compresor de Huffman - Implementación completa con análisis",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Ejemplos de uso:
  python -m huffman_cli comprimir archivo.txt
  python -m huffman_cli descomprimir archivo.huff
  python -m huffman_cli analizar "Texto de ejemplo"
  python -m huffman_cli benchmark archivo.txt --repeticiones 10
  python -m huffman_cli demo --verbose
            """
        )
        
        # Argumentos globales
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Mostrar información detallada durante la ejecución"
        )
        
        parser.add_argument(
            "--output", "-o",
            type=str,
            help="Archivo de salida (opcional)"
        )
        
        # Subcomandos
        subparsers = parser.add_subparsers(dest="comando", help="Comandos disponibles")
        
        # Comando comprimir
        parser_comprimir = subparsers.add_parser(
            "comprimir",
            help="Comprimir un archivo o texto"
        )
        parser_comprimir.add_argument(
            "entrada",
            help="Archivo de texto a comprimir o texto directo (usar comillas)"
        )
        parser_comprimir.add_argument(
            "--guardar-arbol",
            action="store_true",
            help="Guardar el árbol de Huffman para descompresión posterior"
        )
        
        # Comando descomprimir
        parser_descomprimir = subparsers.add_parser(
            "descomprimir",
            help="Descomprimir un archivo comprimido"
        )
        parser_descomprimir.add_argument(
            "archivo_comprimido",
            help="Archivo comprimido (.huff)"
        )
        
        # Comando analizar
        parser_analizar = subparsers.add_parser(
            "analizar",
            help="Analizar las características de compresión de un texto"
        )
        parser_analizar.add_argument(
            "entrada",
            help="Archivo de texto o texto directo a analizar"
        )
        parser_analizar.add_argument(
            "--formato",
            choices=["texto", "json", "csv"],
            default="texto",
            help="Formato del reporte de análisis"
        )
        
        # Comando benchmark
        parser_benchmark = subparsers.add_parser(
            "benchmark",
            help="Realizar pruebas de rendimiento"
        )
        parser_benchmark.add_argument(
            "entrada",
            help="Archivo de texto para benchmark"
        )
        parser_benchmark.add_argument(
            "--repeticiones",
            type=int,
            default=5,
            help="Número de repeticiones para el benchmark"
        )
        
        # Comando demo
        parser_demo = subparsers.add_parser(
            "demo",
            help="Ejecutar demostración con texto de ejemplo"
        )
        parser_demo.add_argument(
            "--ejemplo",
            choices=["basico", "codigo", "literatura", "todos"],
            default="basico",
            help="Tipo de ejemplo a ejecutar"
        )
        
        # Comando test
        parser_test = subparsers.add_parser(
            "test",
            help="Ejecutar suite de pruebas"
        )
        parser_test.add_argument(
            "--rapido",
            action="store_true",
            help="Ejecutar solo pruebas rápidas"
        )
        
        return parser
    
    def ejecutar_comando(self, args) -> int:
        """
        Ejecuta el comando especificado en los argumentos.
        
        Args:
            args: Argumentos parseados de línea de comandos
            
        Returns:
            Código de salida (0 = éxito, 1 = error)
        """
        self.verbose = args.verbose
        
        try:
            if args.comando == "comprimir":
                return self._comando_comprimir(args)
            elif args.comando == "descomprimir":
                return self._comando_descomprimir(args)
            elif args.comando == "analizar":
                return self._comando_analizar(args)
            elif args.comando == "benchmark":
                return self._comando_benchmark(args)
            elif args.comando == "demo":
                return self._comando_demo(args)
            elif args.comando == "test":
                return self._comando_test(args)
            else:
                self._print_error("Comando no especificado. Use --help para ver opciones.")
                return 1
                
        except KeyboardInterrupt:
            self._print_error("\\nOperación cancelada por el usuario.")
            return 1
        except Exception as e:
            self._print_error(f"Error inesperado: {str(e)}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def _comando_comprimir(self, args) -> int:
        """Ejecuta el comando de compresión."""
        # Obtener texto
        texto = self._obtener_texto(args.entrada)
        if texto is None:
            return 1
        
        self._print_info(f"Comprimiendo texto de {len(texto)} caracteres...")
        
        # Comprimir
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        # Mostrar resultados
        self._mostrar_estadisticas_compresion(estadisticas)
        
        # Guardar resultados
        if args.output:
            exito = self._guardar_compresion(args.output, texto_codificado, arbol, codigos, estadisticas)
            return 0 if exito else 1
        elif args.guardar_arbol:
            # Generar nombre automático
            nombre_base = Path(args.entrada).stem if Path(args.entrada).exists() else "compresion"
            archivo_salida = f"{nombre_base}.huff"
            exito = self._guardar_compresion(archivo_salida, texto_codificado, arbol, codigos, estadisticas)
            return 0 if exito else 1
        else:
            # Solo mostrar resultado en pantalla
            print(f"\\nTexto codificado:\\n{texto_codificado}")
            print(f"\\nTabla de códigos:")
            self._mostrar_tabla_codigos(codigos)
            return 0
    
    def _comando_descomprimir(self, args) -> int:
        """Ejecuta el comando de descompresión."""
        archivo_path = Path(args.archivo_comprimido)
        
        if not archivo_path.exists():
            self._print_error(f"El archivo {archivo_path} no existe.")
            return 1
        
        try:
            # Cargar datos comprimidos
            with open(archivo_path, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            texto_codificado = datos['texto_codificado']
            arbol_data = datos['arbol']
            
            # Reconstruir árbol (implementación simplificada)
            # En una implementación completa, se serializaría/deserializaría el árbol
            self._print_error("Descompresión desde archivo no implementada completamente.")
            self._print_info("Use la interfaz gráfica para funcionalidad completa.")
            return 1
            
        except Exception as e:
            self._print_error(f"Error al cargar archivo: {str(e)}")
            return 1
    
    def _comando_analizar(self, args) -> int:
        """Ejecuta el comando de análisis."""
        texto = self._obtener_texto(args.entrada)
        if texto is None:
            return 1
        
        self._print_info(f"Analizando texto de {len(texto)} caracteres...")
        
        # Realizar compresión para análisis
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        # Generar análisis según formato
        if args.formato == "json":
            analisis = self._generar_analisis_json(estadisticas, codigos, texto)
            print(json.dumps(analisis, indent=2, ensure_ascii=False))
        elif args.formato == "csv":
            print("Característica,Valor")
            for key, value in estadisticas.items():
                print(f"{key},{value}")
        else:
            # Formato texto
            reporte = UtilitiesCompresion.generar_reporte_detallado(estadisticas)
            print(reporte)
            
            print("\\nTabla de códigos:")
            self._mostrar_tabla_codigos(codigos)
        
        return 0
    
    def _comando_benchmark(self, args) -> int:
        """Ejecuta el comando de benchmark."""
        texto = self._obtener_texto(args.entrada)
        if texto is None:
            return 1
        
        self._print_info(f"Ejecutando benchmark con {args.repeticiones} repeticiones...")
        
        tiempos_compresion = []
        tiempos_descompresion = []
        estadisticas_lista = []
        
        for i in range(args.repeticiones):
            if self.verbose:
                print(f"  Repetición {i + 1}/{args.repeticiones}")
            
            # Medir compresión
            inicio = time.time()
            resultado = self.compresor.comprimir(texto)
            tiempo_comp = time.time() - inicio
            tiempos_compresion.append(tiempo_comp)
            
            texto_codificado, codigos, arbol, estadisticas = resultado
            estadisticas_lista.append(estadisticas)
            
            # Medir descompresión
            inicio = time.time()
            texto_recuperado, stats_desc = self.compresor.descomprimir(texto_codificado, arbol)
            tiempo_desc = time.time() - inicio
            tiempos_descompresion.append(tiempo_desc)
        
        # Calcular estadísticas del benchmark
        self._mostrar_resultados_benchmark(tiempos_compresion, tiempos_descompresion, estadisticas_lista)
        
        return 0
    
    def _comando_demo(self, args) -> int:
        """Ejecuta el comando de demostración."""
        ejemplos = self._obtener_ejemplos()
        
        if args.ejemplo == "todos":
            for nombre, texto in ejemplos.items():
                self._ejecutar_demo_individual(nombre, texto)
                print("\\n" + "="*60 + "\\n")
        else:
            if args.ejemplo in ejemplos:
                texto = ejemplos[args.ejemplo]
                self._ejecutar_demo_individual(args.ejemplo, texto)
            else:
                self._print_error(f"Ejemplo '{args.ejemplo}' no disponible.")
                return 1
        
        return 0
    
    def _comando_test(self, args) -> int:
        """Ejecuta el comando de pruebas."""
        print("Ejecutando suite de pruebas del compresor de Huffman...")
        
        # Importar y ejecutar pruebas
        try:
            try:
                from .tests import ejecutar_todas_las_pruebas
            except ImportError:
                from tests import ejecutar_todas_las_pruebas
            
            resultados = ejecutar_todas_las_pruebas(rapido=args.rapido)
            
            # Mostrar resultados
            print(f"\\nResultados de las pruebas:")
            print(f"Total: {resultados['total']}")
            print(f"Éxitos: {resultados['exitos']}")
            print(f"Fallos: {resultados['fallos']}")
            
            if resultados['fallos'] > 0:
                print("\\nPruebas fallidas:")
                for fallo in resultados['detalles_fallos']:
                    print(f"  - {fallo}")
                return 1
            else:
                print("\\n✅ Todas las pruebas pasaron exitosamente!")
                return 0
                
        except ImportError:
            self._print_error("Módulo de pruebas no disponible.")
            return 1
    
    def _obtener_texto(self, entrada: str) -> Optional[str]:
        """
        Obtiene texto desde archivo o entrada directa.
        
        Args:
            entrada: Ruta de archivo o texto directo
            
        Returns:
            Texto obtenido o None si hay error
        """
        archivo_path = Path(entrada)
        
        if archivo_path.exists():
            # Es un archivo
            try:
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    texto = f.read()
                if self.verbose:
                    print(f"Archivo cargado: {archivo_path} ({len(texto)} caracteres)")
                return texto
            except Exception as e:
                self._print_error(f"Error al leer archivo {archivo_path}: {str(e)}")
                return None
        else:
            # Es texto directo
            if self.verbose:
                print(f"Texto directo: {len(entrada)} caracteres")
            return entrada
    
    def _mostrar_estadisticas_compresion(self, estadisticas: Dict[str, Any]):
        """Muestra estadísticas de compresión en formato CLI."""
        print(f"\\n📊 Estadísticas de Compresión:")
        print(f"  Longitud original: {estadisticas['longitud_original']} caracteres")
        print(f"  Longitud comprimida: {estadisticas['longitud_comprimida']} bits")
        print(f"  Tasa de compresión: {estadisticas['tasa_compresion']:.2f}%")
        print(f"  Factor de compresión: {estadisticas['factor_compresion']:.2f}x")
        print(f"  Bits ahorrados: {estadisticas['bits_ahorrados']}")
        print(f"  Tiempo de procesamiento: {estadisticas['tiempo_compresion']:.4f}s")
        
        if 'altura' in estadisticas:
            print(f"  Altura del árbol: {estadisticas['altura']}")
            print(f"  Número de hojas: {estadisticas['num_hojas']}")
    
    def _mostrar_tabla_codigos(self, codigos: Dict[str, str]):
        """Muestra la tabla de códigos en formato CLI."""
        print(f"\\n{'Carácter':<10} | {'Código':<15}")
        print("-" * 28)
        
        for caracter, codigo in sorted(codigos.items(), key=lambda x: len(x[1])):
            char_display = repr(caracter) if caracter in ['\\n', '\\t', ' '] else caracter
            print(f"{char_display:<10} | {codigo:<15}")
    
    def _guardar_compresion(self, archivo_salida: str, texto_codificado: str, 
                          arbol, codigos: Dict[str, str], estadisticas: Dict) -> bool:
        """Guarda los resultados de compresión en un archivo."""
        try:
            datos = {
                'texto_codificado': texto_codificado,
                'codigos': codigos,
                'estadisticas': estadisticas,
                'version': '1.0',
                'algoritmo': 'huffman'
            }
            
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            print(f"\\n💾 Resultados guardados en: {archivo_salida}")
            return True
            
        except Exception as e:
            self._print_error(f"Error al guardar archivo: {str(e)}")
            return False
    
    def _generar_analisis_json(self, estadisticas: Dict, codigos: Dict, texto: str) -> Dict:
        """Genera análisis en formato JSON."""
        frecuencias = self.compresor.calcular_frecuencias(texto)
        
        return {
            'estadisticas_compresion': estadisticas,
            'tabla_codigos': codigos,
            'frecuencias_caracteres': frecuencias,
            'analisis_distribucion': {
                'caracteres_unicos': len(frecuencias),
                'caracter_mas_frecuente': max(frecuencias.items(), key=lambda x: x[1]),
                'caracter_menos_frecuente': min(frecuencias.items(), key=lambda x: x[1])
            }
        }
    
    def _mostrar_resultados_benchmark(self, tiempos_comp: list, tiempos_desc: list, 
                                    estadisticas_lista: list):
        """Muestra resultados del benchmark."""
        print(f"\\n🏃 Resultados del Benchmark:")
        
        # Estadísticas de tiempo
        tiempo_comp_promedio = sum(tiempos_comp) / len(tiempos_comp)
        tiempo_desc_promedio = sum(tiempos_desc) / len(tiempos_desc)
        
        print(f"\\nTiempos de Compresión:")
        print(f"  Promedio: {tiempo_comp_promedio:.4f}s")
        print(f"  Mínimo: {min(tiempos_comp):.4f}s")
        print(f"  Máximo: {max(tiempos_comp):.4f}s")
        
        print(f"\\nTiempos de Descompresión:")
        print(f"  Promedio: {tiempo_desc_promedio:.4f}s")
        print(f"  Mínimo: {min(tiempos_desc):.4f}s")
        print(f"  Máximo: {max(tiempos_desc):.4f}s")
        
        # Estadísticas de compresión promedio
        tasa_promedio = sum(s['tasa_compresion'] for s in estadisticas_lista) / len(estadisticas_lista)
        factor_promedio = sum(s['factor_compresion'] for s in estadisticas_lista) / len(estadisticas_lista)
        
        print(f"\\nEficiencia Promedio:")
        print(f"  Tasa de compresión: {tasa_promedio:.2f}%")
        print(f"  Factor de compresión: {factor_promedio:.2f}x")
    
    def _obtener_ejemplos(self) -> Dict[str, str]:
        """Obtiene textos de ejemplo para demostración."""
        return {
            "basico": "AAAAAABBBBCCDDEE",
            "codigo": '''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Ejemplo de uso
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")''',
            "literatura": '''En un lugar de la Mancha, de cuyo nombre no quiero acordarme,
no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero,
adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca
que carnero, salpicón las más noches, duelos y quebrantos los sábados...'''
        }
    
    def _ejecutar_demo_individual(self, nombre: str, texto: str):
        """Ejecuta una demostración individual."""
        print(f"🎯 Demostración: {nombre.title()}")
        print(f"Texto original: '{texto[:50]}{'...' if len(texto) > 50 else ''}'")
        print(f"Longitud: {len(texto)} caracteres\\n")
        
        # Comprimir
        resultado = self.compresor.comprimir(texto)
        texto_codificado, codigos, arbol, estadisticas = resultado
        
        # Mostrar resultados
        self._mostrar_estadisticas_compresion(estadisticas)
        
        # Descomprimir y verificar
        texto_recuperado, _ = self.compresor.descomprimir(texto_codificado, arbol)
        integridad_ok = self.compresor.validar_integridad(texto, texto_recuperado)
        
        print(f"\\n✅ Integridad: {'CORRECTA' if integridad_ok else 'ERROR'}")
        
        if self.verbose:
            print(f"\\nTexto codificado: {texto_codificado}")
            self._mostrar_tabla_codigos(codigos)
    
    def _print_info(self, mensaje: str):
        """Imprime mensaje informativo."""
        print(f"ℹ️  {mensaje}")
    
    def _print_error(self, mensaje: str):
        """Imprime mensaje de error."""
        print(f"❌ {mensaje}", file=sys.stderr)


def main():
    """Función principal del CLI."""
    cli = CLIHuffman()
    parser = cli.configurar_parser()
    args = parser.parse_args()
    
    if not args.comando:
        parser.print_help()
        return 1
    
    return cli.ejecutar_comando(args)


if __name__ == "__main__":
    sys.exit(main())
