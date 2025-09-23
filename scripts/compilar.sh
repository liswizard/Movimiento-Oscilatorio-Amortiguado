```bash
#!/bin/bash

# =============================================================================
# Script de compilación para el oscilador amortiguado
# =============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_ROOT/src"
OUTPUT_NAME="oscilador"
COMPILER="gfortran"
FLAGS="-O2 -Wall -Wextra -pedantic"
SOURCE_FILE="$SRC_DIR/oscilador_amortiguado.f90"

# =============================================================================
# VERIFICACIONES INICIALES
# =============================================================================

print_status "Iniciando proceso de compilación..."
print_status "Directorio del proyecto: $PROJECT_ROOT"

# Verificar que existe el compilador
if ! command -v $COMPILER &> /dev/null; then
    print_error "No se encontró el compilador $COMPILER"
    print_error "Instale gfortran antes de continuar:"
    print_error "  Ubuntu/Debian: sudo apt-get install gfortran"
    print_error "  Fedora: sudo dnf install gcc-gfortran"
    exit 1
fi

print_status "Compilador encontrado: $(which $COMPILER)"
print_status "Versión: $($COMPILER --version | head -n1)"

# Verificar que existe el archivo fuente
if [ ! -f "$SOURCE_FILE" ]; then
    print_error "No se encuentra el archivo fuente: $SOURCE_FILE"
    exit 1
fi

print_status "Archivo fuente encontrado: $SOURCE_FILE"

# =============================================================================
# COMPILACIÓN
# =============================================================================

print_status "Compilando con flags: $FLAGS"

cd "$PROJECT_ROOT"

# Compilar
$COMPILER $FLAGS -o $OUTPUT_NAME "$SOURCE_FILE"

# Verificar si la compilación fue exitosa
if [ $? -eq 0 ]; then
    print_status "✅ Compilación exitosa!"
    print_status "Ejecutable creado: $PROJECT_ROOT/$OUTPUT_NAME"
    
    # Mostrar información del ejecutable
    if [ -f "$OUTPUT_NAME" ]; then
        file_size=$(du -h "$OUTPUT_NAME" | cut -f1)
        print_status "Tamaño del ejecutable: $file_size"
    fi
else
    print_error "❌ Error en la compilación"
    exit 1
fi

# =============================================================================
# VERIFICACIÓN DEL EJECUTABLE
# =============================================================================

print_status "Verificando el ejecutable..."

if [ -x "$OUTPUT_NAME" ]; then
    print_status "✅ El ejecutable tiene permisos de ejecución"
else
    print_warning "El ejecutable no tiene permisos de ejecución, asignando..."
    chmod +x "$OUTPUT_NAME"
fi

# Verificar que el ejecutable puede ser ejecutado
if ./$OUTPUT_NAME --help 2>/dev/null | grep -q "SIMULACIÓN"; then
    print_status "✅ El ejecutable funciona correctamente"
else
    print_warning "No se pudo verificar completamente el ejecutable"
fi

print_status "Proceso de compilación completado!"
echo ""
print_status "Para ejecutar la simulación: ./$OUTPUT_NAME"
print_status "Para generar gráficas: python3 src/graficas_oscilador.py"
