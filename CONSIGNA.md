# Simulador de Asignación de Memoria y Planificación de Procesos

El objetivo de esta práctica consiste en implementar un simulador que muestre los aspectos de la planificación a corto plazo y la gestión de memoria con particiones fijas en un esquema de un solo procesador, tratando el ciclo de vida completo de un proceso desde su ingreso al sistema hasta su finalización.

---

## Consigna

Implementar un simulador de asignación de memoria y planificación de procesos con los siguientes requerimientos:

- El simulador deberá permitir cargar procesos ingresados por el usuario.
- Se permitirá un máximo de **10 procesos**.
- La asignación de memoria será con **particiones fijas**.
- Las particiones serán:

  - **100K** destinados al Sistema Operativo  
  - **250K** para trabajos grandes  
  - **150K** para trabajos medianos  
  - **50K** para trabajos pequeños  

- Se permitirá el ingreso de nuevos procesos cuando sea posible, manteniendo un **grado de multiprogramación de 5**.
- La política de asignación de memoria será **Best-Fit**.
- Para cada proceso se leerá desde un archivo:
  - Id de proceso  
  - Tamaño del proceso  
  - Tiempo de arribo  
  - Tiempo de irrupción  
- La planificación del CPU será mediante **SRTF**.
- Estados manejados:
  - Nuevo  
  - Listo  
  - Listo y suspendido  
  - Ejecución  
  - Terminado  

(No se usa el estado Bloqueado para simplificar.)

---

## Salida esperada del simulador

- Estado del procesador (proceso en ejecución en ese instante).
- Tabla de particiones de memoria, incluyendo:
  - Id de partición  
  - Dirección de comienzo  
  - Tamaño  
  - Id de proceso asignado  
  - Fragmentación interna  
- Estado de la cola de:
  - Listos  
  - Listos/suspendidos  
- Al finalizar:
  - Tiempo de retorno y tiempo de espera de cada proceso  
  - Promedios de estos tiempos  
  - Rendimiento del sistema (trabajos terminados por unidad de tiempo)

---

## Consideraciones

- Las salidas deben presentarse cada vez que:
  - Llega un nuevo proceso  
  - Termina un proceso en ejecución  
- IMPORTANTE: No se permiten corridas ininterrumpidas desde inicio hasta final sin mostrar estados. Las presentaciones de salida deberán realizarse cada vez que llega un nuevo proceso o se termina un proceso en  ejecución. No se permiten corridas ininterrumpidas de simulador, desde que se inicia la simulación hasta que termina el último proceso.
- El programa deberá ser implementado en **Python**.
- La interacción debe ser por terminal
- En la imagen diagrama-flujo.png, existe un diagrama de flujo del funcionamiento de programa. La implementación en codigo debe aproximarse o tratar de imitar este flujo


---

## Ejemplos de salidas esperadas 

Aclaración: Estos ejemplos no son de una implementación real, solo describen el formato de salida esperado.
--- 

------------------------ ESTADO INICIAL DE LA MEMORIA ------------------------

ESTADOS DE LOS PROCESOS:
- EJECUTANDOSE: No hay procesos ejecutandose
- LISTOS:
- LISTOS Y SUSPENDIDOS:
- NUEVOS:
- SIN ARRIBAR: P1, P2, P3, P4, P5, P6, P7, P8, P9, P10
- TERMINADOS:


┌───────────┬────────────────────┬───────────────────────┬──────────────┐
│ PARTICIÓN │     CONTENIDO      │ TAMAÑO PARTICIÓN      │ FI/FE/EL     │
├───────────┼────────────────────┼───────────────────────┼──────────────┤
│     0     │ Sistema operativo  │       100 KB          │ FI: 0 KB     │
│     1     │         -          │       250 KB          │ Espacio Libre│
│     2     │         -          │       120 KB          │ Espacio Libre│
│     3     │         -          │        60 KB          │ Espacio Libre│
└───────────┴────────────────────┴───────────────────────┴──────────────┘


PRESIONE ENTER PARA CONTINUAR

---

---------------- SE ASIGNARON P1, P2 Y P4 A MEMORIA ----------------

INSTANTE: 2
ESTADOS DE LOS PROCESOS:
- EJECUTANDOSE: P2
- LISTOS: P1, P4
- LISTOS Y SUSPENDIDOS: P3, P7
- NUEVOS:
- SIN ARRIBAR: P5, P6, P8, P9, P10
- TERMINADOS:


┌───────────┬────────────────────┬───────────────────────┬──────────────┐
│ PARTICIÓN │     CONTENIDO      │ TAMAÑO PARTICIÓN      │ FI/FE/EL     │
├───────────┼────────────────────┼───────────────────────┼──────────────┤
│     0     │ Sistema operativo  │       100 KB          │ FI: 0 KB     │
│     1     │   P1(200 KB)       │       250 KB          │ FI: 50 KB    │
│     2     │    P2(50 KB)       │       120 KB          │ FI: 70 KB    │
│     3     │    P4(50 KB)       │        60 KB          │ FI: 10 KB    │
└───────────┴────────────────────┴───────────────────────┴──────────────┘


PRESIONE ENTER PARA CONTINUAR
