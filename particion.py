"""
Módulo que define la clase Particion para el simulador de memoria.
"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from proceso import Proceso


class Particion:
    """
    Representa una partición de memoria fija.
    
    Atributos:
        id_particion: Identificador de la partición
        direccion_inicio: Dirección de memoria donde comienza la partición
        tamaño: Tamaño total de la partición en KB
        proceso_asignado: Proceso actualmente asignado (None si está libre)
        es_sistema_operativo: Indica si es la partición del SO
    """
    
    def __init__(self, id_particion: int, direccion_inicio: int, tamaño: int, 
                 es_sistema_operativo: bool = False):
        """
        Inicializa una nueva partición de memoria.
        
        Args:
            id_particion: Identificador de la partición
            direccion_inicio: Dirección de inicio en KB
            tamaño: Tamaño de la partición en KB
            es_sistema_operativo: True si es la partición reservada para el SO
        """
        self.id_particion = id_particion
        self.direccion_inicio = direccion_inicio
        self.tamaño = tamaño
        self.proceso_asignado: Optional['Proceso'] = None
        self.es_sistema_operativo = es_sistema_operativo
    
    def asignar_proceso(self, proceso: 'Proceso') -> bool:
        """
        Asigna un proceso a esta partición.
        
        Args:
            proceso: Proceso a asignar
            
        Returns:
            True si se asignó correctamente, False si no hay espacio o está ocupada
        """
        if self.es_sistema_operativo:
            return False
        
        if not self.esta_libre():
            return False
        
        if proceso.tamaño > self.tamaño:
            return False
        
        self.proceso_asignado = proceso
        proceso.particion_asignada = self
        return True
    
    def liberar(self) -> Optional['Proceso']:
        """
        Libera la partición, removiendo el proceso asignado.
        
        Returns:
            El proceso que estaba asignado, o None si estaba libre
        """
        proceso = self.proceso_asignado
        if proceso is not None:
            proceso.particion_asignada = None
        self.proceso_asignado = None
        return proceso
    
    def esta_libre(self) -> bool:
        """
        Verifica si la partición está libre para asignar un proceso.
        
        Returns:
            True si está libre y no es del SO, False en caso contrario
        """
        return self.proceso_asignado is None and not self.es_sistema_operativo
    
    def calcular_fragmentacion_interna(self) -> int:
        """
        Calcula la fragmentación interna de la partición.
        
        Returns:
            Espacio no utilizado dentro de la partición (en KB).
            Retorna 0 si es del SO o está libre.
        """
        if self.es_sistema_operativo:
            return 0
        
        if self.proceso_asignado is None:
            return 0  # Está libre, se considera espacio libre no fragmentación
        
        return self.tamaño - self.proceso_asignado.tamaño
    
    def obtener_contenido(self) -> str:
        """
        Obtiene una descripción del contenido de la partición.
        
        Returns:
            String describiendo el contenido
        """
        if self.es_sistema_operativo:
            return "Sistema operativo"
        
        if self.proceso_asignado is None:
            return "-"
        
        return f"{self.proceso_asignado.id_proceso}({self.proceso_asignado.tamaño} KB)"
    
    def obtener_estado_fragmentacion(self) -> str:
        """
        Obtiene una descripción del estado de fragmentación.
        
        Returns:
            String describiendo la fragmentación o espacio libre
        """
        if self.es_sistema_operativo:
            return "FI: 0 KB"
        
        if self.proceso_asignado is None:
            return "Libre"
        
        fi = self.calcular_fragmentacion_interna()
        return f"FI: {fi} KB"
    
    def __str__(self) -> str:
        """Representación en string de la partición."""
        contenido = self.obtener_contenido()
        return f"Partición {self.id_particion}: {contenido} ({self.tamaño} KB)"
    
    def __repr__(self) -> str:
        """Representación detallada de la partición."""
        return (f"Particion(id={self.id_particion}, dir={self.direccion_inicio}, "
                f"tamaño={self.tamaño}KB, proceso={self.proceso_asignado})")

