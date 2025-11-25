"""
Módulo que define la clase Particion para el simulador de memoria.
"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.proceso import Proceso

class Particion:
       
    def __init__(self, id_particion: int, direccion_inicio: int, tamaño: int, 
                 es_sistema_operativo: bool = False):
        self.id_particion = id_particion
        self.direccion_inicio = direccion_inicio
        self.tamaño = tamaño
        self.proceso_asignado: Optional['Proceso'] = None
        self.es_sistema_operativo = es_sistema_operativo
    
    def asignar_proceso(self, proceso: 'Proceso') -> bool:
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
        proceso = self.proceso_asignado
        if proceso is not None:
            proceso.particion_asignada = None
        self.proceso_asignado = None
        return proceso
    
    def esta_libre(self) -> bool:
        return self.proceso_asignado is None and not self.es_sistema_operativo
    
    def calcular_fragmentacion_interna(self) -> int:
        if self.es_sistema_operativo:
            return 0
        
        if self.proceso_asignado is None:
            return 0
        
        return self.tamaño - self.proceso_asignado.tamaño
    
    def obtener_contenido(self) -> str:
        if self.es_sistema_operativo:
            return "Sistema operativo"
        
        if self.proceso_asignado is None:
            return "-"
        
        return f"{self.proceso_asignado.id_proceso}({self.proceso_asignado.tamaño} KB)"
    
    def obtener_estado_fragmentacion(self) -> str:
        if self.es_sistema_operativo:
            return "FI: 0 KB"
        
        if self.proceso_asignado is None:
            return "Libre"
        
        fi = self.calcular_fragmentacion_interna()
        return f"FI: {fi} KB"
    
    def __str__(self) -> str:
        contenido = self.obtener_contenido()
        return f"Partición {self.id_particion}: {contenido} ({self.tamaño} KB)"
    
    def __repr__(self) -> str:
        return (f"Particion(id={self.id_particion}, dir={self.direccion_inicio}, "
                f"tamaño={self.tamaño}KB, proceso={self.proceso_asignado})")

