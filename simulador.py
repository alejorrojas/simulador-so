"""
Módulo principal del simulador de memoria y planificación de procesos.
"""

from typing import List, Optional, Tuple
from proceso import Proceso, EstadoProceso
from gestor_memoria import GestorMemoria
from planificador import Planificador
from formato_salida import FormateadorSalida
from lector_csv import LectorCSV


class Simulador:
    """
    Simulador de asignación de memoria y planificación de procesos.
    
    Coordina el gestor de memoria (Best-Fit) y el planificador de CPU (SRTF)
    para simular el ciclo de vida completo de los procesos.
    
    Atributos:
        procesos: Lista de todos los procesos del sistema
        gestor_memoria: Gestor de memoria con particiones fijas
        planificador: Planificador de CPU con SRTF
        tiempo_actual: Tiempo actual de la simulación
        formateador: Formateador para mostrar salidas
        cola_nuevos: Cola de procesos que han arribado pero no tienen memoria
    """
    
    def __init__(self):
        """Inicializa el simulador con componentes vacíos."""
        self.procesos: List[Proceso] = []
        self.gestor_memoria = GestorMemoria()
        self.planificador = Planificador()
        self.tiempo_actual = 0
        self.formateador = FormateadorSalida()
        self._simulacion_iniciada = False
        self.cola_nuevos: List[Proceso] = []
    
    def cargar_procesos(self, ruta_archivo: str):
        """
        Carga los procesos desde un archivo CSV.
        
        Args:
            ruta_archivo: Ruta al archivo CSV con los procesos
        """
        self.procesos = LectorCSV.leer_procesos(ruta_archivo)
        
        # Todos los procesos inician en estado SIN_ARRIBAR
        for proceso in self.procesos:
            proceso.estado = EstadoProceso.SIN_ARRIBAR
    
    def _obtener_procesos_por_estado(self, estado: EstadoProceso) -> List[Proceso]:
        """
        Obtiene la lista de procesos en un estado específico.
        
        Args:
            estado: Estado a filtrar
            
        Returns:
            Lista de procesos en ese estado
        """
        return [p for p in self.procesos if p.estado == estado]
    
    def _obtener_procesos_sin_arribar(self) -> List[Proceso]:
        """Obtiene procesos que aún no han arribado."""
        return [p for p in self.procesos 
                if p.estado == EstadoProceso.SIN_ARRIBAR]
    
    def _obtener_procesos_nuevos(self) -> List[Proceso]:
        """Obtiene procesos en estado nuevo (en cola de nuevos)."""
        return self.cola_nuevos.copy()
    
    def _obtener_procesos_terminados(self) -> List[Proceso]:
        """Obtiene procesos terminados."""
        return self._obtener_procesos_por_estado(EstadoProceso.TERMINADO)
    
    def mostrar_estado(self, mensaje_evento: str = None):
        """
        Muestra el estado actual del sistema.
        
        Args:
            mensaje_evento: Mensaje opcional describiendo el evento actual
        """
        if mensaje_evento:
            self.formateador.mostrar_evento(mensaje_evento)
        
        if self._simulacion_iniciada:
            self.formateador.mostrar_instante(self.tiempo_actual)
        
        self.formateador.mostrar_estados_procesos(
            proceso_ejecutando=self.planificador.obtener_proceso_ejecutando(),
            cola_listos=self.planificador.obtener_cola_listos(),
            cola_suspendidos=self.planificador.obtener_cola_suspendidos(),
            procesos_nuevos=self._obtener_procesos_nuevos(),
            procesos_sin_arribar=self._obtener_procesos_sin_arribar(),
            procesos_terminados=self._obtener_procesos_terminados()
        )
        
        self.formateador.mostrar_tabla_particiones(
            self.gestor_memoria.obtener_particiones()
        )
    
    def _procesar_arribos(self) -> List[Proceso]:
        """
        Procesa los procesos que arriban en el tiempo actual.
        Los procesos pasan a estado NUEVO y se agregan a la cola de nuevos.
        
        Returns:
            Lista de procesos que arribaron
        """
        procesos_arribados = []
        
        for proceso in self.procesos:
            if (proceso.estado == EstadoProceso.SIN_ARRIBAR and 
                proceso.tiempo_arribo == self.tiempo_actual):
                
                proceso.estado = EstadoProceso.NUEVO
                self.cola_nuevos.append(proceso)
                procesos_arribados.append(proceso)
        
        return procesos_arribados
    
    def _intentar_asignar_memoria_desde_colas(self) -> Tuple[List[Proceso], List[Proceso]]:
        """
        Intenta asignar memoria a procesos desde cola de nuevos y suspendidos.
        Según el flowchart, se toman procesos de NUEVOS o LISTOS/SUSPENDIDOS
        según prioridad mientras el grado de multiprogramación < 5.
        
        Returns:
            Tupla (procesos_asignados, procesos_suspendidos)
        """
        asignados = []
        suspendidos_nuevos = []
        
        # Procesar cola de nuevos primero (tienen prioridad según arribo)
        while self.cola_nuevos:
            # Verificar grado de multiprogramación
            if self.gestor_memoria.contar_procesos_en_memoria() >= self.gestor_memoria.grado_multiprogramacion:
                # No hay espacio por grado de multiprogramación
                # Mover restantes a suspendidos
                for proceso in self.cola_nuevos:
                    self.planificador.agregar_suspendido(proceso, self.tiempo_actual)
                    suspendidos_nuevos.append(proceso)
                self.cola_nuevos.clear()
                break
            
            proceso = self.cola_nuevos[0]
            
            # Intentar asignar memoria (Best-Fit)
            if self.gestor_memoria.asignar_proceso(proceso):
                self.cola_nuevos.pop(0)
                self.planificador.agregar_listo(proceso, self.tiempo_actual)
                asignados.append(proceso)
            else:
                # No hay partición adecuada, mover a suspendidos
                self.cola_nuevos.pop(0)
                self.planificador.agregar_suspendido(proceso, self.tiempo_actual)
                suspendidos_nuevos.append(proceso)
        
        return asignados, suspendidos_nuevos
    
    def _promover_suspendidos(self) -> List[Proceso]:
        """
        Intenta promover procesos suspendidos a listos si hay espacio.
        
        Returns:
            Lista de procesos promovidos
        """
        promovidos = []
        
        while self.planificador.cola_listos_suspendidos:
            # Verificar grado de multiprogramación
            if self.gestor_memoria.contar_procesos_en_memoria() >= self.gestor_memoria.grado_multiprogramacion:
                break
            
            # Verificar si hay espacio en memoria para el primer suspendido
            proceso_candidato = self.planificador.cola_listos_suspendidos[0]
            
            if self.gestor_memoria.asignar_proceso(proceso_candidato):
                # Remover de suspendidos y agregar a listos
                self.planificador.cola_listos_suspendidos.pop(0)
                self.planificador.agregar_listo(proceso_candidato, self.tiempo_actual)
                promovidos.append(proceso_candidato)
            else:
                # No hay partición adecuada para este proceso
                # Intentar con el siguiente (podría haber uno más pequeño)
                encontrado = False
                for i, proceso in enumerate(self.planificador.cola_listos_suspendidos[1:], 1):
                    if self.gestor_memoria.asignar_proceso(proceso):
                        self.planificador.cola_listos_suspendidos.pop(i)
                        self.planificador.agregar_listo(proceso, self.tiempo_actual)
                        promovidos.append(proceso)
                        encontrado = True
                        break
                
                if not encontrado:
                    # No se puede promover ninguno, salir
                    break
        
        return promovidos
    
    def _calcular_tiempo_siguiente_evento(self) -> Optional[int]:
        """
        Calcula el tiempo del siguiente evento importante.
        
        Returns:
            Tiempo del siguiente evento, o None si no hay más eventos
        """
        tiempos_posibles = []
        
        # Tiempo del próximo arribo
        for proceso in self.procesos:
            if proceso.estado == EstadoProceso.SIN_ARRIBAR:
                if proceso.tiempo_arribo > self.tiempo_actual:
                    tiempos_posibles.append(proceso.tiempo_arribo)
        
        # Tiempo de finalización del proceso actual
        proceso_actual = self.planificador.obtener_proceso_ejecutando()
        if proceso_actual:
            tiempo_fin = self.tiempo_actual + proceso_actual.tiempo_restante
            tiempos_posibles.append(tiempo_fin)
        
        if tiempos_posibles:
            return min(tiempos_posibles)
        
        return None
    
    def _hay_procesos_pendientes(self) -> bool:
        """
        Verifica si hay procesos pendientes de procesar.
        
        Returns:
            True si hay procesos sin terminar
        """
        for proceso in self.procesos:
            if proceso.estado != EstadoProceso.TERMINADO:
                return True
        return False
    
    def simular(self):
        """
        Ejecuta la simulación completa.
        
        La simulación avanza en eventos discretos (arribos y finalizaciones),
        mostrando el estado del sistema en cada evento.
        """
        self._simulacion_iniciada = False
        
        # Mostrar estado inicial
        self.formateador.mostrar_titulo("ESTADO INICIAL DE LA MEMORIA")
        self.mostrar_estado()
        self.formateador.esperar_entrada()
        
        self._simulacion_iniciada = True
        
        # Procesar arribos en tiempo 0 antes del bucle principal
        hay_arribos_iniciales = any(
            p.estado == EstadoProceso.SIN_ARRIBAR and p.tiempo_arribo == 0
            for p in self.procesos
        )
        
        if hay_arribos_iniciales:
            procesos_arribados = self._procesar_arribos()
            asignados, suspendidos = self._intentar_asignar_memoria_desde_colas()
            self.planificador.seleccionar_siguiente(self.tiempo_actual)
            
            if asignados:
                ids_asignados = ", ".join([p.id_proceso for p in asignados])
                if suspendidos:
                    ids_suspendidos = ", ".join([p.id_proceso for p in suspendidos])
                    mensaje = f"SE ASIGNARON {ids_asignados} A MEMORIA - SUSPENDIDOS: {ids_suspendidos}"
                else:
                    mensaje = f"SE ASIGNARON {ids_asignados} A MEMORIA"
            elif suspendidos:
                ids_suspendidos = ", ".join([p.id_proceso for p in suspendidos])
                mensaje = f"ARRIBARON {ids_suspendidos} (SIN MEMORIA DISPONIBLE)"
            else:
                ids_arribados = ", ".join([p.id_proceso for p in procesos_arribados])
                mensaje = f"ARRIBARON {ids_arribados}"
            
            self.mostrar_estado(mensaje)
            self.formateador.esperar_entrada()
        
        while self._hay_procesos_pendientes():
            # Calcular tiempo del siguiente evento
            tiempo_siguiente = self._calcular_tiempo_siguiente_evento()
            
            if tiempo_siguiente is None:
                break
            
            # Determinar qué tipo de evento ocurre
            hay_arribos = any(
                p.estado == EstadoProceso.SIN_ARRIBAR and p.tiempo_arribo == tiempo_siguiente
                for p in self.procesos
            )
            
            proceso_actual = self.planificador.obtener_proceso_ejecutando()
            proceso_termina = (
                proceso_actual and 
                self.tiempo_actual + proceso_actual.tiempo_restante == tiempo_siguiente
            )
            
            # Avanzar tiempo y ejecutar proceso si corresponde
            if proceso_actual and self.tiempo_actual < tiempo_siguiente:
                tiempo_ejecucion = tiempo_siguiente - self.tiempo_actual
                proceso_actual.tiempo_restante -= tiempo_ejecucion
            
            self.tiempo_actual = tiempo_siguiente
            
            # Procesar finalización si corresponde (primero las finalizaciones)
            if proceso_termina and proceso_actual.tiempo_restante <= 0:
                proceso_terminado = self.planificador.finalizar_proceso_actual(self.tiempo_actual)
                self.gestor_memoria.liberar_particion(proceso_terminado)
                
                # Intentar promover suspendidos
                promovidos = self._promover_suspendidos()
                
                # Seleccionar siguiente proceso
                self.planificador.seleccionar_siguiente(self.tiempo_actual)
                
                # Construir mensaje del evento
                mensaje = f"TERMINÓ {proceso_terminado.id_proceso}"
                if promovidos:
                    ids_promovidos = ", ".join([p.id_proceso for p in promovidos])
                    mensaje += f" - SE PROMOVIERON: {ids_promovidos}"
                
                self.mostrar_estado(mensaje)
                self.formateador.esperar_entrada()
            
            # Procesar arribos
            if hay_arribos:
                procesos_arribados = self._procesar_arribos()
                
                # Intentar asignar memoria a los nuevos procesos
                asignados, suspendidos = self._intentar_asignar_memoria_desde_colas()
                
                # Verificar preemption con SRTF
                self.planificador.seleccionar_siguiente(self.tiempo_actual)
                
                # Construir mensaje del evento
                if asignados:
                    ids_asignados = ", ".join([p.id_proceso for p in asignados])
                    if suspendidos:
                        ids_suspendidos = ", ".join([p.id_proceso for p in suspendidos])
                        mensaje = f"SE ASIGNARON {ids_asignados} A MEMORIA - SUSPENDIDOS: {ids_suspendidos}"
                    else:
                        mensaje = f"SE ASIGNARON {ids_asignados} A MEMORIA"
                elif suspendidos:
                    ids_suspendidos = ", ".join([p.id_proceso for p in suspendidos])
                    mensaje = f"ARRIBARON {ids_suspendidos} (SIN MEMORIA DISPONIBLE)"
                else:
                    ids_arribados = ", ".join([p.id_proceso for p in procesos_arribados])
                    mensaje = f"ARRIBARON {ids_arribados}"
                
                self.mostrar_estado(mensaje)
                self.formateador.esperar_entrada()
        
        # Mostrar estadísticas finales
        self.formateador.mostrar_estadisticas_finales(
            self._obtener_procesos_terminados(),
            self.tiempo_actual
        )
    
    def ejecutar(self, ruta_archivo: str):
        """
        Ejecuta el simulador completo.
        
        Args:
            ruta_archivo: Ruta al archivo CSV con los procesos
        """
        self.formateador.mostrar_bienvenida()
        
        try:
            self.cargar_procesos(ruta_archivo)
            self.formateador.mostrar_procesos_cargados(self.procesos)
            self.formateador.esperar_entrada()
            self.simular()
        except FileNotFoundError as e:
            print(f"\nError: {e}")
            print("Por favor, verifique que el archivo existe.")
        except ValueError as e:
            print(f"\nError en el archivo de entrada: {e}")

