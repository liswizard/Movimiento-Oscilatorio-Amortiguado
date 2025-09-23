#!/usr/bin/env python3
# -- coding: utf-8 --
"""
Script de visualización para el oscilador amortiguado
Genera gráficas de posición, velocidad y energía vs tiempo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import sys

# =============================================================================
# CONFIGURACIÓN DE ESTILO PARA GRÁFICAS PROFESIONALES
# =============================================================================

# Configurar estilo de matplotlib para gráficas científicas
plt.style.use('seaborn-v0_8-whitegrid')
rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.figsize': (10, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.format': 'png'
})

# =============================================================================
# PARÁMETROS Y CONFIGURACIÓN
# =============================================================================

# Valores de coeficientes de fricción (consistentes con Fortran)
VALORES_B = [0.50, 2.00, 3.00]

# Configuración de estilos para cada régimen
CONFIG_GRAFICAS = {
    'colores': ['#1f77b4', '#2ca02c', '#d62728'],  # Azul, verde, rojo
    'estilos': ['-', '--', '-.'],
    'marcadores': ['o', 's', '^'],
    'ancho_linea': 2.5,
    'tamaño_marcador': 4
}

# Configuración de nombres de archivos
ARCHIVOS_ENTRADA = [f"resultados_b{b:.2f}.dat" for b in VALORES_B]

# =============================================================================
# FUNCIONES DE CARGA Y PROCESAMIENTO DE DATOS
# =============================================================================

def cargar_datos(nombre_archivo):
    """
    Carga datos desde archivo generado por Fortran
    
    Parameters:
    nombre_archivo (str): Ruta al archivo de datos
    
    Returns:
    tuple: (tiempo, posicion, velocidad, energia) como arrays de numpy
    """
    try:
        # Saltar líneas de comentario (que empiezan con #)
        with open(nombre_archivo, 'r') as f:
            lineas = [linea for linea in f if not linea.startswith('#')]
        
        # Cargar datos numéricos
        datos = np.loadtxt(lineas)
        
        if datos.shape[1] != 4:
            raise ValueError(f"Archivo {nombre_archivo} no tiene 4 columnas")
        
        tiempo, posicion, velocidad, energia = datos.T
        return tiempo, posicion, velocidad, energia
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {nombre_archivo}")
        print("Asegúrese de ejecutar primero el programa Fortran")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar {nombre_archivo}: {e}")
        sys.exit(1)

def calcular_energia_disipada(tiempo, velocidad, b):
    """
    Calcula la energía disipada por integración numérica
    
    Parameters:
    tiempo (array): Array de tiempos
    velocidad (array): Array de velocidades
    b (float): Coeficiente de fricción
    
    Returns:
    float: Energía disipada calculada
    """
    # Usar regla del trapecio para integración numérica
    integral_v2 = np.trapz(velocidad**2, tiempo)
    energia_disipada = b * integral_v2
    return energia_disipada

# =============================================================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def graficar_posicion_vs_tiempo():
    """Genera gráfica de posición vs tiempo para los tres regímenes"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for i, (b, archivo) in enumerate(zip(VALORES_B, ARCHIVOS_ENTRADA)):
        # Cargar datos
        t, x, v, E = cargar_datos(archivo)
        
        # Crear gráfica
        ax.plot(t, x, 
                label=f'$b = {b}$ kg/s', 
                color=CONFIG_GRAFICAS['colores'][i],
                linestyle=CONFIG_GRAFICAS['estilos'][i],
                linewidth=CONFIG_GRAFICAS['ancho_linea'])
    
    # Configurar gráfica
    ax.set_xlabel('Tiempo (s)', fontweight='bold')
    ax.set_ylabel('Posición (m)', fontweight='bold')
    ax.set_title('Evolución Temporal de la Posición del Oscilador Amortiguado', 
                 fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Añadir anotaciones
    ax.text(0.02, 0.98, 'Subamortiguado → Crítico → Sobreamortiguado', 
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Guardar gráfica
    plt.tight_layout()
    plt.savefig('posicion_vs_tiempo.png', dpi=300)
    plt.show()
    
    print("✓ Gráfica de posición vs tiempo generada: posicion_vs_tiempo.png")

def graficar_velocidad_vs_tiempo():
    """Genera gráfica de velocidad vs tiempo para los tres regímenes"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for i, (b, archivo) in enumerate(zip(VALORES_B, ARCHIVOS_ENTRADA)):
        t, x, v, E = cargar_datos(archivo)
        
        ax.plot(t, v, 
                label=f'$b = {b}$ kg/s', 
                color=CONFIG_GRAFICAS['colores'][i],
                linestyle=CONFIG_GRAFICAS['estilos'][i],
                linewidth=CONFIG_GRAFICAS['ancho_linea'])
    
    ax.set_xlabel('Tiempo (s)', fontweight='bold')
    ax.set_ylabel('Velocidad (m/s)', fontweight='bold')
    ax.set_title('Evolución Temporal de la Velocidad del Oscilador Amortiguado', 
                 fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('velocidad_vs_tiempo.png', dpi=300)
    plt.show()
    
    print("✓ Gráfica de velocidad vs tiempo generada: velocidad_vs_tiempo.png")

def graficar_energia_vs_tiempo():
    """Genera gráfica de energía mecánica vs tiempo"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for i, (b, archivo) in enumerate(zip(VALORES_B, ARCHIVOS_ENTRADA)):
        t, x, v, E = cargar_datos(archivo)
        
        ax.plot(t, E, 
                label=f'$b = {b}$ kg/s', 
                color=CONFIG_GRAFICAS['colores'][i],
                linestyle=CONFIG_GRAFICAS['estilos'][i],
                linewidth=CONFIG_GRAFICAS['ancho_linea'])
    
    ax.set_xlabel('Tiempo (s)', fontweight='bold')
    ax.set_ylabel('Energía Mecánica (J)', fontweight='bold')
    ax.set_title('Energía Mecánica del Oscilador Amortiguado', 
                 fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Añadir línea de energía inicial de referencia
    ax.axhline(y=2.0, color='red', linestyle=':', alpha=0.7, 
               label='Energía inicial (2 J)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('energia_vs_tiempo.png', dpi=300)
    plt.show()
    
    print("✓ Gráfica de energía vs tiempo generada: energia_vs_tiempo.png")

def graficar_comparativa_regimenes():
    """Genera gráfica comparativa con los tres regímenes en subplots"""
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    axs = axs.ravel()
    
    for i, (b, archivo) in enumerate(zip(VALORES_B, ARCHIVOS_ENTRADA)):
        t, x, v, E = cargar_datos(archivo)
        
        # Posición
        axs[0].plot(t, x, 
                    label=f'$b = {b}$ kg/s', 
                    color=CONFIG_GRAFICAS['colores'][i],
                    linestyle=CONFIG_GRAFICAS['estilos'][i],
                    linewidth=CONFIG_GRAFICAS['ancho_linea'])
        
        # Velocidad
        axs[1].plot(t, v, 
                    label=f'$b = {b}$ kg/s', 
                    color=CONFIG_GRAFICAS['colores'][i],
                    linestyle=CONFIG_GRAFICAS['estilos'][i],
                    linewidth=CONFIG_GRAFICAS['ancho_linea'])
        
        # Energía
        axs[2].plot(t, E, 
                    label=f'$b = {b}$ kg/s', 
                    color=CONFIG_GRAFICAS['colores'][i],
                    linestyle=CONFIG_GRAFICAS['estilos'][i],
                    linewidth=CONFIG_GRAFICAS['ancho_linea'])
    
    # Configurar subplots
    titulos = ['Posición (m)', 'Velocidad (m/s)', 'Energía (J)', 'Espacio de Fases']
    ejes_y = ['Posición (m)', 'Velocidad (m/s)', 'Energía (J)', 'Velocidad (m/s)']
    
    for j, (ax, titulo, ey) in enumerate(zip(axs[:3], titulos[:3], ejes_y[:3])):
        ax.set_xlabel('Tiempo (s)', fontweight='bold')
        ax.set_ylabel(ey, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Espacio de fases (posición vs velocidad)
    for i, (b, archivo) in enumerate(zip(VALORES_B, ARCHIVOS_ENTRADA)):
        t, x, v, E = cargar_datos(archivo)
        axs[3].plot(x, v, 
                   label=f'$b = {b}$ kg/s', 
                   color=CONFIG_GRAFICAS['colores'][i],
                   linestyle=CONFIG_GRAFICAS['estilos'][i],
                   linewidth=CONFIG_GRAFICAS['ancho_linea'])
    
    axs[3].set_xlabel('Posición (m)', fontweight='bold')
    axs[3].set_ylabel('Velocidad (m/s)', fontweight='bold')
    axs[3].set_title('Espacio de Fases', fontsize=14, fontweight='bold')
    axs[3].legend()
    axs[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comparativa_regimenes.png', dpi=300)
    plt.show()
    
    print("✓ Gráfica comparativa generada: comparativa_regimenes.png")

# =============================================================================
# ANÁLISIS Y REPORTE DE RESULTADOS
# =============================================================================

def generar_reporte_energia():
    """Genera un reporte detallado de la energía disipada"""
    print("\n" + "="*60)
    print("REPORTE DE ENERGÍA DISIPADA")
    print("="*60)
    
    energia_teorica = 2.0  # 0.5*k*x0^2
    
    for b, archivo in zip(VALORES_B, ARCHIVOS_ENTRADA):
        t, x, v, E = cargar_datos(archivo)
        energia_disipada = calcular_energia_disipada(t, v, b)
        
        error_absoluto = abs(energia_disipada - energia_teorica)
        error_relativo = (error_absoluto / energia_teorica) * 100
        
        print(f"\nCoeficiente b = {b:.2f} kg/s:")
        print(f"  • Energía disipada calculada: {energia_disipada:.6f} J")
        print(f"  • Energía teórica esperada:   {energia_teorica:.6f} J")
        print(f"  • Error absoluto:            {error_absoluto:.6f} J")
        print(f"  • Error relativo:            {error_relativo:.4f} %")
        
        # Evaluación cualitativa
        if error_relativo < 1.0:
            evaluacion = "Excelente"
        elif error_relativo < 5.0:
            evaluacion = "Muy bueno"
        else:
            evaluacion = "Aceptable"
        
        print(f"  • Evaluación:                {evaluacion}")
    
    print("\n" + "="*60)

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal del script"""
    print("="*60)
    print("GENERADOR DE GRÁFICAS - OSCILADOR AMORTIGUADO")
    print("="*60)
    
    # Verificar que existan los archivos de datos
    print("Verificando archivos de datos...")
    for archivo in ARCHIVOS_ENTRADA:
        if not os.path.exists(archivo):
            print(f"❌ Error: No se encuentra {archivo}")
            print("Ejecute primero el programa Fortran para generar los datos")
            return
    
    print("✓ Todos los archivos de datos encontrados")
    
    # Generar gráficas
    print("\nGenerando gráficas...")
    graficar_posicion_vs_tiempo()
    graficar_velocidad_vs_tiempo()
    graficar_energia_vs_tiempo()
    graficar_comparativa_regimenes()
    
    # Generar reporte
    generar_reporte_energia()
    
    print("\n" + "="*60)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("="*60)
    print("Grágficas generadas:")
    print("  • posicion_vs_tiempo.png")
    print("  • velocidad_vs_tiempo.png")
    print("  • energia_vs_tiempo.png")
    print("  • comparativa_regimenes.png")

if _name_ == "_main_":
    main()
