#!/bin/bash

# =============================================================================
# Script de ejecución completa del proyecto oscilador amortiguado
# =============================================================================

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Funciones de impresión
print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
EXECUTABLE="$PROJECT_ROOT/oscilador"
PYTHON_SCRIPT="$PROJECT_ROOT/src/graficas_oscilador.py"

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

check_dependencies() {
    print_info "Verificando dependencias..."
    
    # Verificar compilador Fortran
    if ! command -v gfortran &> /dev/null; then
        print_error "gfortran no encontrado. Instale con: sudo apt-get install gfortran"
        return 1
    fi
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "python3 no encontrado"
        return 1
    fi
    
    # Verificar módulos Python
    if ! python3 -c "import numpy, matplotlib" 2>/dev/null; then
        print_warning "Algunos módulos Python pueden faltar"
        print_info "Instale con: pip3 install numpy matplotlib"
    fi
    
    print_info "✅ Dependencias verificadas"
}

compile_if_needed() {
    if [ ! -f "$EXECUTABLE" ]; then
        print_warning "Ejecutable no encontrado, compilando..."
        if ! "$SCRIPT_DIR/compilar.sh"; then
            print_error "Error en la compilación"
            return 1
        fi
    else
        print_info "✅ Ejecutable encontrado"
    fi
}

run_simulation() {
    print_info "Ejecutando simulación..."
    
    # Medir tiempo de ejecución
    start_time=$(date +%s)
    
    if ! ./"$EXECUTABLE"; then
        print_error "Error en la ejecución de la simulación"
        return 1
    fi
    
    end_time=$(date +%s)
    execution_time=$((end_time - start_time))
    
    print_info "✅ Simulación completada en ${execution_time} segundos"
}

generate_plots() {
    print_info "Generando gráficas..."
    
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        print_error "Script de gráficas no encontrado: $PYTHON_SCRIPT"
        return 1
    fi
    
    if ! python3 "$PYTHON_SCRIPT"; then
        print_error "Error generando gráficas"
        return 1
    fi
    
    print_info "✅ Gráficas generadas exitosamente"
}

check_results() {
    print_info "Verificando resultados..."
    
    # Verificar que se crearon los archivos de datos
    data_files=("resultados_b0.50.dat" "resultados_b2.00.dat" "resultados_b3.00.dat")
    missing_files=()
    
    for file in "${data_files[@]}"; do
        if [ ! -f "$PROJECT_ROOT/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        print_info "✅ Todos los archivos de datos generados"
        
        # Mostrar información de los archivos
        for file in "${data_files[@]}"; do
            if [ -f "$PROJECT_ROOT/$file" ]; then
                lines=$(wc -l < "$PROJECT_ROOT/$file")
                size=$(du -h "$PROJECT_ROOT/$file" | cut -f1)
                print_info "  📊 $file: $lines líneas, $size"
            fi
        done
    else
        print_warning "Faltan algunos archivos: ${missing_files[*]}"
    fi
    
    # Verificar gráficas generadas
    plot_files=("posicion_vs_tiempo.png" "velocidad_vs_tiempo.png" "energia_vs_tiempo.png")
    for plot in "${plot_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$plot" ]; then
            print_info "  📈 Gráfica generada: $plot"
        fi
    done
}

# =============================================================================
# FLUJO PRINCIPAL
# =============================================================================

main() {
    print_info "=================================================="
    print_info "    SIMULACIÓN OSCILADOR AMORTIGUADO"
    print_info "=================================================="
    
    # Cambiar al directorio del proyecto
    cd "$PROJECT_ROOT" || {
        print_error "No se puede acceder al directorio del proyecto"
        exit 1
    }
    
    # Ejecutar los pasos en orden
    if ! check_dependencies; then
        print_error "Faltan dependencias, abortando..."
        exit 1
    fi
    
    if ! compile_if_needed; then
        exit 1
    fi
    
    if ! run_simulation; then
        exit 1
    fi
    
    if ! generate_plots; then
        exit 1
    fi
    
    check_results
    
    print_info "=================================================="
    print_info "         PROCESO COMPLETADO EXITOSAMENTE"
    print_info "=================================================="
    print_info "Archivos generados:"
    print_info "  • resultados_b*.dat (datos de simulación)"
    print_info "  • *.png (gráficas de resultados)"
    print_info ""
    print_info "Próximos pasos:"
    print_info "  • Ver gráficas en el directorio actual"
    print_info "  • Ejecutar pruebas: python3 -m pytest tests/"
    print_info "  • Consultar docs/reporte_teorico.pdf para análisis detallado"
}

# Ejecutar función principal
main "$@"
