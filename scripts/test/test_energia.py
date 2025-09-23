#!/usr/bin/env python3
"""
Pruebas de validación para la conservación de energía en el oscilador amortiguado
"""

import numpy as np
import pytest
import os
import sys

# Agregar directorio principal al path para imports
sys.path.append(os.path.join(os.path.dirname(_file_), '..'))

class TestConservacionEnergia:
    """Pruebas relacionadas con la conservación de energía"""
    
    # Parámetros de prueba
    VALORES_B = [0.5, 2.0, 3.0]
    ENERGIA_TEORICA = 2.0  # 0.5 * k * x0^2 = 0.5 * 4 * 1^2 = 2 J
    TOLERANCIA_ERROR = 0.01  # 1% de tolerancia
    
    def cargar_datos(self, b):
        """Carga datos desde archivo para un coeficiente b dado"""
        filename = f"resultados_b{b:.2f}.dat"
        if not os.path.exists(filename):
            pytest.skip(f"Archivo {filename} no encontrado")
        
        # Cargar datos, saltando líneas de comentario
        with open(filename, 'r') as f:
            lines = [line for line in f if not line.startswith('#')]
        
        data = np.loadtxt(lines)
        return data[:, 0], data[:, 1], data[:, 2], data[:, 3]  # t, x, v, E
    
    def test_archivos_existen(self):
        """Verifica que todos los archivos de datos existen"""
        for b in self.VALORES_B:
            filename = f"resultados_b{b:.2f}.dat"
            assert os.path.exists(filename), f"Falta archivo: {filename}"
    
    def test_condiciones_iniciales(self):
        """Verifica que las condiciones iniciales sean correctas"""
        for b in self.VALORES_B:
            t, x, v, E = self.cargar_datos(b)
            
            # Verificar condiciones iniciales
            assert abs(x[0] - 1.0) < 1e-10, f"Posición inicial incorrecta para b={b}"
            assert abs(v[0] - 0.0) < 1e-10, f"Velocidad inicial incorrecta para b={b}"
            assert abs(E[0] - self.ENERGIA_TEORICA) < 1e-10, f"Energía inicial incorrecta para b={b}"
    
    def test_energia_disipada(self):
        """Verifica que la energía disipada ≈ energía inicial"""
        for b in self.VALORES_B:
            t, x, v, E = self.cargar_datos(b)
            
            # Calcular energía disipada por integración numérica
            integral_v2 = np.trapz(v**2, t)
            energia_disipada = b * integral_v2
            
            # Calcular error relativo
            error_relativo = abs(energia_disipada - self.ENERGIA_TEORICA) / self.ENERGIA_TEORICA
            
            # Verificar que el error sea menor a la tolerancia
            assert error_relativo < self.TOLERANCIA_ERROR, \
                f"Error muy grande para b={b}: {error_relativo*100:.2f}%"
    
    def test_energia_decrece(self):
        """Verifica que la energía mecánica nunca aumenta"""
        for b in self.VALORES_B:
            t, x, v, E = self.cargar_datos(b)
            
            # La energía debe ser monótonamente decreciente (o constante en caso ideal)
            # Permitimos pequeñas fluctuaciones numéricas
            diferencias = np.diff(E)
            incrementos = diferencias[diferencias > 1e-10]  # Ignorar fluctuaciones pequeñas
            
            assert len(incrementos) == 0, f"La energía aumenta en algún punto para b={b}"
    
    def test_convergencia_temporal(self):
        """Verifica que la energía tiende a cero para tiempos largos"""
        for b in self.VALORES_B:
            t, x, v, E = self.cargar_datos(b)
            
            # Verificar que en el último cuarto de la simulación la energía es pequeña
            punto_cuarto = len(E) // 4
            energia_final = E[punto_cuarto:]
            
            # La energía final debe ser pequeña (menor al 5% de la inicial)
            assert np.max(energia_final) < 0.05 * self.ENERGIA_TEORICA, \
                f"La energía no decae suficientemente para b={b}"
    
    def test_formato_archivos(self):
        """Verifica el formato correcto de los archivos de datos"""
        for b in self.VALORES_B:
            filename = f"resultados_b{b:.2f}.dat"
            
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            # Verificar que tiene encabezado de comentarios
            lineas_comentario = [line for line in lines if line.startswith('#')]
            assert len(lineas_comentario) >= 3, f"Falta encabezado en {filename}"
            
            # Verificar número de columnas
            lineas_datos = [line for line in lines if not line.startswith('#')]
            primera_linea = lineas_datos[0].split()
            assert len(primera_linea) == 4, f"Formato incorrecto en {filename}"

def test_rendimiento():
    """Prueba de rendimiento - verifica que la simulación sea eficiente"""
    # Esta prueba verifica que los archivos tengan un número razonable de puntos
    for b in [0.5, 2.0, 3.0]:
        filename = f"resultados_b{b:.2f}.dat"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = [line for line in f if not line.startswith('#')]
            
            # Debería tener alrededor de 5000 puntos (5s / 0.001s)
            assert 4000 <= len(lines) <= 6000, f"Número de puntos inesperado en {filename}"

if _name_ == "_main_":
    # Ejecutar pruebas manualmente
    pytest.main([_file_, "-v"])
