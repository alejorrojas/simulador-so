"""
Módulo que define el Gestor de Memoria con particiones fijas y algoritmo Best-Fit.
"""

from typing import List, Optional
from entities.particion import Particion
from entities.proceso import Proceso


class GestorMemoria:
    
    # Configuración de particiones fijas (en KB)
    TAMAÑO_SO = 100        # Partición del Sistema Operativo
    TAMAÑO_GRANDE = 250    # Partición para trabajos grandes
    TAMAÑO_MEDIANO = 150   # Partición para trabajos medianos
    TAMAÑO_PEQUEÑO = 50    # Partición para trabajos pequeños
    
    GRADO_MULTIPROGRAMACION_MAX = 5
    
    def __init__(self):
        """Inicializa el gestor de memoria con las particiones fijas."""
        self.particiones: List[Particion] = []
        self.grado_multiprogramacion = self.GRADO_MULTIPROGRAMACION_MAX
        self._inicializar_particiones()
    
    def _inicializar_particiones(self):
        """Crea las particiones fijas de memoria."""
        direccion_actual = 0
        
        # Partición 0: Sistema Operativo (100K)
        particion_so = Particion(
            id_particion=0,
            direccion_inicio=direccion_actual,
            tamaño=self.TAMAÑO_SO,
            es_sistema_operativo=True
        )
        self.particiones.append(particion_so)
        direccion_actual += self.TAMAÑO_SO
        
        # Partición 1: Trabajos grandes (250K)
        particion_grande = Particion(
            id_particion=1,
            direccion_inicio=direccion_actual,
            tamaño=self.TAMAÑO_GRANDE
        )
        self.particiones.append(particion_grande)
        direccion_actual += self.TAMAÑO_GRANDE
        
        # Partición 2: Trabajos medianos (150K)
        particion_mediana = Particion(
            id_particion=2,
            direccion_inicio=direccion_actual,
            tamaño=self.TAMAÑO_MEDIANO
        )
        self.particiones.append(particion_mediana)
        direccion_actual += self.TAMAÑO_MEDIANO
        
        # Partición 3: Trabajos pequeños (50K)
        particion_pequeña = Particion(
            id_particion=3,
            direccion_inicio=direccion_actual,
            tamaño=self.TAMAÑO_PEQUEÑO
        )
        self.particiones.append(particion_pequeña)
    
    def best_fit(self, proceso: Proceso) -> Optional[Particion]:
        """
        Encuentra la mejor partición para un proceso usando Best-Fit.
        
        Best-Fit busca la partición libre más pequeña que pueda contener el proceso,
        minimizando así la fragmentación interna.
        
        Args:
            proceso: Proceso para el cual se busca partición
            
        Returns:
            La partición que mejor se ajusta, o None si no hay ninguna disponible
        """
        mejor_particion = None
        menor_desperdicio = float('inf')
        
        for particion in self.particiones:
            # Verificar que la partición esté libre y pueda contener el proceso
            if particion.esta_libre() and particion.tamaño >= proceso.tamaño:
                desperdicio = particion.tamaño - proceso.tamaño
                
                # Si encontramos una partición con menor desperdicio, la seleccionamos
                if desperdicio < menor_desperdicio:
                    menor_desperdicio = desperdicio
                    mejor_particion = particion
        
        return mejor_particion
    
    def asignar_proceso(self, proceso: Proceso) -> bool:
        """
        Intenta asignar un proceso a memoria usando Best-Fit.
        
        Args:
            proceso: Proceso a asignar
            
        Returns:
            True si se asignó correctamente, False si no hay espacio
        """
        # Verificar grado de multiprogramación
        if self.contar_procesos_en_memoria() >= self.grado_multiprogramacion:
            return False
        
        # Buscar la mejor partición
        particion = self.best_fit(proceso)
        
        if particion is None:
            return False
        
        # Asignar el proceso a la partición
        return particion.asignar_proceso(proceso)
    
    def liberar_particion(self, proceso: Proceso) -> bool:
        """
        Libera la partición asignada a un proceso.
        
        Args:
            proceso: Proceso cuya partición se liberará
            
        Returns:
            True si se liberó correctamente, False si el proceso no tenía partición
        """
        if proceso.particion_asignada is None:
            return False
        
        proceso.particion_asignada.liberar()
        return True
    
    def contar_procesos_en_memoria(self) -> int:
        """
        Cuenta el número de procesos actualmente en memoria.
        
        Returns:
            Número de particiones ocupadas (excluyendo SO)
        """
        contador = 0
        for particion in self.particiones:
            if not particion.es_sistema_operativo and particion.proceso_asignado is not None:
                contador += 1
        return contador
    
    def hay_espacio_disponible(self, proceso: Proceso) -> bool:
        """
        Verifica si hay espacio para un proceso sin asignarlo.
        
        Args:
            proceso: Proceso a verificar
            
        Returns:
            True si hay una partición disponible para el proceso
        """
        if self.contar_procesos_en_memoria() >= self.grado_multiprogramacion:
            return False
        
        return self.best_fit(proceso) is not None
    
    def obtener_particiones(self) -> List[Particion]:
        """
        Obtiene la lista de todas las particiones.
        
        Returns:
            Lista de particiones
        """
        return self.particiones
    
    def calcular_fragmentacion_interna_total(self) -> int:
        """
        Calcula la fragmentación interna total del sistema.
        
        Returns:
            Suma de fragmentación interna de todas las particiones ocupadas
        """
        total = 0
        for particion in self.particiones:
            total += particion.calcular_fragmentacion_interna()
        return total
    
    def __str__(self) -> str:
        """Representación en string del estado de memoria."""
        lineas = ["Estado de Memoria:"]
        for particion in self.particiones:
            lineas.append(f"  {particion}")
        return "\n".join(lineas)

