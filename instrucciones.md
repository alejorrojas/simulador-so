================================================================================
INSTRUCCIONES DE EJECUCIÓN - SIMULADOR DE ASIGNACIÓN DE MEMORIA
================================================================================

Este documento contiene las instrucciones para ejecutar el simulador en
Windows y Linux usando los ejecutables precompilados incluidos en el zip.

IMPORTANTE: El simulador requiere un archivo CSV con un formato específico.
Asegúrese de tener un archivo CSV válido antes de ejecutar el programa.

================================================================================
FORMATO DEL ARCHIVO CSV REQUERIDO
================================================================================

El archivo CSV debe tener EXACTAMENTE las siguientes columnas (en este orden):

  proceso_id,t_arribo_al_sistema,memoria_K,tiempo_irrupcion

Ejemplo de contenido válido:

  proceso_id,t_arribo_al_sistema,memoria_K,tiempo_irrupcion
  P1,0,200,5
  P2,1,50,3
  P3,2,180,8

Descripción de las columnas:
  - proceso_id: Identificador único del proceso (texto, ej: P1, A1, Proceso1)
  - t_arribo_al_sistema: Instante en que el proceso llega al sistema (número entero >= 0)
  - memoria_K: Tamaño del proceso en KB (número entero > 0)
  - tiempo_irrupcion: Tiempo de CPU que necesita el proceso (número entero > 0)

Restricciones:
  - Máximo 10 procesos por archivo
  - Los valores numéricos deben ser enteros
  - memoria_K y tiempo_irrupcion deben ser positivos
  - t_arribo_al_sistema no puede ser negativo

NOTA: Puede encontrar archivos CSV de ejemplo en la carpeta:
      ejecutables/ejemplos
      
      Archivos de ejemplo disponibles:
      - catedra_lote_1.csv
      - catedra_lote_2.csv
      - catedra_lote_3.csv

================================================================================
EJECUCIÓN EN WINDOWS
================================================================================

PASO 1: Extraer el archivo ZIP
  - Descomprima el archivo "grupo-round-robin-tpi.zip"
  - Se creará la carpeta "grupo-round-robin-tpi"

PASO 2: Abrir la carpeta de ejecutables
  - Navegue a: grupo-round-robin-tpi\ejecutables\
  - Encontrará el archivo: simulador-memoria-windows.exe

PASO 3: Preparar el archivo CSV
  - Los archivos CSV de ejemplo se encuentran en: grupo-round-robin-tpi\ejecutables\ejemplos\
  - Puede usar directamente uno de los archivos de ejemplo desde esa carpeta

PASO 4: Ejecutar el simulador
  - Haga doble clic en "simulador-memoria-windows.exe"
  - O abra una terminal (PowerShell o CMD) en la carpeta ejecutables y ejecute:
    
    .\simulador-memoria-windows.exe

PASO 5: Usar el menú interactivo
  - El programa mostrará un menú con 4 opciones:
    1. Cargar archivo de procesos (CSV)
    2. Ver procesos cargados
    3. Iniciar simulación
    4. Salir

  - Si colocó un archivo llamado "procesos.csv" en la misma carpeta que el
    ejecutable, puede presionar Enter cuando se le solicite la ruta del archivo
    para usar ese archivo automáticamente.

  - Si el archivo está en otra ubicación, ingrese la ruta completa, por ejemplo:
    C:\Users\Profesor\Desktop\procesos.csv
    o una ruta relativa desde donde ejecutó el programa, por ejemplo:
    .\ejemplos\catedra_lote_1.csv

PASO 6: Iniciar la simulación
  - Seleccione la opción 1 para cargar el archivo CSV
  - Verifique los procesos cargados con la opción 2
  - Seleccione la opción 3 para iniciar la simulación
  - Siga las instrucciones en pantalla para avanzar paso a paso

NOTA: Si aparece un error al cargar el CSV, verifique que:
  - El archivo tenga las columnas exactas mencionadas anteriormente
  - No haya espacios extra en los nombres de las columnas
  - Los valores numéricos sean enteros válidos
  - El archivo no tenga más de 10 procesos

================================================================================
EJECUCIÓN EN LINUX
================================================================================

PASO 1: Extraer el archivo ZIP
  - Descomprima el archivo "grupo-round-robin-tpi.zip"
  - Se creará la carpeta "grupo-round-robin-tpi"

PASO 2: Abrir la carpeta de ejecutables
  - Navegue a: grupo-round-robin-tpi/ejecutables/
  - Encontrará el archivo: simulador-memoria-linux-x86_64

PASO 3: Dar permisos de ejecución
  - Abra una terminal en la carpeta ejecutables
  - Ejecute el siguiente comando para dar permisos de ejecución:
    
    chmod +x simulador-memoria-linux-x86_64

PASO 4: Preparar el archivo CSV
  - Los archivos CSV de ejemplo se encuentran en: grupo-round-robin-tpi/ejecutables/ejemplos/
  - Puede usar directamente uno de los archivos de ejemplo desde esa carpeta

PASO 5: Ejecutar el simulador
  - Desde la terminal en la carpeta ejecutables, ejecute:
    
    ./simulador-memoria-linux-x86_64

PASO 6: Usar el menú interactivo
  - El programa mostrará un menú con 4 opciones:
    1. Cargar archivo de procesos (CSV)
    2. Ver procesos cargados
    3. Iniciar simulación
    4. Salir

  - Si colocó un archivo llamado "procesos.csv" en la misma carpeta que el
    ejecutable, puede presionar Enter cuando se le solicite la ruta del archivo
    para usar ese archivo automáticamente.

  - Si el archivo está en otra ubicación, ingrese la ruta completa, por ejemplo:
    /home/usuario/Desktop/procesos.csv
    o una ruta relativa desde donde ejecutó el programa, por ejemplo:
    ejemplos/catedra_lote_1.csv

PASO 7: Iniciar la simulación
  - Seleccione la opción 1 para cargar el archivo CSV
  - Verifique los procesos cargados con la opción 2
  - Seleccione la opción 3 para iniciar la simulación
  - Siga las instrucciones en pantalla para avanzar paso a paso

NOTA: Si aparece un error al cargar el CSV, verifique que:
  - El archivo tenga las columnas exactas mencionadas anteriormente
  - No haya espacios extra en los nombres de las columnas
  - Los valores numéricos sean enteros válidos
  - El archivo no tenga más de 10 procesos

================================================================================
SOLUCIÓN DE PROBLEMAS COMUNES
================================================================================

ERROR: "El archivo CSV debe tener las columnas: proceso_id, t_arribo_al_sistema, memoria_K, tiempo_irrupcion"
  SOLUCIÓN: Verifique que la primera línea del CSV tenga exactamente esos
            nombres de columna, sin espacios adicionales y en ese orden.

ERROR: "No se encontró el archivo: [ruta]"
  SOLUCIÓN: Verifique que la ruta sea correcta. En Windows, use barras
            invertidas (\) o barras normales (/). En Linux, use barras
            normales (/). Puede usar rutas relativas o absolutas.

El ejecutable no se ejecuta en Linux
  SOLUCIÓN: Asegúrese de haber dado permisos de ejecución con:
            chmod +x simulador-memoria-linux-x86_64

================================================================================
INFORMACIÓN ADICIONAL
================================================================================

FLUJO DE PROCESAMIENTO DE FINALIZACIONES

IMPORTANTE - Comportamiento en el mismo instante de tiempo:

Cuando un proceso termina (tiempo_restante == 0), en el mismo instante de tiempo se realizan tres acciones secuenciales:

1. Liberar memoria: El proceso pasa a estado "Terminado", se libera su partición 
   de memoria y se registra su tiempo_finalizacion = tiempo_actual.

2. Cargar el siguiente proceso: 
   - Primero se intentan promover procesos suspendidos a listos (si hay espacio 
     y memoria disponible usando Best-Fit).
   - Después se intentan asignar procesos nuevos a memoria (si hay espacio, 
     también usando Best-Fit).

3. Re-evaluar SRTF inmediatamente: Una vez que se han cargado nuevos procesos a 
   memoria (promovidos o asignados), se vuelve a evaluar SRTF inmediatamente 
   considerando al nuevo integrante. Esto significa:
   - Se ordena la cola de listos por tiempo restante (ascendente).
   - Se selecciona el proceso con menor tiempo restante para ejecutar.
   - Si el proceso que estaba ejecutando tiene más tiempo restante que algún 
     proceso en la cola de listos, se produce preemption.

Ejemplo:
  - En tiempo T=10, proceso P1 termina (tiempo_restante = 0).
  - Mismo instante T=10:
    1. Se libera memoria de P1 → Partición queda libre.
    2. Se promueve P2 (suspendido) a memoria → P2 entra a cola de listos.
    3. Se re-evalúa SRTF → Si P2 tiene menos tiempo restante que el proceso 
       actual, P2 ejecuta inmediatamente (preemption).

ORDEN DE PROCESAMIENTO DE COLAS

Cola de Nuevos (al asignar memoria):
  - Se ordenan por: (t_arribo_al_sistema, tiempo_irrupcion) ascendente
  - Procesos que llegaron antes tienen prioridad (FIFO por arribo)
  - Si varios procesos llegaron al mismo tiempo, se prioriza el de menor 
    tiempo de irrupción

Cola de Suspendidos (al promover):
  - Se procesan en orden FIFO (primero en llegar, primero en promover)
  - Pero si el primero no cabe, se intenta con los siguientes (puede haber 
    uno más pequeño que sí quepa)

Cola de Listos:
  - Siempre ordenada por tiempo_restante ascendente (SRTF)

CÁLCULO DE TIEMPOS

Tiempo de Finalización:
  - Es el instante en que el proceso pasa a estado "Terminado"
  - Se registra cuando tiempo_restante == 0

Tiempo de Retorno (Turnaround Time):
  
  Tiempo de Retorno = Tiempo de Finalización - Tiempo de Arribo

Tiempo de Espera:
  
  Tiempo de Espera = Tiempo de Retorno - Tiempo de Irrupción

NOTA: El tiempo de espera incluye:
  - Tiempo esperando en cola de listos (antes de ejecutar)
  - Tiempo esperando en cola de suspendidos (sin memoria)
  - Tiempo esperando en cola de nuevos (si grado de multiprogramación está lleno)
  - Tiempo de preemption (si fue preemptado y volvió a esperar)

SALIDA ESPERADA

Al finalizar la simulación, debes generar una tabla con el siguiente formato:

  Tiempos por Proceso
  ┌──────────┬──────────────────┬───────────────┬──────────────┐
  │ Proceso  │ T. Finalización  │ T. Retorno    │ T. Espera    │
  ├──────────┼──────────────────┼───────────────┼──────────────┤
  │ A1       │ 12               │ 12            │ 0            │
  │ A2       │ 21               │ 20            │ 11           │
  │ A3       │ 29               │ 27            │ 19           │
  │ ...      │ ...              │ ...           │ ...          │
  └──────────┴──────────────────┴───────────────┴──────────────┘

VALIDACIONES IMPORTANTES

  - Un proceso solo puede estar en UNA cola a la vez
  - Un proceso solo puede tener UNA partición asignada
  - El grado de multiprogramación nunca debe exceder 5
  - Un proceso no puede ejecutarse si no está en memoria
  - Los procesos que excedan el tamaño de la partición más grande (250KB)
    serán detectados antes de iniciar la simulación, se mostrará una 
    advertencia y serán ignorados. La simulación continuará solo con 
    los procesos válidos.

================================================================================
