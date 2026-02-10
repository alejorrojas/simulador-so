"""
Módulo que define la clase Proceso para el simulador de memoria.
"""

from enum import Enum


class EstadoProceso(Enum):
    """Estados posibles de un proceso en el sistema."""
    NUEVO = "Nuevo"
    LISTO = "Listo"
    LISTO_SUSPENDIDO = "Listo y suspendido"
    EJECUCION = "Ejecución"
    TERMINADO = "Terminado"
    SIN_ARRIBAR = "Sin arribar"


class Proceso:
    """
    Representa un proceso en el sistema.
    
    Atributos:
        id_proceso: Identificador único del proceso
        tamaño: Tamaño del proceso en KB
        tiempo_arribo: Tiempo en que el proceso llega al sistema
        tiempo_irrupcion: Tiempo total de CPU que necesita el proceso
        tiempo_restante: Tiempo de CPU restante para completar
        estado: Estado actual del proceso
        tiempo_llegada_listo: Momento en que el proceso entró a la cola de listos
        tiempo_finalizacion: Momento en que el proceso terminó
        particion_asignada: Referencia a la partición de memoria asignada
        tiempo_espera_acumulado: Tiempo total esperando en colas
    """
    
    def __init__(self, id_proceso: str, tamaño: int, tiempo_arribo: int, tiempo_irrupcion: int):
        """
        Inicializa un nuevo proceso.
        
        Args:
            id_proceso: Identificador del proceso (ej: "P1")
            tamaño: Tamaño en KB
            tiempo_arribo: Tiempo de llegada al sistema
            tiempo_irrupcion: Tiempo de CPU necesario
        """
        self.id_proceso = id_proceso
        self.tamaño = tamaño
        self.tiempo_arribo = tiempo_arribo
        self.tiempo_irrupcion = tiempo_irrupcion
        self.tiempo_restante = tiempo_irrupcion
        self.estado = EstadoProceso.SIN_ARRIBAR
        self.tiempo_llegada_listo = None
        self.tiempo_finalizacion = None
        self.particion_asignada = None
        self.tiempo_espera_acumulado = 0
        self.ultimo_tiempo_espera_inicio = None
    
    def actualizar_estado(self, nuevo_estado: EstadoProceso, tiempo_actual: int = None):
        """
        Actualiza el estado del proceso y registra tiempos relevantes.
        
        Args:
            nuevo_estado: Nuevo estado del proceso
            tiempo_actual: Tiempo actual de la simulación
        """
        estado_anterior = self.estado
        self.estado = nuevo_estado
        
        # Si pasa a estado Listo, registrar tiempo para calcular espera
        if nuevo_estado == EstadoProceso.LISTO and tiempo_actual is not None:
            if self.tiempo_llegada_listo is None:
                self.tiempo_llegada_listo = tiempo_actual
            self.ultimo_tiempo_espera_inicio = tiempo_actual
        
        # Si pasa a ejecución desde listo, acumular tiempo de espera
        if nuevo_estado == EstadoProceso.EJECUCION and estado_anterior == EstadoProceso.LISTO:
            if self.ultimo_tiempo_espera_inicio is not None and tiempo_actual is not None:
                self.tiempo_espera_acumulado += tiempo_actual - self.ultimo_tiempo_espera_inicio
                self.ultimo_tiempo_espera_inicio = None
        
        # Si termina, registrar tiempo de finalización
        if nuevo_estado == EstadoProceso.TERMINADO and tiempo_actual is not None:
            self.tiempo_finalizacion = tiempo_actual
    
    def ejecutar(self, tiempo: int) -> bool:
        """
        Ejecuta el proceso por una unidad de tiempo.
        
        Args:
            tiempo: Unidades de tiempo a ejecutar
            
        Returns:
            True si el proceso terminó, False en caso contrario
        """
        self.tiempo_restante -= tiempo
        return self.tiempo_restante <= 0
    
    def calcular_tiempo_retorno(self) -> int:
        """
        Calcula el tiempo de retorno (turnaround time).
        
        Returns:
            Tiempo desde el arribo hasta la finalización
        """
        if self.tiempo_finalizacion is not None:
            return self.tiempo_finalizacion - self.tiempo_arribo
        return None
    
    def calcular_tiempo_espera(self) -> int:
        """
        Calcula el tiempo de espera total.
        
        Returns:
            Tiempo total esperando en colas (retorno - irrupción)
        """
        tiempo_retorno = self.calcular_tiempo_retorno()
        if tiempo_retorno is not None:
            return tiempo_retorno - self.tiempo_irrupcion
        return None
    
    def __str__(self) -> str:
        """Representación en string del proceso."""
        return f"{self.id_proceso}({self.tamaño} KB)"
    
    def __repr__(self) -> str:
        """Representación detallada del proceso."""
        return (f"Proceso(id={self.id_proceso}, tamaño={self.tamaño}KB, "
                f"arribo={self.tiempo_arribo}, irrupción={self.tiempo_irrupcion}, "
                f"restante={self.tiempo_restante}, estado={self.estado.value})")

