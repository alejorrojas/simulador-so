# Archivos CSV de Prueba

Esta carpeta contiene archivos CSV para probar diferentes escenarios del simulador.

## Archivos disponibles

### 1. `fragmentacion_externa.csv`

**Objetivo**: Demostrar fragmentación externa

**Escenario**:
- P1 (200KB) → se asigna a partición grande (250KB), deja 50KB libres
- P2 (140KB) → se asigna a partición mediana (150KB), deja 10KB libres  
- P3 (40KB) → se asigna a partición pequeña (50KB), deja 10KB libres
- P4 (45KB) → se asigna a partición pequeña (50KB), deja 5KB libres
- P5 (180KB) → **NO puede entrar** porque aunque hay espacio total suficiente (50+10+10+5=75KB libres), está fragmentado en particiones pequeñas que no pueden alojar un proceso de 180KB

**Resultado esperado**: P5 queda suspendido o en cola de nuevos porque no hay una partición libre lo suficientemente grande para alojarlo, a pesar de haber espacio total disponible.

---

### 2. `fragmentacion_interna.csv`

**Objetivo**: Demostrar fragmentación interna

**Escenario**:
- Todos los procesos son de 50KB
- Se asignan a las particiones disponibles:
  - P1 → Partición grande (250KB): **200KB de fragmentación interna**
  - P2 → Partición mediana (150KB): **100KB de fragmentación interna**
  - P3 → Partición pequeña (50KB): **0KB de fragmentación interna**
  - P4 → Partición grande (250KB): **200KB de fragmentación interna** (si hay otra disponible)
  - P5 → Partición mediana (150KB): **100KB de fragmentación interna**

**Resultado esperado**: Se observa fragmentación interna significativa cuando procesos pequeños se asignan a particiones grandes o medianas, desperdiciando espacio dentro de cada partición.

---

### 3. `grado_multiprogramacion_5.csv`

**Objetivo**: Demostrar el límite de grado de multiprogramación (máximo 5 procesos)

**Escenario**:
- P1 (200KB, t=0) → entra a memoria
- P2 (50KB, t=0) → entra a memoria
- P3 (100KB, t=0) → entra a memoria
- P4 (140KB, t=0) → entra a memoria
- P5 (40KB, t=0) → entra a memoria
- **Grado de multiprogramación alcanzado: 5**
- P6 (180KB, t=1) → **NO puede entrar** (grado máximo alcanzado)
- P7 (45KB, t=1) → **NO puede entrar** (grado máximo alcanzado)
- P8 (120KB, t=2) → **NO puede entrar** (grado máximo alcanzado)

**Resultado esperado**: 
- Los primeros 5 procesos entran a memoria o quedan suspendidos (contando para el grado)
- Los procesos P6, P7 y P8 quedan en cola de nuevos o suspendidos porque el grado de multiprogramación ya alcanzó el máximo de 5
- Cuando un proceso termina y libera espacio, los procesos pendientes pueden entrar

---

## Cómo usar

Ejecuta el simulador y carga cualquiera de estos archivos:

```bash
uv run python src/main.py
```

Luego selecciona la opción 1 para cargar el archivo CSV deseado, por ejemplo:
- `csv/fragmentacion_externa.csv`
- `csv/fragmentacion_interna.csv`
- `csv/grado_multiprogramacion_5.csv`

## Notas

- **Particiones disponibles**:
  - Partición 0: 100KB (Sistema Operativo)
  - Partición 1: 250KB (Grande)
  - Partición 2: 150KB (Mediana)
  - Partición 3: 50KB (Pequeña)

- **Grado de multiprogramación máximo**: 5 procesos (incluyendo procesos en memoria y suspendidos)

- **Algoritmo de asignación**: Best-Fit (mejor ajuste)

