#!/bin/bash

# =============================================================================
# Script de limpieza para el proyecto oscilador amortiguado
# =============================================================================

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Archivos y patrones a eliminar
PATRONES_ELIMINAR=(
    "oscilador"                 # Ejecutable principal
    "*.o"                       # Objetos Fortran
    "*.mod"                     # Módulos Fortran
    "resultados_b*.dat"         # Archivos de datos
    "*.png"                     # Gráficas
    "*.pdf"                     # Documentos (si se generan)
    "core"                      # Core dumps
    "*.tmp"                     # Archivos temporales
)

# Archivos a mantener (no eliminar)
ARCHIVOS_PROTEGIDOS=(
    "src/"
    "scripts/"
    "tests/"
    "docs/"
    "README.md"
    "LICENSE"
    ".gitignore"
)

# =============================================================================
# FUNCIONES
# =============================================================================

confirmar_eliminacion() {
    local archivo=$1
    read -p "¿Eliminar '$archivo'? [s/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        return 0
    else
        return 1
    fi
}

mostrar_estado_directorio() {
    print_info "Estado actual del directorio:"
    echo "=================================================="
    
    # Mostrar archivos relevantes
    for patron in "${PATRONES_ELIMINAR[@]}"; do
        archivos=($(find "$PROJECT_ROOT" -maxdepth 1 -name "$patron" 2>/dev/null))
        if [ ${#archivos[@]} -gt 0 ]; then
            echo "Patrón: $patron"
            for archivo in "${archivos[@]}"; do
                if [ -f "$archivo" ]; then
                    size=$(du -h "$archivo" | cut -f1)
                    echo "  📄 $(basename "$archivo") ($size)"
                elif [ -d "$archivo" ]; then
                    echo "  📁 $(basename "$archivo")/"
                fi
            done
            echo ""
        fi
    done
    echo "=================================================="
}

limpiar_archivos() {
    local modo=$1  # "auto" o "interactivo"
    local archivos_eliminados=0
    local espacio_liberado=0
    
    for patron in "${PATRONES_ELIMINAR[@]}"; do
        # Encontrar archivos que coincidan con el patrón
        while IFS= read -r -d '' archivo; do
            # Verificar que no sea un archivo protegido
            es_protegido=0
            for protegido in "${ARCHIVOS_PROTEGIDOS[@]}"; do
                if [[ "$archivo" == "$protegido" ]]; then
                    es_protegido=1
                    break
                fi
            done
            
            if [ $es_protegido -eq 0 ]; then
                if [ "$modo" == "interactivo" ]; then
                    if confirmar_eliminacion "$archivo"; then
                        eliminar_archivo "$archivo"
                        ((archivos_eliminados++))
                    fi
                else
                    eliminar_archivo "$archivo"
                    ((archivos_eliminados++))
                fi
            fi
        done < <(find "$PROJECT_ROOT" -name "$patron" -type f -print0 2>/dev/null)
    done
    
    echo "$archivos_eliminados"
}

eliminar_archivo() {
    local archivo=$1
    if [ -f "$archivo" ]; then
        tamaño=$(du -k "$archivo" | cut -f1)
        if rm "$archivo"; then
            print_info "✅ Eliminado: $archivo"
            ((espacio_liberado += tamaño))
        else
            print_error "❌ Error eliminando: $archivo"
        fi
    elif [ -d "$archivo" ]; then
        if rm -r "$archivo"; then
            print_info "✅ Eliminado directorio: $archivo"
        else
            print_error "❌ Error eliminando directorio: $archivo"
        fi
    fi
}

limpiar_cache_python() {
    print_info "Limpiando caché de Python..."
    find "$PROJECT_ROOT" -type d -name "_pycache_" -exec rm -rf {} + 2>/dev/null
    find "$PROJECT_ROOT" -name "*.pyc" -delete
    find "$PROJECT_ROOT" -name "*.pyo" -delete
    print_info "✅ Caché de Python limpiado"
}

mostrar_resumen() {
    local archivos_eliminados=$1
    local espacio_mb=$(echo "scale=2; $espacio_liberado/1024" | bc)
    
    print_info "=================================================="
    print_info "           RESUMEN DE LA LIMPIEZA"
    print_info "=================================================="
    print_info "Archivos eliminados: $archivos_eliminados"
    print_info "Espacio liberado: ${espacio_mb} MB"
    print_info "=================================================="
}

# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================

mostrar_menu() {
    echo ""
    print_info "OPCIONES DE LIMPIEZA:"
    echo "1) Limpieza automática (elimina todo sin confirmar)"
    echo "2) Limpieza interactiva (confirma cada archivo)"
    echo "3) Solo limpiar caché de Python"
    echo "4) Mostrar estado actual"
    echo "5) Salir"
    echo ""
}

main() {
    print_info "=================================================="
    print_info "       LIMPIADOR DE PROYECTO OSCILADOR"
    print_info "=================================================="
    
    cd "$PROJECT_ROOT" || {
        print_error "No se puede acceder al directorio del proyecto"
        exit 1
    }
    
    while true; do
        mostrar_menu
        read -p "Seleccione una opción (1-5): " opcion
        
        case $opcion in
            1)
                print_warning "Iniciando limpieza automática..."
                archivos_eliminados=$(limpiar_archivos "auto")
                limpiar_cache_python
                mostrar_resumen "$archivos_eliminados"
                ;;
            2)
                print_info "Iniciando limpieza interactiva..."
                archivos_eliminados=$(limpiar_archivos "interactivo")
                limpiar_cache_python
                mostrar_resumen "$archivos_eliminados"
                ;;
            3)
                limpiar_cache_python
                ;;
            4)
                mostrar_estado_directorio
                ;;
            5)
                print_info "Saliendo..."
                exit 0
                ;;
            *)
                print_error "Opción inválida"
                ;;
        esac
    done
}

# Ejecutar si se llama directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
