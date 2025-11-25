"""
Módulo para leer procesos desde archivos CSV.
"""

import csv
from typing import List
from proceso import Proceso


class LectorCSV:
    """
    Clase para leer procesos desde archivos CSV.
    
    Formato esperado del CSV:
        id_proceso,tamaño,tiempo_arribo,tiempo_irrupcion
        P1,200,0,5
        P2,50,1,3
        ...
    """
    
    MAX_PROCESOS = 10
    
    @staticmethod
    def leer_procesos(ruta_archivo: str) -> List[Proceso]:
        """
        Lee procesos desde un archivo CSV.
        
        Args:
            ruta_archivo: Ruta al archivo CSV
            
        Returns:
            Lista de procesos leídos del archivo
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato del archivo es inválido o hay más de 10 procesos
        """
        procesos = []
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                # Verificar que las columnas requeridas existan
                columnas_requeridas = {'id_proceso', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'}
                if not columnas_requeridas.issubset(set(lector.fieldnames or [])):
                    raise ValueError(
                        f"El archivo CSV debe tener las columnas: {', '.join(columnas_requeridas)}"
                    )
                
                for numero_linea, fila in enumerate(lector, start=2):
                    try:
                        proceso = LectorCSV._crear_proceso_desde_fila(fila)
                        procesos.append(proceso)
                        
                        # Verificar máximo de procesos
                        if len(procesos) > LectorCSV.MAX_PROCESOS:
                            raise ValueError(
                                f"Se permiten máximo {LectorCSV.MAX_PROCESOS} procesos. "
                                f"El archivo contiene más."
                            )
                            
                    except (ValueError, KeyError) as e:
                        raise ValueError(
                            f"Error en línea {numero_linea} del archivo CSV: {e}"
                        )
        
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
        
        if not procesos:
            raise ValueError("El archivo CSV está vacío o no contiene procesos válidos")
        
        # Ordenar procesos por tiempo de arribo
        procesos.sort(key=lambda p: p.tiempo_arribo)
        
        return procesos
    
    @staticmethod
    def _crear_proceso_desde_fila(fila: dict) -> Proceso:
        """
        Crea un proceso a partir de una fila del CSV.
        
        Args:
            fila: Diccionario con los datos de la fila
            
        Returns:
            Objeto Proceso creado
            
        Raises:
            ValueError: Si los datos son inválidos
        """
        id_proceso = fila['id_proceso'].strip()
        
        if not id_proceso:
            raise ValueError("El id_proceso no puede estar vacío")
        
        try:
            tamaño = int(fila['tamaño'].strip())
            tiempo_arribo = int(fila['tiempo_arribo'].strip())
            tiempo_irrupcion = int(fila['tiempo_irrupcion'].strip())
        except ValueError:
            raise ValueError(
                "tamaño, tiempo_arribo y tiempo_irrupcion deben ser números enteros"
            )
        
        # Validaciones
        if tamaño <= 0:
            raise ValueError(f"El tamaño debe ser positivo (proceso {id_proceso})")
        
        if tiempo_arribo < 0:
            raise ValueError(f"El tiempo de arribo no puede ser negativo (proceso {id_proceso})")
        
        if tiempo_irrupcion <= 0:
            raise ValueError(f"El tiempo de irrupción debe ser positivo (proceso {id_proceso})")
        
        return Proceso(
            id_proceso=id_proceso,
            tamaño=tamaño,
            tiempo_arribo=tiempo_arribo,
            tiempo_irrupcion=tiempo_irrupcion
        )
    
    @staticmethod
    def validar_archivo(ruta_archivo: str) -> tuple[bool, str]:
        """
        Valida un archivo CSV sin cargar los procesos.
        
        Args:
            ruta_archivo: Ruta al archivo CSV
            
        Returns:
            Tupla (es_valido, mensaje) indicando si el archivo es válido
        """
        try:
            procesos = LectorCSV.leer_procesos(ruta_archivo)
            return True, f"Archivo válido con {len(procesos)} procesos"
        except (FileNotFoundError, ValueError) as e:
            return False, str(e)

