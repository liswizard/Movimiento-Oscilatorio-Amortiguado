# Reporte Teórico: Oscilador Armónico Amortiguado

## Fundamentos Matemáticos

### Ecuación Diferencial del Movimiento

La ecuación que describe el movimiento del oscilador amortiguado es:

\[
m\frac{d^2x}{dt^2} + b\frac{dx}{dt} + kx = 0
\]

### Solución Analítica

La solución general depende del discriminante:

\[
\Delta = b^2 - 4mk
\]

#### Caso 1: Subamortiguado (\( \Delta < 0 \))
\[
x(t) = e^{-\gamma t}[A\cos(\omega_d t) + B\sin(\omega_d t)]
\]
donde:
- \( \gamma = \frac{b}{2m} \) (coeficiente de amortiguamiento)
- \( \omega_d = \sqrt{\omega_0^2 - \gamma^2} \) (frecuencia angular amortiguada)
- \( \omega_0 = \sqrt{\frac{k}{m}} \) (frecuencia natural)

#### Caso 2: Amortiguamiento Crítico (\( \Delta = 0 \))
\[
x(t) = (A + Bt)e^{-\gamma t}
\]

#### Caso 3: Sobreamortiguado (\( \Delta > 0 \))
\[
x(t) = Ae^{r_1 t} + Be^{r_2 t}
\]
donde \( r_{1,2} = -\gamma \pm \sqrt{\gamma^2 - \omega_0^2} \)

## Método Numérico Implementado

### Esquema de Euler-Cromer

*Actualización de velocidad:*
\[
v_{i+1} = v_i + a_i \cdot h
\]

*Actualización de posición:*
\[
x_{i+1} = x_i + v_{i+1} \cdot h
\]

*Aceleración:*
\[
a_i = -\frac{b}{m}v_i - \frac{k}{m}x_i
\]

### Análisis de Error

El método de Euler-Cromer es de primer orden para la velocidad y de segundo orden para la posición.

## Parámetros del Estudio

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| \( m \) | 0.5 kg | Masa del oscilador |
| \( k \) | 4.0 N/m | Constante del resorte |
| \( b \) | 0.5, 2.0, 3.0 kg/s | Coeficientes de fricción |
| \( h \) | 0.001 s | Paso temporal |
| \( t_{\text{max}} \) | 5.0 s | Tiempo de simulación |

## Validación Teórica

### Energía Inicial
\[
E_0 = \frac{1}{2}kx_0^2 = \frac{1}{2} \times 4 \times 1^2 = 2 \, \text{J}
\]

### Amortiguamiento Crítico Teórico
\[
b_{\text{crítico}} = 2\sqrt{mk} = 2\sqrt{0.5 \times 4} = 2\sqrt{2} \approx 2.828 \, \text{kg/s}
