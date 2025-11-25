"""
Módulo para formatear la salida del simulador en terminal.
"""

from typing import List, Optional
from proceso import Proceso, EstadoProceso
from particion import Particion


class FormateadorSalida:
    """
    Clase para formatear y mostrar el estado del simulador en terminal.
    """
    
    # Anchos de columna para la tabla de particiones
    ANCHO_PARTICION = 11
    ANCHO_CONTENIDO = 20
    ANCHO_TAMAÑO = 23
    ANCHO_FI = 14
    
    @staticmethod
    def limpiar_pantalla():
        """Imprime líneas vacías para simular limpieza de pantalla."""
        print("\n" * 2)
    
    @staticmethod
    def mostrar_titulo(titulo: str):
        """
        Muestra un título centrado con decoración.
        
        Args:
            titulo: Texto del título a mostrar
        """
        linea = "-" * len(titulo)
        print(f"\n{linea} {titulo} {linea}\n")
    
    @staticmethod
    def mostrar_estados_procesos(
        proceso_ejecutando: Optional[Proceso],
        cola_listos: List[Proceso],
        cola_suspendidos: List[Proceso],
        procesos_nuevos: List[Proceso],
        procesos_sin_arribar: List[Proceso],
        procesos_terminados: List[Proceso]
    ):
        """
        Muestra el estado de todos los procesos organizados por categoría.
        
        Args:
            proceso_ejecutando: Proceso actualmente en CPU
            cola_listos: Lista de procesos listos
            cola_suspendidos: Lista de procesos suspendidos
            procesos_nuevos: Lista de procesos nuevos
            procesos_sin_arribar: Lista de procesos sin arribar
            procesos_terminados: Lista de procesos terminados
        """
        print("ESTADOS DE LOS PROCESOS:")
        
        # Ejecutando
        if proceso_ejecutando:
            print(f"- EJECUTANDOSE: {proceso_ejecutando.id_proceso}")
        else:
            print("- EJECUTANDOSE: No hay procesos ejecutandose")
        
        # Listos
        ids_listos = [p.id_proceso for p in cola_listos]
        print(f"- LISTOS: {', '.join(ids_listos) if ids_listos else ''}")
        
        # Listos y Suspendidos
        ids_suspendidos = [p.id_proceso for p in cola_suspendidos]
        print(f"- LISTOS Y SUSPENDIDOS: {', '.join(ids_suspendidos) if ids_suspendidos else ''}")
        
        # Nuevos
        ids_nuevos = [p.id_proceso for p in procesos_nuevos]
        print(f"- NUEVOS: {', '.join(ids_nuevos) if ids_nuevos else ''}")
        
        # Sin arribar
        ids_sin_arribar = [p.id_proceso for p in procesos_sin_arribar]
        print(f"- SIN ARRIBAR: {', '.join(ids_sin_arribar) if ids_sin_arribar else ''}")
        
        # Terminados
        ids_terminados = [p.id_proceso for p in procesos_terminados]
        print(f"- TERMINADOS: {', '.join(ids_terminados) if ids_terminados else ''}")
        
        print()
    
    @staticmethod
    def mostrar_tabla_particiones(particiones: List[Particion]):
        """
        Muestra la tabla de particiones de memoria con formato.
        
        Args:
            particiones: Lista de particiones a mostrar
        """
        # Encabezado de la tabla
        print("┌───────────┬────────────────────┬───────────────────────┬──────────────┐")
        print("│ PARTICIÓN │     CONTENIDO      │ TAMAÑO PARTICIÓN      │ FI/FE/EL     │")
        print("├───────────┼────────────────────┼───────────────────────┼──────────────┤")
        
        for particion in particiones:
            id_str = str(particion.id_particion).center(9)
            contenido = particion.obtener_contenido().center(18)
            tamaño_str = f"{particion.tamaño} KB".center(21)
            fi_str = particion.obtener_estado_fragmentacion().center(12)
            
            print(f"│ {id_str} │ {contenido} │ {tamaño_str} │ {fi_str} │")
        
        print("└───────────┴────────────────────┴───────────────────────┴──────────────┘")
        print()
    
    @staticmethod
    def mostrar_instante(tiempo: int):
        """
        Muestra el instante actual de la simulación.
        
        Args:
            tiempo: Tiempo actual
        """
        print(f"INSTANTE: {tiempo}")
    
    @staticmethod
    def mostrar_evento(mensaje: str):
        """
        Muestra un mensaje de evento con formato.
        
        Args:
            mensaje: Mensaje del evento
        """
        lineas = "-" * 16
        print(f"\n{lineas} {mensaje} {lineas}\n")
    
    @staticmethod
    def esperar_entrada():
        """Pausa la ejecución esperando que el usuario presione Enter."""
        input("\nPRESIONE ENTER PARA CONTINUAR\n")
    
    @staticmethod
    def mostrar_estadisticas_finales(procesos_terminados: List[Proceso], tiempo_total: int):
        """
        Muestra las estadísticas finales de la simulación.
        
        Args:
            procesos_terminados: Lista de procesos que terminaron
            tiempo_total: Tiempo total de la simulación
        """
        print("\n" + "=" * 60)
        print("ESTADÍSTICAS FINALES DE LA SIMULACIÓN")
        print("=" * 60)
        
        if not procesos_terminados:
            print("No hay procesos terminados para mostrar estadísticas.")
            return
        
        print("\nTiempos por proceso:")
        print("-" * 50)
        print(f"{'Proceso':<10} {'T. Retorno':<15} {'T. Espera':<15}")
        print("-" * 50)
        
        suma_retorno = 0
        suma_espera = 0
        
        for proceso in procesos_terminados:
            tiempo_retorno = proceso.calcular_tiempo_retorno()
            tiempo_espera = proceso.calcular_tiempo_espera()
            
            if tiempo_retorno is not None:
                suma_retorno += tiempo_retorno
            if tiempo_espera is not None:
                suma_espera += tiempo_espera
            
            print(f"{proceso.id_proceso:<10} {tiempo_retorno:<15} {tiempo_espera:<15}")
        
        cantidad = len(procesos_terminados)
        promedio_retorno = suma_retorno / cantidad if cantidad > 0 else 0
        promedio_espera = suma_espera / cantidad if cantidad > 0 else 0
        
        print("-" * 50)
        print(f"\nPROMEDIOS:")
        print(f"  - Tiempo de retorno promedio: {promedio_retorno:.2f}")
        print(f"  - Tiempo de espera promedio: {promedio_espera:.2f}")
        print(f"\nRENDIMIENTO DEL SISTEMA:")
        print(f"  - Trabajos terminados: {cantidad}")
        print(f"  - Tiempo total de simulación: {tiempo_total}")
        print("=" * 60)
    
    @staticmethod
    def mostrar_bienvenida():
        """Muestra mensaje de bienvenida al simulador."""
        print("\n" + "=" * 70)
        print("   SIMULADOR DE ASIGNACIÓN DE MEMORIA Y PLANIFICACIÓN DE PROCESOS")
        print("=" * 70)
        print("\nConfiguración del sistema:")
        print("  - Asignación de memoria: Particiones fijas con Best-Fit")
        print("  - Planificación de CPU: SRTF (Shortest Remaining Time First)")
        print("  - Grado de multiprogramación: 5")
        print("  - Particiones: SO(100KB), 250KB, 150KB, 50KB")
        print()
    
    @staticmethod
    def mostrar_procesos_cargados(procesos: List[Proceso]):
        """
        Muestra la lista de procesos cargados.
        
        Args:
            procesos: Lista de procesos cargados
        """
        print("Procesos cargados:")
        print("-" * 60)
        print(f"{'ID':<8} {'Tamaño':<12} {'T. Arribo':<12} {'T. Irrupción':<12}")
        print("-" * 60)
        
        for proceso in procesos:
            print(f"{proceso.id_proceso:<8} {proceso.tamaño:<12} "
                  f"{proceso.tiempo_arribo:<12} {proceso.tiempo_irrupcion:<12}")
        
        print("-" * 60)
        print(f"Total: {len(procesos)} procesos\n")

