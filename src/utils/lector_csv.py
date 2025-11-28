"""
Módulo para leer procesos desde archivos CSV.
"""

import csv
from typing import List
from entities.proceso import Proceso

class LectorCSV:
    
    MAX_PROCESOS = 10
    
    @staticmethod
    def leer_procesos(ruta_archivo: str) -> List[Proceso]:
        
        procesos = []
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                # Verificar que las columnas requeridas existan
                columnas_requeridas = {'proceso_id', 't_arribo_al_sistema', 'memoria_K', 'tiempo_irrupcion'}
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
        
        procesos.sort(key=lambda p: p.tiempo_arribo)
        
        return procesos
    
    @staticmethod
    def _crear_proceso_desde_fila(fila: dict) -> Proceso:
        id_proceso = fila['proceso_id'].strip()
        
        if not id_proceso:
            raise ValueError("El proceso_id no puede estar vacío")
        
        try:
            tamaño = int(fila['memoria_K'].strip())
            tiempo_arribo = int(fila['t_arribo_al_sistema'].strip())
            tiempo_irrupcion = int(fila['tiempo_irrupcion'].strip())
        except ValueError:
            raise ValueError(
                "memoria_K, t_arribo_al_sistema y tiempo_irrupcion deben ser números enteros"
            )
        
        if tamaño <= 0:
            raise ValueError(f"La memoria_K debe ser positiva (proceso {id_proceso})")
        
        if tiempo_arribo < 0:
            raise ValueError(f"El tiempo de arribo al sistema no puede ser negativo (proceso {id_proceso})")
        
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
        try:
            procesos = LectorCSV.leer_procesos(ruta_archivo)
            return True, f"Archivo válido con {len(procesos)} procesos"
        except (FileNotFoundError, ValueError) as e:
            return False, str(e)

