! =============================================================================
! Programa: Oscilador Armónico Amortiguado
! Método: Euler-Cromer
! =============================================================================

program oscilador_amortiguado
  implicit none
  
  ! ===========================================================================
  ! DECLARACIÓN DE VARIABLES Y PARÁMETROS
  ! ===========================================================================
  integer, parameter :: nmax = 10000    ! Número máximo de pasos
  integer, parameter :: nb = 3          ! Número de coeficientes de fricción
  real(8) :: m, k, h, tmax, b           ! Parámetros físicos y numéricos
  real(8), dimension(0:nmax) :: x, v, a, t, E  ! Arrays de evolución temporal
  real(8) :: Edis, sum_v2               ! Energía disipada y acumulador
  real(8), dimension(nb) :: bvals = (/ 0.5d0, 2.0d0, 3.0d0 /)  ! Valores de b
  integer :: i, j, nsteps, fileunit     ! Variables de loop y archivo
  character(len=40) :: filename          ! Nombre de archivo de salida
  character(len=8) :: date               ! Fecha para el log
  character(len=10) :: time              ! Hora para el log
  
  ! ===========================================================================
  ! PARÁMETROS FÍSICOS Y NUMÉRICOS
  ! ===========================================================================
  m = 0.5d0        ! Masa (kg)
  k = 4.0d0        ! Constante del resorte (N/m)
  h = 0.001d0      ! Paso temporal (s)
  tmax = 5.0d0     ! Tiempo máximo de simulación (s)
  nsteps = int(tmax/h)  ! Número total de pasos
  
  ! ===========================================================================
  ! ENCABEZADO DEL PROGRAMA
  ! ===========================================================================
  call date_and_time(date=date, time=time)
  print *, "================================================"
  print *, "SIMULACIÓN OSCILADOR AMORTIGUADO"
  print *, "Fecha: ", date(7:8), "/", date(5:6), "/", date(1:4)
  print *, "Hora: ", time(1:2), ":", time(3:4)
  print *, "================================================"
  print *, "Parámetros de simulación:"
  print *, "  Masa (m): ", m, " kg"
  print *, "  Constante resorte (k): ", k, " N/m"
  print *, "  Paso temporal (h): ", h, " s"
  print *, "  Tiempo total: ", tmax, " s"
  print *, "  Número de pasos: ", nsteps
  print *, "================================================"
  
  ! ===========================================================================
  ! BUCLE PRINCIPAL SOBRE COEFICIENTES DE FRICCIÓN
  ! ===========================================================================
  do j = 1, nb
     b = bvals(j)
     
     print *, ""
     print *, "Procesando coeficiente b = ", b, " kg/s"
     print *, "----------------------------------------"
     
     ! ------------------------------------------------------------------------
     ! CONDICIONES INICIALES
     ! ------------------------------------------------------------------------
     x(0) = 1.0d0      ! Posición inicial (m)
     v(0) = 0.0d0      ! Velocidad inicial (m/s)
     t(0) = 0.0d0      ! Tiempo inicial (s)
     E(0) = 0.5d0*m*v(0)*2 + 0.5d0*k*x(0)*2  ! Energía inicial
     sum_v2 = 0.0d0    ! Inicializar acumulador para energía disipada
     
     ! ------------------------------------------------------------------------
     ! INTEGRACIÓN TEMPORAL (MÉTODO DE EULER-CROMER)
     ! ------------------------------------------------------------------------
     do i = 0, nsteps-1
        ! Avance del tiempo
        t(i+1) = t(i) + h
        
        ! Cálculo de la aceleración (ecuación de movimiento)
        a(i) = -(b/m)*v(i) - (k/m)*x(i)
        
        ! Actualización de velocidad (Euler hacia adelante)
        v(i+1) = v(i) + a(i)*h
        
        ! Actualización de posición (Euler-Cromer)
        x(i+1) = x(i) + v(i+1)*h
        
        ! Cálculo de energía mecánica total
        E(i+1) = 0.5d0*m*v(i+1)*2 + 0.5d0*k*x(i+1)*2
        
        ! Acumulación para energía disipada (integral de v^2)
        sum_v2 = sum_v2 + v(i)**2 * h
     end do
     
     ! ------------------------------------------------------------------------
     ! CÁLCULO DE ENERGÍA DISIPADA TOTAL
     ! ------------------------------------------------------------------------
     Edis = b * sum_v2
     
     ! ------------------------------------------------------------------------
     ! ESCRITURA DE RESULTADOS A ARCHIVO
     ! ------------------------------------------------------------------------
     write(filename,'("resultados_b",f0.2,".dat")') b
     
     open(newunit=fileunit, file=trim(filename), status="replace")
     
     ! Escribir encabezado del archivo
     write(fileunit, '(A)') "# Datos del oscilador amortiguado"
     write(fileunit, '(A, F6.3)') "# Coeficiente de fricción b = ", b
     write(fileunit, '(A, F6.3, A, F6.3, A, F6.3)') "# Parámetros: m = ", m, &
          " kg, k = ", k, " N/m, h = ", h, " s"
     write(fileunit, '(A)') "# Columnas: Tiempo(s) Posición(m) Velocidad(m/s) Energía(J)"
     
     ! Escribir datos
     do i = 0, nsteps
        write(fileunit, '(4F15.6)') t(i), x(i), v(i), E(i)
     end do
     
     close(fileunit)
     
     ! ------------------------------------------------------------------------
     ! REPORTE DE RESULTADOS EN CONSOLA
     ! ------------------------------------------------------------------------
     print *, "Archivo generado: ", trim(filename)
     print *, "Energía disipada: ", Edis, " J"
     print *, "Energía inicial:  2.000000 J"
     print *, "Diferencia: ", abs(Edis - 2.0d0), " J"
     print *, "Error relativo: ", abs(Edis - 2.0d0)/2.0d0 * 100.0d0, " %"
     
  end do
  
  ! ===========================================================================
  ! FINALIZACIÓN DEL PROGRAMA
  ! ===========================================================================
  print *, ""
  print *, "================================================"
  print *, "SIMULACIÓN COMPLETADA EXITOSAMENTE"
  print *, "Archivos de datos generados en el directorio actual"
  print *, "================================================"
  
end program oscilador_amortiguado
