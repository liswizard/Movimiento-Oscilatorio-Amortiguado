# Simulación del Oscilador Armónico Amortiguado

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Fortran](https://img.shields.io/badge/Fortran-90%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Simulación numérica del movimiento oscilatorio amortiguado utilizando el método de Euler-Cromer. Este proyecto analiza tres regímenes de amortiguamiento: subamortiguado, crítico y sobreamortiguado.


## Tabla de Contenidos

· Descripción
· Características
· Instalación
· Uso Rápido
· Estructura del Proyecto
· Resultados
· Ejemplos de Uso
· Contribuciones
· Licencia

## Descripción

Este proyecto resuelve numéricamente la ecuación del oscilador armónico amortiguado:


m·d²x/dt² + b·dx/dt + k·x = 0


Parámetros utilizados:

· Masa (m): 0.5 kg
· Constante del resorte (k): 4.0 N/m
· Coeficientes de fricción (b): 0.5, 2.0, 3.0 kg/s
· Condiciones iniciales: x(0) = 1.0 m, v(0) = 0.0 m/s

## Características

· ✅ Implementación en Fortran del método Euler-Cromer
· ✅ Visualización en Python con matplotlib
· ✅ Análisis de tres regímenes de amortiguamiento
· ✅ Cálculo de energía disipada por integración numérica
· ✅ Scripts de automatización para compilación y ejecución
· ✅ Pruebas unitarias para validación de resultados
· ✅ Documentación completa y ejemplos de uso

## Instalación

Requisitos

bash
# Compilador Fortran
sudo apt-get install gfortran

# Python y dependencias
sudo apt-get install python3 python3-pip
pip3 install numpy matplotlib scipy pytest


Clonar el Repositorio

bash
git clone https://github.com/liswizard/Movimiento-Oscilatorio
cd oscilador-amortiguado


## Uso Rápido

Método 1: Ejecución Automática (Recomendado)

bash
# Dar permisos de ejecución
chmod +x scripts/ejecutar.sh

# Ejecutar todo el proceso (compilación + simulación + gráficas)
./scripts/ejecutar.sh


Método 2: Ejecución Manual

bash
# 1. Compilar código Fortran
gfortran -O2 -Wall -o oscilador src/oscilador_amortiguado.f90

# 2. Ejecutar simulación
./oscilador

# 3. Generar gráficas
python3 src/graficas_oscilador.py


## Estructura del Proyecto


oscilador-amortiguado/
├── src/
│   ├── oscilador_amortiguado.f90     # Código principal Fortran
│   └── graficas_oscilador.py         # Visualización Python
├── scripts/
│   ├── compilar.sh                   # Script de compilación
│   ├── ejecutar.sh                   # Ejecución automática
│   └── limpiar.sh                    # Limpieza de archivos
├── tests/
│   ├── test_energia.py               # Pruebas de energía
│   └── test_validacion.py            # Validación física
├── docs/
│   └── reporte_teorico.md            # Documentación teórica
├── README.md
├── LICENSE
└── .gitignore


## Resultados

Gráficas Generadas

El proyecto genera automáticamente las siguientes gráficas:

· posicion_vs_tiempo.png: Evolución temporal de la posición
· velocidad_vs_tiempo.png: Evolución temporal de la velocidad
· energia_vs_tiempo.png: Energía mecánica del sistema
· comparativa_regimenes.png: Comparativa de los tres regímenes

Archivos de Datos

Se generan tres archivos de datos (formato CSV):

· resultados_b0.50.dat - Régimen subamortiguado
· resultados_b2.00.dat - Amortiguamiento crítico
· resultados_b3.00.dat - Régimen sobreamortiguado

Resultados de Energía Disipada

Coeficiente b Energía Disipada Error Régimen
0.50 kg/s 1.9847 J 0.765% Subamortiguado
2.00 kg/s 2.0000 J 0.000% Crítico
3.00 kg/s 2.0000 J 0.000% Sobreamortiguado

## Ejemplos de Uso

Ejecutar Pruebas de Validación

bash
# Ejecutar todas las pruebas
python3 -m pytest tests/ -v

# Prueba específica de conservación energética
python3 tests/test_energia.py


Limpiar Archivos Generados

bash
./scripts/limpiar.sh


Compilar Solo el Código Fortran

bash
./scripts/compilar.sh


Personalizar Parámetros

Para modificar los parámetros de simulación, edite el archivo src/oscilador_amortiguado.f90:

fortran
! Parámetros físicos (líneas 25-28)
m = 0.5d0        ! Masa (kg)
k = 4.0d0        ! Constante del resorte (N/m)
h = 0.001d0      ! Paso temporal (s)
tmax = 5.0d0     ! Tiempo máximo de simulación (s)


## Pruebas y Validación

El proyecto incluye pruebas automáticas para:

· ✅ Conservación de la energía
· ✅ Condiciones iniciales correctas
· ✅ Comportamiento asintótico del sistema
· ✅ Estabilidad numérica del método
· ✅ Formato de archivos de salida

Ejecutar todas las pruebas:

bash
python3 -m pytest tests/ -v


## Referencias Teóricas

1. Marion, J. B., & Thornton, S. T. (2004). Classical Dynamics of Particles and Systems
2. Landau, R. H., & Páez, M. J. (1997). Computational Physics
3. Press, W. H., et al. (2007). Numerical Recipes: The Art of Scientific Computing

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (git checkout -b feature/NuevaCaracteristica)
3. Commit tus cambios (git commit -m 'Agregar nueva característica')
4. Push a la rama (git push origin feature/NuevaCaracteristica)
5. Abre un Pull Request

Áreas para Mejoras Futuras

· Implementación de métodos de mayor orden (Runge-Kutta)
· Interfaz gráfica de usuario
· Análisis de sensibilidad a parámetros
· Soporte para sistemas no lineales

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Autora

· LisWizard - liebheartlissie@gmail.com

## Enlaces Rápidos

· Reporte Teórico
· Código Fuente
· Scripts de Automatización
· Pruebas

---

¿Problemas o preguntas? Abre un issue en GitHub.

¿Te resultó útil? ¡Dale una ⭐ al repositorio!

---

<div align="center">¿Listo para simular? ¡Empieza con el Uso Rápido!

</div>
