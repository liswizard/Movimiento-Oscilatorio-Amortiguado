#!/usr/bin/env python3
"""
Pruebas de validación física y numérica del oscilador amortiguado
"""

import numpy as np
import pytest
import os
import sys
from scipy import integrate

class TestValidacionFisica:
    """Pruebas de validación física del modelo"""
    
    # Parámetros físicos teóricos
    MASA = 0.5
    CONSTANTE_RESORTE = 4.0
    VALORES_B = [0.5, 2.0, 3.0]
    
    def test_frecuencia_natural(self):
        """Verifica la frecuencia natural del sistema"""
        # Frecuencia angular teórica: ω₀ = √(k/m)
        omega_teorico = np.sqrt(self.CONSTANTE_RESORTE / self.MASA)
        omega_calculado = np.sqrt(4.0 / 0.5)  # k=4, m=0.5
        
        assert np.isclose(omega_teorico, omega_calculado), \
            f"Frecuencia natural incorrecta: {omega_calculado} vs {omega_teorico}"
        
        # Período teórico
        periodo_teorico = 2 * np.pi / omega_teorico
        print(f"Período teórico del oscilador: {periodo_teorico:.4f} s")
    
    def test_amortiguamiento_critico(self):
        """Verifica el cálculo del amortiguamiento crítico"""
        # Amortiguamiento crítico: b_crítico = 2√(mk)
        b_critico_teorico = 2 * np.sqrt(self.MASA * self.CONSTANTE_RESORTE)
        b_critico_calculado = 2 * np.sqrt(0.5 * 4.0)
        
        assert np.isclose(b_critico_teorico, b_critico_calculado), \
            f"Amortiguamiento crítico incorrecto: {b_critico_calculado} vs {b_critico_teorico}"
        
        print(f"Amortiguamiento crítico teórico: {b_critico_teorico:.4f} kg/s")
        
        # Verificar que b=2.0 está cerca del crítico
        b_simulado = 2.0
        ratio = b_simulado / b_critico_teorico
        assert 0.9 < ratio < 1.1, f"b=2.0 debería estar cerca del crítico (ratio: {ratio:.3f})"
    
    def test_energia_inicial(self):
        """Verifica el cálculo de energía inicial"""
        x0, v0 = 1.0, 0.0  # Condiciones iniciales
        
        # Energía inicial teórica: E = 0.5*m*v² + 0.5*k*x²
        energia_teorica = 0.5 * self.MASA * v0*2 + 0.5 * self.CONSTANTE_RESORTE * x0*2
        energia_esperada = 2.0  # 0.5*4*1² = 2 J
        
        assert np.isclose(energia_teorica, energia_esperada), \
            f"Energía inicial incorrecta: {energia_teorica} vs {energia_esperada}"
        
        print(f"Energía inicial teórica: {energia_teorica:.4f} J")

class TestValidacionNumerica:
    """Pruebas de validación numérica del método"""
    
    def test_convergencia_integral(self):
        """Verifica la convergencia de la integración numérica"""
        # Para b=0.5, comparar diferentes métodos de integración
        b = 0.5
        filename = f"resultados_b{b:.2f}.dat"
        
        if not os.path.exists(filename):
            pytest.skip(f"Archivo {filename} no encontrado")
        
        # Cargar datos
        with open(filename, 'r') as f:
            lines = [line for line in f if not line.startswith('#')]
        data = np.loadtxt(lines)
        t, v = data[:, 0], data[:, 2]
        
        # Calcular integral con diferentes métodos
        integral_trapz = integrate.trapz(v**2, t)
        integral_simpson = integrate.simpson(v**2, t)
        integral_rect = np.sum(v**2) * (t[1] - t[0])  # Regla del rectángulo
        
        # Las diferencias deberían ser pequeñas
        error_trapz_simpson = abs(integral_trapz - integral_simpson) / integral_trapz
        error_trapz_rect = abs(integral_trapz - integral_rect) / integral_trapz
        
        assert error_trapz_simpson < 0.01, "Error grande entre trapz y simpson"
        assert error_trapz_rect < 0.05, "Error grande entre trapz y rectángulo"
        
        print(f"Convergencia integral - Trapz: {integral_trapz:.6f}, "
              f"Simpson: {integral_simpson:.6f}, Error: {error_trapz_simpson*100:.2f}%")
    
    def test_estabilidad_numerica(self):
        """Verifica la estabilidad del método numérico"""
        for b in [0.5, 2.0, 3.0]:
            filename = f"resultados_b{b:.2f}.dat"
            
            if not os.path.exists(filename):
                continue
                
            # Cargar datos
            with open(filename, 'r') as f:
                lines = [line for line in f if not line.startswith('#')]
            data = np.loadtxt(lines)
            x, v, E = data[:, 1], data[:, 2], data[:, 3]
            
            # Verificar que no hay valores NaN o infinitos
            assert not np.any(np.isnan(x)), f"Valores NaN en posición para b={b}"
            assert not np.any(np.isnan(v)), f"Valores NaN en velocidad para b={b}"
            assert not np.any(np.isinf(x)), f"Valores infinitos en posición para b={b}"
            assert not np.any(np.isinf(v)), f"Valores infinitos en velocidad para b={b}"
            
            # Verificar que la energía no se vuelve negativa
            assert np.all(E >= -1e-10), f"Energía negativa para b={b}"
            
            print(f"Estabilidad numérica para b={b}: ✅")

class TestAnalisisResultados:
    """Análisis avanzado de los resultados"""
    
    def test_comportamiento_asintotico(self):
        """Verifica el comportamiento asintótico del sistema"""
        for b in [0.5, 2.0, 3.0]:
            filename = f"resultados_b{b:.2f}.dat"
            
            if not os.path.exists(filename):
                continue
                
            # Cargar datos
            with open(filename, 'r') as f:
                lines = [line for line in f if not line.startswith('#')]
            data = np.loadtxt(lines)
            t, x, v = data[:, 0], data[:, 1], data[:, 2]
            
            # Verificar que el sistema tiende al equilibrio
            ultimo_cuarto = len(x) // 4
            x_final = x[ultimo_cuarto:]
            v_final = v[ultimo_cuarto:]
            
            # La posición y velocidad finales deberían ser cercanas a cero
            max_x_final = np.max(np.abs(x_final))
            max_v_final = np.max(np.abs(v_final))
            
            assert max_x_final < 0.1, f"Posición final muy grande para b={b}: {max_x_final}"
            assert max_v_final < 0.1, f"Velocidad final muy grande para b={b}: {max_v_final}"
            
            print(f"Comportamiento asintótico b={b}: "
                  f"max|x|={max_x_final:.4f}, max|v|={max_v_final:.4f}")
    
    def test_identificacion_regimenes(self):
        """Identifica automáticamente el régimen de amortiguamiento"""
        for b in [0.5, 2.0, 3.0]:
            filename = f"resultados_b{b:.2f}.dat"
            
            if not os.path.exists(filename):
                continue
                
            # Cargar datos
            with open(filename, 'r') as f:
                lines = [line for line in f if not line.startswith('#')]
            data = np.loadtxt(lines)
            t, x = data[:, 0], data[:, 1]
            
            # Contar cruces por cero para identificar oscilaciones
            signos = np.sign(x)
            cambios_signo = np.where(np.diff(signos))[0]
            num_oscilaciones = len(cambios_signo) // 2  # Cada oscilación tiene 2 cruces
            
            # Clasificar según el número de oscilaciones
            if num_oscilaciones > 3:
                regimen = "Subamortiguado"
            elif num_oscilaciones > 0:
                regimen = "Casi crítico"
            else:
                regimen = "Sobreamortiguado/Crítico"
            
            print(f"b={b}: {num_oscilaciones} oscilaciones → {regimen}")

def test_generar_reporte():
    """Genera un reporte completo de validación"""
    print("\n" + "="*60)
    print("REPORTE DE VALIDACIÓN COMPLETO")
    print("="*60)
    
    # Ejecutar todas las pruebas y capturar resultados
    test_classes = [TestValidacionFisica, TestValidacionNumerica, TestAnalisisResultados]
    
    for test_class in test_classes:
        print(f"\n{test_class._name_}:")
        print("-" * 40)
        
        # Crear instancia y ejecutar métodos de prueba
        instancia = test_class()
        for method_name in dir(instancia):
            if method_name.startswith('test_'):
                method = getattr(instancia, method_name)
                if callable(method):
                    try:
                        method()
                        print(f"  ✅ {method_name}")
                    except Exception as e:
                        print(f"  ❌ {method_name}: {e}")

if _name_ == "_main_":
    # Ejecutar el reporte de validación
    test_generar_reporte()
