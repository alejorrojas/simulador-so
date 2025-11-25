# Simulador de Asignación de Memoria y Planificación de Procesos

Simulador interactivo que demuestra los conceptos de planificación de CPU y gestión de memoria con particiones fijas en un sistema de un solo procesador.

## Características

- **Asignación de memoria**: Particiones fijas con algoritmo **Best-Fit**
- **Planificación de CPU**: **SRTF** (Shortest Remaining Time First)
- **Grado de multiprogramación**: 5 procesos simultáneos en memoria
- **Máximo de procesos**: 10

### Particiones de memoria

| Partición | Tamaño | Uso |
|-----------|--------|-----|
| 0 | 100 KB | Sistema Operativo |
| 1 | 250 KB | Trabajos grandes |
| 2 | 150 KB | Trabajos medianos |
| 3 | 50 KB | Trabajos pequeños |

### Estados de los procesos

- **Sin arribar**: Aún no llegó al sistema
- **Nuevo**: Arribó pero no tiene memoria asignada
- **Listo**: En memoria, esperando CPU
- **Listo y suspendido**: Sin memoria, esperando asignación
- **Ejecución**: Usando el CPU
- **Terminado**: Finalizó su ejecución

## Instalación

### Requisitos

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recomendado)

### Con uv

```bash
uv sync
```

## Uso

```bash
uv run python main.py
```

El programa mostrará un menú interactivo donde podrás:

1. Cargar un archivo CSV con procesos
2. Ver los procesos cargados
3. Iniciar la simulación
4. Salir

## Formato del archivo CSV

El archivo de procesos debe tener el siguiente formato:

```csv
id_proceso,tamaño,tiempo_arribo,tiempo_irrupcion
P1,200,0,5
P2,50,1,3
P3,180,2,8
```

| Campo | Descripción |
|-------|-------------|
| `id_proceso` | Identificador único (ej: P1, P2) |
| `tamaño` | Tamaño del proceso en KB |
| `tiempo_arribo` | Instante en que llega al sistema |
| `tiempo_irrupcion` | Tiempo de CPU que necesita |

Se incluye un archivo de ejemplo `procesos.csv` en el repositorio.

## Salida del simulador

Durante la simulación se muestra en cada evento:

- Estado actual de todos los procesos
- Tabla de particiones de memoria con fragmentación interna
- Proceso en ejecución y colas de listos/suspendidos

Al finalizar:

- Tiempo de retorno y espera de cada proceso
- Promedios de tiempos
- Rendimiento del sistema

## Estructura del proyecto

```
so-kernel/
├── main.py              # Punto de entrada y menú principal
├── simulador.py         # Lógica principal de simulación
├── proceso.py           # Clase Proceso y estados
├── particion.py         # Clase Partición de memoria
├── gestor_memoria.py    # Gestor de memoria (Best-Fit)
├── planificador.py      # Planificador de CPU (SRTF)
├── lector_csv.py        # Lectura de archivos CSV
├── formato_salida.py    # Formateo de salida con Rich
├── procesos.csv         # Archivo de ejemplo
├── pyproject.toml       # Configuración del proyecto
└── CONSIGNA.md          # Consigna original del trabajo
```

