"""
Interfaz Gráfica para el Compresor de Huffman
============================================

Este módulo implementa una interfaz gráfica moderna utilizando CustomTkinter
para el compresor de Huffman.

Autor: Gustav0C
Fecha: Agosto 2025
Versión: 1.0
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
from typing import Dict, Optional

try:
    from .huffman_compressor import CompresorHuffman, UtilitiesCompresion
except ImportError:
    from huffman_compressor import CompresorHuffman, UtilitiesCompresion


class InterfazHuffman:
    """
    Interfaz gráfica principal para el compresor de Huffman.
    
    Proporciona una interfaz moderna y fácil de usar para realizar
    compresión y descompresión de texto utilizando el algoritmo de Huffman.
    
    Características:
    - Interfaz moderna con CustomTkinter
    - Procesamiento en hilos separados
    - Visualización de estadísticas detalladas
    - Carga y guardado de archivos
    - Validación de integridad
    """
    
    def __init__(self):
        """Inicializa la interfaz gráfica."""
        self.compresor = CompresorHuffman()
        self.texto_original = ""
        self.texto_codificado = ""
        self.arbol = None
        self.codigos = {}
        self.estadisticas_actuales = {}
        
        self._configurar_tema()
        self._setup_gui()
    
    def _configurar_tema(self):
        """Configura el tema visual de la aplicación."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def _setup_gui(self):
        """Configura la interfaz gráfica completa."""
        self.ventana = ctk.CTk()
        self.ventana.title("Compresor de Huffman - Proyecto Hans")
        self.ventana.geometry("1200x800")
        self.ventana.resizable(True, True)
        
        # Frame principal con scroll
        self.frame_principal = ctk.CTkScrollableFrame(self.ventana)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Componentes de la interfaz
        self._crear_titulo()
        self._crear_seccion_entrada()
        self._crear_seccion_botones()
        self._crear_seccion_resultados()
        self._crear_seccion_estadisticas()
        self._crear_seccion_analisis()
    
    def _crear_titulo(self):
        """Crea el título principal de la aplicación."""
        frame_titulo = ctk.CTkFrame(self.frame_principal)
        frame_titulo.pack(fill="x", pady=(0, 20))
        
        self.titulo = ctk.CTkLabel(
            frame_titulo,
            text="🗜️ Compresor de Texto - Algoritmo de Huffman",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.titulo.pack(pady=20)
        
        self.subtitulo = ctk.CTkLabel(
            frame_titulo,
            text="Implementación completa con análisis algorítmico y pruebas",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subtitulo.pack(pady=(0, 20))
    
    def _crear_seccion_entrada(self):
        """Crea la sección de entrada de texto."""
        frame_entrada = ctk.CTkFrame(self.frame_principal)
        frame_entrada.pack(fill="x", pady=(0, 20))
        
        # Título de sección
        label_seccion = ctk.CTkLabel(
            frame_entrada,
            text="📝 Entrada de Datos",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_seccion.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Área de texto
        label_entrada = ctk.CTkLabel(
            frame_entrada,
            text="Texto a comprimir:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_entrada.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.texto_entrada = ctk.CTkTextbox(
            frame_entrada,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.texto_entrada.pack(fill="x", padx=20, pady=(5, 15))
        
        # Agregar texto placeholder manualmente
        self.texto_entrada.insert("1.0", "Ingrese aquí el texto que desea comprimir...")
        self.texto_entrada.configure(text_color="gray")
        
        # Botones de carga
        frame_botones_carga = ctk.CTkFrame(frame_entrada)
        frame_botones_carga.pack(fill="x", padx=20, pady=(0, 20))
        
        self.btn_cargar = ctk.CTkButton(
            frame_botones_carga,
            text="📁 Cargar Archivo",
            command=self.cargar_archivo,
            font=ctk.CTkFont(size=12),
            width=150
        )
        self.btn_cargar.pack(side="left", padx=(10, 5), pady=10)
        
        self.btn_ejemplo = ctk.CTkButton(
            frame_botones_carga,
            text="📋 Texto de Ejemplo",
            command=self.cargar_ejemplo,
            font=ctk.CTkFont(size=12),
            width=150
        )
        self.btn_ejemplo.pack(side="left", padx=5, pady=10)
        
        self.btn_guardar = ctk.CTkButton(
            frame_botones_carga,
            text="💾 Guardar Resultado",
            command=self.guardar_resultado,
            font=ctk.CTkFont(size=12),
            width=150,
            state="disabled"
        )
        self.btn_guardar.pack(side="right", padx=(5, 10), pady=10)
    
    def _crear_seccion_botones(self):
        """Crea la sección de botones principales."""
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", pady=(0, 20))
        
        # Título de sección
        label_seccion = ctk.CTkLabel(
            frame_botones,
            text="⚙️ Operaciones",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_seccion.pack(pady=(20, 15))
        
        # Frame interno para botones
        frame_botones_interno = ctk.CTkFrame(frame_botones)
        frame_botones_interno.pack(fill="x", padx=20, pady=(0, 20))
        
        self.btn_comprimir = ctk.CTkButton(
            frame_botones_interno,
            text="🗜️ Comprimir Texto",
            command=self.comprimir_texto,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#2b5aa0"
        )
        self.btn_comprimir.pack(side="left", padx=(20, 10), pady=15, expand=True, fill="x")
        
        self.btn_descomprimir = ctk.CTkButton(
            frame_botones_interno,
            text="📤 Descomprimir",
            command=self.descomprimir_texto,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            state="disabled",
            fg_color="#0d7377"
        )
        self.btn_descomprimir.pack(side="left", padx=10, pady=15, expand=True, fill="x")
        
        self.btn_analizar = ctk.CTkButton(
            frame_botones_interno,
            text="📊 Análisis Detallado",
            command=self.mostrar_analisis_detallado,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            state="disabled",
            fg_color="#7209b7"
        )
        self.btn_analizar.pack(side="left", padx=10, pady=15, expand=True, fill="x")
        
        self.btn_limpiar = ctk.CTkButton(
            frame_botones_interno,
            text="🗑️ Limpiar Todo",
            command=self.limpiar_todo,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#dc2626"
        )
        self.btn_limpiar.pack(side="right", padx=(10, 20), pady=15)
    
    def _crear_seccion_resultados(self):
        """Crea la sección de resultados con pestañas."""
        frame_resultados = ctk.CTkFrame(self.frame_principal)
        frame_resultados.pack(fill="both", expand=True, pady=(0, 20))
        
        # Título de sección
        label_seccion = ctk.CTkLabel(
            frame_resultados,
            text="📋 Resultados",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_seccion.pack(pady=(20, 15))
        
        # Pestañas
        self.tabview = ctk.CTkTabview(frame_resultados, height=300)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Pestaña de texto codificado
        self.tab_codificado = self.tabview.add("🔢 Texto Codificado")
        self.texto_codificado_widget = ctk.CTkTextbox(
            self.tab_codificado,
            font=ctk.CTkFont(family="Courier", size=10),
            state="disabled"
        )
        self.texto_codificado_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de códigos
        self.tab_codigos = self.tabview.add("🗂️ Tabla de Códigos")
        self.tabla_codigos = ctk.CTkTextbox(
            self.tab_codigos,
            font=ctk.CTkFont(family="Courier", size=11),
            state="disabled"
        )
        self.tabla_codigos.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de texto descomprimido
        self.tab_descomprimido = self.tabview.add("📤 Texto Recuperado")
        self.texto_descomprimido = ctk.CTkTextbox(
            self.tab_descomprimido,
            font=ctk.CTkFont(size=12),
            state="disabled"
        )
        self.texto_descomprimido.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _crear_seccion_estadisticas(self):
        """Crea la sección de estadísticas."""
        frame_stats = ctk.CTkFrame(self.frame_principal)
        frame_stats.pack(fill="x", pady=(0, 20))
        
        # Título de sección
        label_seccion = ctk.CTkLabel(
            frame_stats,
            text="📊 Estadísticas de Compresión",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_seccion.pack(pady=(20, 15))
        
        # Grid de estadísticas
        stats_grid = ctk.CTkFrame(frame_stats)
        stats_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Configurar grid
        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Fila 1
        self.label_tasa = ctk.CTkLabel(
            stats_grid, 
            text="Tasa de Compresión: --",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.label_tasa.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        self.label_factor = ctk.CTkLabel(
            stats_grid, 
            text="Factor de Compresión: --",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.label_factor.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        self.label_ahorro = ctk.CTkLabel(
            stats_grid, 
            text="Bits Ahorrados: --",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.label_ahorro.grid(row=0, column=2, padx=15, pady=10, sticky="w")
        
        # Fila 2
        self.label_tiempo = ctk.CTkLabel(
            stats_grid, 
            text="Tiempo de Procesamiento: --",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.label_tiempo.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        
        self.label_eficiencia = ctk.CTkLabel(
            stats_grid, 
            text="Eficiencia del Árbol: --",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.label_eficiencia.grid(row=1, column=1, padx=15, pady=10, sticky="w")
        
        self.label_integridad = ctk.CTkLabel(
            stats_grid, 
            text="Integridad: --",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.label_integridad.grid(row=1, column=2, padx=15, pady=10, sticky="w")
    
    def _crear_seccion_analisis(self):
        """Crea la sección de análisis avanzado."""
        self.frame_analisis = ctk.CTkFrame(self.frame_principal)
        self.frame_analisis.pack(fill="x", pady=(0, 20))
        
        # Título de sección
        label_seccion = ctk.CTkLabel(
            self.frame_analisis,
            text="🔬 Análisis Algorítmico",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_seccion.pack(pady=(20, 15))
        
        # Área de análisis
        self.texto_analisis = ctk.CTkTextbox(
            self.frame_analisis,
            height=200,
            font=ctk.CTkFont(family="Courier", size=11),
            state="disabled"
        )
        self.texto_analisis.pack(fill="x", padx=20, pady=(0, 20))
    
    def cargar_archivo(self):
        """Carga texto desde un archivo."""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos Python", "*.py"),
                ("Archivos de código", "*.js *.html *.css *.json"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.texto_entrada.delete("1.0", "end")
                self.texto_entrada.insert("1.0", contenido)
                messagebox.showinfo("Éxito", f"Archivo cargado exitosamente.\nCaracteres: {len(contenido)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def cargar_ejemplo(self):
        """Carga un texto de ejemplo para pruebas."""
        ejemplo = """¡Hola! Este es un ejemplo de texto para demostrar el algoritmo de compresión de Huffman.

El algoritmo de Huffman es un método de compresión sin pérdidas que asigna códigos de longitud variable a los caracteres, donde los caracteres más frecuentes reciben códigos más cortos.

Este algoritmo fue desarrollado por David A. Huffman en 1952 mientras era estudiante de posgrado en el MIT. Es ampliamente utilizado en formatos de compresión como ZIP, GZIP, JPEG y muchos otros.

Características principales:
- Compresión sin pérdidas
- Códigos de prefijo únicos
- Optimalidad garantizada para códigos de longitud entera
- Eficiencia O(n log n) en construcción del árbol

¿Sabías que la eficiencia de la compresión de Huffman depende directamente de la distribución de frecuencias de los caracteres en el texto? Textos con distribuciones más desiguales tienden a comprimirse mejor.

Ejemplo de frecuencias:
AAAAAABBBBCCDDEE

En este caso, 'A' aparece 6 veces, 'B' 4 veces, 'C' 2 veces, 'D' 2 veces y 'E' 2 veces.
El algoritmo asignará códigos más cortos a 'A' y 'B', resultando en una mejor compresión."""
        
        self.texto_entrada.delete("1.0", "end")
        self.texto_entrada.insert("1.0", ejemplo)
        messagebox.showinfo("Ejemplo Cargado", "Se ha cargado un texto de ejemplo para demostración.")
    
    def comprimir_texto(self):
        """Comprime el texto ingresado."""
        texto = self.texto_entrada.get("1.0", "end-1c")
        
        if not texto.strip():
            messagebox.showwarning("Advertencia", "Por favor, ingrese algún texto para comprimir.")
            return
        
        self._deshabilitar_botones()
        self.btn_comprimir.configure(text="🔄 Comprimiendo...")
        
        def proceso_compresion():
            try:
                # Comprimir
                self.texto_original = texto
                resultado = self.compresor.comprimir(texto)
                self.texto_codificado, self.codigos, self.arbol, self.estadisticas_actuales = resultado
                
                # Actualizar interfaz en el hilo principal
                self.ventana.after(0, self._mostrar_resultados_compresion)
                
            except Exception as e:
                error_msg = f"Error durante la compresión:\n{str(e)}"
                self.ventana.after(0, lambda: messagebox.showerror("Error", error_msg))
                self.ventana.after(0, self._habilitar_botones)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=proceso_compresion)
        thread.daemon = True
        thread.start()
    
    def _mostrar_resultados_compresion(self):
        """Muestra los resultados de la compresión en la interfaz."""
        # Mostrar texto codificado
        self.texto_codificado_widget.configure(state="normal")
        self.texto_codificado_widget.delete("1.0", "end")
        
        # Agregar información adicional
        info_header = f"Longitud: {len(self.texto_codificado)} bits\n"
        info_header += f"Texto original: {len(self.texto_original)} caracteres\n"
        info_header += "-" * 50 + "\n"
        
        self.texto_codificado_widget.insert("1.0", info_header + self.texto_codificado)
        self.texto_codificado_widget.configure(state="disabled")
        
        # Mostrar tabla de códigos
        self._mostrar_tabla_codigos()
        
        # Actualizar estadísticas
        self._actualizar_estadisticas()
        
        # Habilitar botones
        self.btn_descomprimir.configure(state="normal")
        self.btn_analizar.configure(state="normal")
        self.btn_guardar.configure(state="normal")
        self._habilitar_botones()
        
        messagebox.showinfo("Éxito", "¡Texto comprimido exitosamente!")
    
    def _mostrar_tabla_codigos(self):
        """Muestra la tabla de códigos de Huffman."""
        self.tabla_codigos.configure(state="normal")
        self.tabla_codigos.delete("1.0", "end")
        
        # Encabezado de la tabla
        tabla_texto = "TABLA DE CÓDIGOS DE HUFFMAN\n"
        tabla_texto += "=" * 40 + "\n"
        tabla_texto += f"{'Carácter':<12} | {'Código':<15} | {'Frecuencia'}\n"
        tabla_texto += "-" * 40 + "\n"
        
        # Calcular frecuencias para mostrar
        frecuencias = self.compresor.calcular_frecuencias(self.texto_original)
        
        # Ordenar por frecuencia (más frecuentes primero)
        items_ordenados = sorted(self.codigos.items(), 
                               key=lambda x: frecuencias.get(x[0], 0), 
                               reverse=True)
        
        for caracter, codigo in items_ordenados:
            freq = frecuencias.get(caracter, 0)
            
            # Formatear caracteres especiales
            if caracter == '\n':
                char_display = '\\n'
            elif caracter == '\t':
                char_display = '\\t'
            elif caracter == ' ':
                char_display = 'ESPACIO'
            else:
                char_display = caracter
            
            tabla_texto += f"{char_display:<12} | {codigo:<15} | {freq}\n"
        
        # Estadísticas adicionales
        tabla_texto += "\n" + "=" * 40 + "\n"
        tabla_texto += f"Total de caracteres únicos: {len(self.codigos)}\n"
        tabla_texto += f"Código más corto: {min(len(c) for c in self.codigos.values())} bits\n"
        tabla_texto += f"Código más largo: {max(len(c) for c in self.codigos.values())} bits\n"
        
        self.tabla_codigos.insert("1.0", tabla_texto)
        self.tabla_codigos.configure(state="disabled")
    
    def _actualizar_estadisticas(self):
        """Actualiza las etiquetas de estadísticas."""
        stats = self.estadisticas_actuales
        
        tasa = stats.get('tasa_compresion', 0)
        factor = stats.get('factor_compresion', 0)
        ahorro = stats.get('bits_ahorrados', 0)
        tiempo = stats.get('tiempo_compresion', 0)
        altura = stats.get('altura', 0)
        
        self.label_tasa.configure(text=f"Tasa de Compresión: {tasa:.2f}%")
        self.label_factor.configure(text=f"Factor de Compresión: {factor:.2f}x")
        self.label_ahorro.configure(text=f"Bits Ahorrados: {ahorro}")
        self.label_tiempo.configure(text=f"Tiempo: {tiempo:.4f}s")
        self.label_eficiencia.configure(text=f"Altura del Árbol: {altura}")
        self.label_integridad.configure(text="Integridad: Pendiente")
    
    def descomprimir_texto(self):
        """Descomprime el texto codificado."""
        if not self.texto_codificado or not self.arbol:
            messagebox.showwarning("Advertencia", "Primero debe comprimir un texto.")
            return
        
        self._deshabilitar_botones()
        self.btn_descomprimir.configure(text="🔄 Descomprimiendo...")
        
        def proceso_descompresion():
            try:
                # Descomprimir
                texto_recuperado, stats_descomp = self.compresor.descomprimir(
                    self.texto_codificado, self.arbol
                )
                
                # Validar integridad
                integridad_ok = self.compresor.validar_integridad(
                    self.texto_original, texto_recuperado
                )
                
                # Actualizar interfaz
                self.ventana.after(0, lambda: self._mostrar_resultados_descompresion(
                    texto_recuperado, stats_descomp, integridad_ok
                ))
                
            except Exception as e:
                error_msg = f"Error durante la descompresión:\n{str(e)}"
                self.ventana.after(0, lambda: messagebox.showerror("Error", error_msg))
                self.ventana.after(0, self._habilitar_botones)
        
        thread = threading.Thread(target=proceso_descompresion)
        thread.daemon = True
        thread.start()
    
    def _mostrar_resultados_descompresion(self, texto_recuperado, stats_descomp, integridad_ok):
        """Muestra los resultados de la descompresión."""
        # Mostrar texto descomprimido
        self.texto_descomprimido.configure(state="normal")
        self.texto_descomprimido.delete("1.0", "end")
        
        # Agregar información del resultado
        info_header = f"Longitud recuperada: {len(texto_recuperado)} caracteres\n"
        info_header += f"Tiempo de descompresión: {stats_descomp.get('tiempo_descompresion', 0):.4f}s\n"
        info_header += f"Integridad: {'✅ CORRECTA' if integridad_ok else '❌ ERROR'}\n"
        info_header += "-" * 50 + "\n"
        
        self.texto_descomprimido.insert("1.0", info_header + texto_recuperado)
        self.texto_descomprimido.configure(state="disabled")
        
        # Actualizar estado de integridad
        integridad_texto = "✅ Correcta" if integridad_ok else "❌ Error"
        self.label_integridad.configure(text=f"Integridad: {integridad_texto}")
        
        # Mostrar mensaje
        if integridad_ok:
            tiempo = stats_descomp.get('tiempo_descompresion', 0)
            mensaje = f"¡Descompresión exitosa!\nTiempo: {tiempo:.4f}s\n✅ La integridad del texto se mantuvo."
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", "❌ Error: El texto descomprimido no coincide con el original.")
        
        self._habilitar_botones()
    
    def mostrar_analisis_detallado(self):
        """Muestra un análisis algorítmico detallado."""
        if not self.estadisticas_actuales:
            messagebox.showwarning("Advertencia", "Primero debe comprimir un texto.")
            return
        
        # Generar reporte detallado
        reporte = UtilitiesCompresion.generar_reporte_detallado(self.estadisticas_actuales)
        
        # Agregar análisis de complejidad
        analisis_adicional = self._generar_analisis_complejidad()
        reporte_completo = reporte + "\n" + analisis_adicional
        
        # Mostrar en el área de análisis
        self.texto_analisis.configure(state="normal")
        self.texto_analisis.delete("1.0", "end")
        self.texto_analisis.insert("1.0", reporte_completo)
        self.texto_analisis.configure(state="disabled")
        
        messagebox.showinfo("Análisis Generado", "Se ha generado el análisis algorítmico detallado.")
    
    def _generar_analisis_complejidad(self):
        """Genera análisis de complejidad algorítmica."""
        stats = self.estadisticas_actuales
        n = stats.get('longitud_original', 0)
        k = stats.get('num_hojas', 0)
        
        analisis = f"""
ANÁLISIS DE COMPLEJIDAD ALGORÍTMICA
===================================

Parámetros de entrada:
- n = {n} (longitud del texto)
- k = {k} (caracteres únicos)

Complejidad Temporal:
- Cálculo de frecuencias: O(n)
- Construcción del heap: O(k)
- Construcción del árbol: O(k log k)
- Generación de códigos: O(k)
- Codificación del texto: O(n)
- Total: O(n + k log k)

Complejidad Espacial:
- Almacenamiento del texto: O(n)
- Tabla de frecuencias: O(k)
- Árbol de Huffman: O(k)
- Tabla de códigos: O(k)
- Texto codificado: O(n) en el peor caso
- Total: O(n + k)

Análisis de Eficiencia:
- Caso ideal: Texto con distribución muy desigual
- Caso peor: Texto con distribución uniforme
- Eficiencia actual: {stats.get('tasa_compresion', 0):.2f}%

Comparación con ASCII:
- Bits por carácter (ASCII): 8
- Bits por carácter (Huffman): {stats.get('bits_comprimidos', 1) / max(stats.get('longitud_original', 1), 1):.2f}
- Reducción: {8 - (stats.get('bits_comprimidos', 1) / max(stats.get('longitud_original', 1), 1)):.2f} bits/carácter
"""
        return analisis
    
    def guardar_resultado(self):
        """Guarda los resultados en un archivo."""
        if not self.texto_codificado:
            messagebox.showwarning("Advertencia", "No hay resultados para guardar.")
            return
        
        archivo = filedialog.asksaveasfilename(
            title="Guardar resultados",
            defaultextension=".txt",
            filetypes=[
                ("Archivo de texto", "*.txt"),
                ("Archivo JSON", "*.json"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            try:
                # Preparar contenido
                contenido = f"""RESULTADOS DE COMPRESIÓN HUFFMAN
================================

TEXTO ORIGINAL:
{self.texto_original}

TEXTO CODIFICADO:
{self.texto_codificado}

{UtilitiesCompresion.generar_reporte_detallado(self.estadisticas_actuales)}

TABLA DE CÓDIGOS:
"""
                for char, code in sorted(self.codigos.items()):
                    char_display = repr(char) if char in ['\n', '\t', ' '] else char
                    contenido += f"{char_display}: {code}\n"
                
                # Guardar archivo
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                messagebox.showinfo("Éxito", f"Resultados guardados en:\n{archivo}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    def limpiar_todo(self):
        """Limpia todos los campos y reinicia la aplicación."""
        self.texto_entrada.delete("1.0", "end")
        
        # Limpiar todas las áreas de resultado
        for widget in [self.texto_codificado_widget, self.tabla_codigos, 
                      self.texto_descomprimido, self.texto_analisis]:
            widget.configure(state="normal")
            widget.delete("1.0", "end")
            widget.configure(state="disabled")
        
        # Resetear estadísticas
        self.label_tasa.configure(text="Tasa de Compresión: --")
        self.label_factor.configure(text="Factor de Compresión: --")
        self.label_ahorro.configure(text="Bits Ahorrados: --")
        self.label_tiempo.configure(text="Tiempo: --")
        self.label_eficiencia.configure(text="Eficiencia del Árbol: --")
        self.label_integridad.configure(text="Integridad: --")
        
        # Resetear variables
        self.texto_original = ""
        self.texto_codificado = ""
        self.arbol = None
        self.codigos = {}
        self.estadisticas_actuales = {}
        
        # Resetear estado de botones
        self.btn_descomprimir.configure(state="disabled")
        self.btn_analizar.configure(state="disabled")
        self.btn_guardar.configure(state="disabled")
        self._habilitar_botones()
        
        messagebox.showinfo("Limpieza Completa", "Todos los datos han sido limpiados.")
    
    def _deshabilitar_botones(self):
        """Deshabilita todos los botones durante el procesamiento."""
        self.btn_comprimir.configure(state="disabled")
        self.btn_descomprimir.configure(state="disabled")
        self.btn_analizar.configure(state="disabled")
    
    def _habilitar_botones(self):
        """Habilita los botones después del procesamiento."""
        self.btn_comprimir.configure(state="normal", text="🗜️ Comprimir Texto")
        self.btn_descomprimir.configure(text="📤 Descomprimir")
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.ventana.mainloop()


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas."""
    try:
        import customtkinter
        return True
    except ImportError:
        print("Error: customtkinter no está instalado.")
        print("Instálalo con: pip install customtkinter")
        return False
