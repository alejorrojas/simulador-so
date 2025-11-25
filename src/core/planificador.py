"""
Módulo que define el Planificador de CPU con algoritmo SRTF.
"""

from typing import List, Optional
from entities.proceso import Proceso, EstadoProceso


class Planificador:
    
    def __init__(self):
        self.cola_listos: List[Proceso] = []
        self.cola_listos_suspendidos: List[Proceso] = []
        self.proceso_ejecutando: Optional[Proceso] = None
    
    def agregar_listo(self, proceso: Proceso, tiempo_actual: int):
        """
        Agrega un proceso a la cola de listos.
        
        La cola se mantiene ordenada por tiempo restante (SRTF).
        
        Args:
            proceso: Proceso a agregar
            tiempo_actual: Tiempo actual de la simulación
        """
        proceso.actualizar_estado(EstadoProceso.LISTO, tiempo_actual)
        self.cola_listos.append(proceso)
        self._ordenar_cola_listos()
    
    def agregar_suspendido(self, proceso: Proceso, tiempo_actual: int):
        """
        Agrega un proceso a la cola de listos y suspendidos.
        
        Args:
            proceso: Proceso a suspender
            tiempo_actual: Tiempo actual de la simulación
        """
        proceso.actualizar_estado(EstadoProceso.LISTO_SUSPENDIDO, tiempo_actual)
        self.cola_listos_suspendidos.append(proceso)
    
    def _ordenar_cola_listos(self):
        """Ordena la cola de listos por tiempo restante (ascendente)."""
        self.cola_listos.sort(key=lambda p: p.tiempo_restante)
    
    def seleccionar_siguiente(self, tiempo_actual: int) -> Optional[Proceso]:
        """
        Selecciona el siguiente proceso a ejecutar según SRTF.
        
        Si hay un proceso ejecutando, verifica si debe ser preemptado
        por uno con menor tiempo restante.
        
        Args:
            tiempo_actual: Tiempo actual de la simulación
            
        Returns:
            El proceso seleccionado para ejecutar, o None si no hay ninguno
        """
        if not self.cola_listos and self.proceso_ejecutando is None:
            return None
        
        # Si no hay proceso ejecutando, tomar el primero de la cola
        if self.proceso_ejecutando is None:
            if self.cola_listos:
                self.proceso_ejecutando = self.cola_listos.pop(0)
                self.proceso_ejecutando.actualizar_estado(EstadoProceso.EJECUCION, tiempo_actual)
            return self.proceso_ejecutando
        
        # Verificar si hay preemption (SRTF)
        if self.cola_listos:
            proceso_candidato = self.cola_listos[0]
            if proceso_candidato.tiempo_restante < self.proceso_ejecutando.tiempo_restante:
                # Preemption: el proceso actual vuelve a la cola
                proceso_preemptado = self.proceso_ejecutando
                proceso_preemptado.actualizar_estado(EstadoProceso.LISTO, tiempo_actual)
                self.cola_listos.append(proceso_preemptado)
                self._ordenar_cola_listos()
                
                # El nuevo proceso toma el CPU
                self.proceso_ejecutando = self.cola_listos.pop(0)
                self.proceso_ejecutando.actualizar_estado(EstadoProceso.EJECUCION, tiempo_actual)
        
        return self.proceso_ejecutando
    
    def ejecutar_tick(self) -> bool:
        """
        Ejecuta un tick de tiempo del proceso actual.
        
        Returns:
            True si el proceso terminó, False en caso contrario
        """
        if self.proceso_ejecutando is None:
            return False
        
        return self.proceso_ejecutando.ejecutar(1)
    
    def finalizar_proceso_actual(self, tiempo_actual: int) -> Optional[Proceso]:
        """
        Finaliza el proceso actualmente en ejecución.
        
        Args:
            tiempo_actual: Tiempo actual de la simulación
            
        Returns:
            El proceso que terminó, o None si no había proceso ejecutando
        """
        if self.proceso_ejecutando is None:
            return None
        
        proceso_terminado = self.proceso_ejecutando
        proceso_terminado.actualizar_estado(EstadoProceso.TERMINADO, tiempo_actual)
        self.proceso_ejecutando = None
        
        return proceso_terminado
    
    def promover_suspendido(self, tiempo_actual: int) -> Optional[Proceso]:
        """
        Promueve un proceso de suspendido a listo.
        
        El proceso promovido es el primero de la cola (FIFO para suspendidos).
        
        Args:
            tiempo_actual: Tiempo actual de la simulación
            
        Returns:
            El proceso promovido, o None si no hay suspendidos
        """
        if not self.cola_listos_suspendidos:
            return None
        
        proceso = self.cola_listos_suspendidos.pop(0)
        self.agregar_listo(proceso, tiempo_actual)
        return proceso
    
    def obtener_proceso_ejecutando(self) -> Optional[Proceso]:
        """
        Obtiene el proceso actualmente en ejecución.
        
        Returns:
            El proceso en ejecución, o None si no hay ninguno
        """
        return self.proceso_ejecutando
    
    def obtener_cola_listos(self) -> List[Proceso]:
        """
        Obtiene la lista de procesos en cola de listos.
        
        Returns:
            Lista de procesos listos (ordenada por tiempo restante)
        """
        return self.cola_listos.copy()
    
    def obtener_cola_suspendidos(self) -> List[Proceso]:
        """
        Obtiene la lista de procesos suspendidos.
        
        Returns:
            Lista de procesos listos y suspendidos
        """
        return self.cola_listos_suspendidos.copy()
    
    def hay_procesos_pendientes(self) -> bool:
        """
        Verifica si hay procesos pendientes de ejecutar.
        
        Returns:
            True si hay procesos en cola de listos o ejecutando
        """
        return bool(self.cola_listos) or self.proceso_ejecutando is not None
    
    def remover_de_cola_listos(self, proceso: Proceso):
        """
        Remueve un proceso de la cola de listos.
        
        Args:
            proceso: Proceso a remover
        """
        if proceso in self.cola_listos:
            self.cola_listos.remove(proceso)
    
    def remover_de_suspendidos(self, proceso: Proceso):
        """
        Remueve un proceso de la cola de suspendidos.
        
        Args:
            proceso: Proceso a remover
        """
        if proceso in self.cola_listos_suspendidos:
            self.cola_listos_suspendidos.remove(proceso)
    
    def __str__(self) -> str:
        """Representación en string del estado del planificador."""
        lineas = ["Estado del Planificador:"]
        
        if self.proceso_ejecutando:
            lineas.append(f"  Ejecutando: {self.proceso_ejecutando.id_proceso}")
        else:
            lineas.append("  Ejecutando: Ninguno")
        
        listos = [p.id_proceso for p in self.cola_listos]
        lineas.append(f"  Cola Listos: {', '.join(listos) if listos else 'Vacía'}")
        
        suspendidos = [p.id_proceso for p in self.cola_listos_suspendidos]
        lineas.append(f"  Cola Suspendidos: {', '.join(suspendidos) if suspendidos else 'Vacía'}")
        
        return "\n".join(lineas)

