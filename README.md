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

## Ejecutables

Puedes usar los ejecutables precompilados disponibles en la carpeta [`dist/`](dist/).

### Ejecutables disponibles

| Plataforma | Archivo |
|------------|---------|
| Linux (x64) | [`simulador-memoria-linux-x86_64`](dist/simulador-memoria-linux-x86_64) |
| Linux (ARM64) | [`simulador-memoria-linux-arm64`](dist/simulador-memoria-linux-arm64) |
| Windows | [`simulador-memoria-windows.exe`](dist/simulador-memoria-windows.exe) |
| macOS (Apple Silicon) | [`simulador-memoria-macos-arm`](dist/simulador-memoria-macos-arm) |

### Cómo ejecutar

**Windows:**
```bash
simulador-memoria-windows.exe
```

**macOS:**
```bash
./simulador-memoria-macos-arm
```

**Linux:**
```bash
./simulador-memoria-linux
```

**Nota:** En Linux y macOS, asegúrate de que el ejecutable tenga permisos de ejecución.


### Cargar archivo de procesos en los ejecutables

Al ejecutar el programa, busca automáticamente un archivo `procesos.csv` en el directorio de trabajo actual. Si no lo encuentra, puedes ingresar la ruta del archivo manualmente.

**Ejemplos de rutas según dónde ejecutes el programa:**

- Puedes usar rutas absolutas:
  ```
  /ruta/completa/al/archivo/procesos.csv
  ```

- También puedes usar rutas relativas desde donde ejecutas:
  ```
  ./procesos.csv
  ```

## Correr el proyecto local

### Requisitos

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 

### Con uv

```bash
uv sync
```

## Uso

```bash
uv run python src/main.py
```

El programa iniciará un menú interactivo con las siguientes opciones:

1. **Cargar archivo de procesos (CSV)**: Permite cargar un archivo CSV con los procesos a simular. Si existe un archivo `procesos.csv` en el directorio actual, se puede usar presionando Enter.
2. **Ver procesos cargados**: Muestra una tabla con todos los procesos cargados y sus características.
3. **Iniciar simulación**: Ejecuta la simulación con los procesos cargados.
4. **Salir**: Finaliza el programa.

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

Se incluye un archivo de ejemplo `procesos.csv` en la carpeta `./src/tests`.

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

El proyecto está organizado en módulos separados por responsabilidad:

```
so-kernel/
├── src/                 # Código fuente del proyecto
│   ├── entities/        # Clases de dominio/entidades
│   │   ├── __init__.py
│   │   ├── proceso.py       # Clase Proceso y estados
│   │   └── particion.py     # Clase Partición de memoria
│   ├── core/            # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── gestor_memoria.py    # Gestor de memoria (Best-Fit)
│   │   ├── planificador.py      # Planificador de CPU (SRTF)
│   │   └── simulador.py         # Lógica principal de simulación
│   ├── utils/           # Utilidades y helpers
│   │   ├── __init__.py
│   │   ├── lector_csv.py        # Lectura de archivos CSV
│   │   ├── formato_salida.py    # Formateo de salida
│   │   └── menu_principal.py    # Menú interactivo de usuario
│   ├── main.py          # Punto de entrada principal
│   └── tests/           # Archivos de prueba
│       └── procesos.csv  # Archivo de ejemplo
├── pyproject.toml       # Configuración del proyecto
└── README.md            # Este archivo
```

### Organización por módulos

- **`src/entities/`**: Contiene las clases que representan las entidades del dominio del sistema (Proceso, Partición)
- **`src/core/`**: Contiene la lógica de negocio principal (gestión de memoria, planificación, simulación)
- **`src/utils/`**: Contiene utilidades y funciones auxiliares (lectura de archivos, formateo de salida, menú interactivo)
- **`src/main.py`**: Punto de entrada que inicializa y ejecuta el menú principal

