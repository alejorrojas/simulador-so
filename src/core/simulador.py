"""
Módulo principal del simulador de memoria y planificación de procesos. Coordina el gestor de memoria (Best-Fit) y el planificador de CPU (SRTF)
"""

from typing import List, Optional, Tuple
from rich.console import Console
from entities.proceso import Proceso, EstadoProceso
from core.gestor_memoria import GestorMemoria
from core.planificador import Planificador
from utils.formato_salida import FormateadorSalida
from utils.lector_csv import LectorCSV


# Consola global
console = Console()


class Simulador:
    
    def __init__(self):
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
    
    def _calcular_grado_multiprogramacion_actual(self) -> int:
        procesos_en_memoria = self.gestor_memoria.contar_procesos_en_memoria()
        procesos_suspendidos = len(self.planificador.obtener_cola_suspendidos())
        return procesos_en_memoria + procesos_suspendidos
    
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
        
        # Mostrar grado de multiprogramación actual
        # Incluye procesos en memoria y procesos en cola de listo y suspendido
        grado_actual = self._calcular_grado_multiprogramacion_actual()
        grado_maximo = self.gestor_memoria.grado_multiprogramacion
        self.formateador.mostrar_grado_multiprogramacion(grado_actual, grado_maximo)
        
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
        
        # Mostrar fragmentación externa si existe
        # Procesos esperando memoria = suspendidos + nuevos
        procesos_esperando = (
            self.planificador.obtener_cola_suspendidos() + 
            self._obtener_procesos_nuevos()
        )
        self.formateador.mostrar_fragmentacion_externa(
            self.gestor_memoria.obtener_particiones(),
            procesos_esperando
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
    
    def _intentar_asignar_memoria_desde_colas(self) -> Tuple[List[Proceso], List[Proceso], List[Proceso]]:
        """
        Intenta asignar memoria a procesos desde cola de nuevos.
        Según el flowchart, se toman procesos de NUEVOS mientras el 
        grado de multiprogramación < 5.
        
        NOTA: SRTF no se aplica a procesos que aún no están en memoria.
        Los procesos nuevos se ordenan por:
          1. Tiempo de arribo (FIFO para procesos que llegan en momentos diferentes)
          2. Tiempo de irrupción (para procesos que llegan al mismo tiempo)
        
        Esto permite que si varios procesos arriban simultáneamente (ej: t=0),
        se priorice el de menor tiempo de irrupción, pero una vez establecido
        el orden de arribo, se respeta FIFO.
        
        Returns:
            Tupla (procesos_asignados, procesos_suspendidos, procesos_en_cola_por_grado)
        """
        asignados = []
        suspendidos_nuevos = []
        procesos_en_cola_por_grado = []
        
        # Ordenar cola_nuevos por (tiempo_arribo, tiempo_irrupcion)
        # - Procesos con menor tiempo_arribo van primero (FIFO por arribo)
        # - Para procesos con MISMO tiempo_arribo, menor tiempo_irrupcion primero
        self.cola_nuevos.sort(key=lambda p: (p.tiempo_arribo, p.tiempo_irrupcion))
        
        # Procesar cola de nuevos
        while self.cola_nuevos:
            proceso = self.cola_nuevos[0]
            
            # Verificar grado de multiprogramación (incluye procesos en memoria y suspendidos)
            if self._calcular_grado_multiprogramacion_actual() >= self.gestor_memoria.grado_multiprogramacion:
                # No hay espacio por grado de multiprogramación
                # Dejar los procesos restantes en cola de nuevos (no mover a suspendidos)
                procesos_en_cola_por_grado = self.cola_nuevos.copy()
                break
            
            # Intentar asignar memoria (Best-Fit)
            if self.gestor_memoria.asignar_proceso(proceso):
                self.cola_nuevos.pop(0)
                self.planificador.agregar_listo(proceso, self.tiempo_actual)
                asignados.append(proceso)
            else:
                # No hay partición adecuada, mover a suspendidos
                # (ya verificamos el límite arriba, así que podemos agregarlo)
                self.cola_nuevos.pop(0)
                self.planificador.agregar_suspendido(proceso, self.tiempo_actual)
                suspendidos_nuevos.append(proceso)
        
        return asignados, suspendidos_nuevos, procesos_en_cola_por_grado
    
    def _promover_suspendidos(self) -> List[Proceso]:
        """
        Intenta promover procesos suspendidos a listos si hay espacio.
        
        Returns:
            Lista de procesos promovidos
        """
        promovidos = []
        
        while self.planificador.cola_listos_suspendidos:
            # Verificar grado de multiprogramación (incluye procesos en memoria y suspendidos)
            if self._calcular_grado_multiprogramacion_actual() >= self.gestor_memoria.grado_multiprogramacion:
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
            asignados, suspendidos, en_cola_por_grado = self._intentar_asignar_memoria_desde_colas()
            
            # Filtrar en_cola_por_grado para incluir solo procesos que arribaron en este instante
            en_cola_por_grado_este_instante = [
                p for p in en_cola_por_grado 
                if p in procesos_arribados
            ]
            
            self.planificador.seleccionar_siguiente(self.tiempo_actual)
            
            if asignados:
                mensaje_asignacion = self.formateador.mensaje_asignacion(asignados)
                if suspendidos:
                    mensaje_suspendido = self.formateador.mensaje_suspendido(suspendidos)
                    mensaje = f"{mensaje_asignacion} - {mensaje_suspendido}"
                elif en_cola_por_grado_este_instante:
                    mensaje_arribo = self.formateador.mensaje_arribo(en_cola_por_grado_este_instante)
                    mensaje = f"{mensaje_asignacion} - {mensaje_arribo} (GRADO DE MULTIPROGRAMACIÓN MÁXIMO ALCANZADO)"
                else:
                    mensaje = mensaje_asignacion
            elif suspendidos:
                mensaje_arribo = self.formateador.mensaje_arribo(suspendidos)
                mensaje = f"{mensaje_arribo} (SIN MEMORIA DISPONIBLE)"
            elif en_cola_por_grado_este_instante:
                mensaje_arribo = self.formateador.mensaje_arribo(en_cola_por_grado_este_instante)
                mensaje = f"{mensaje_arribo} (GRADO DE MULTIPROGRAMACIÓN MÁXIMO ALCANZADO)"
            else:
                mensaje = self.formateador.mensaje_arribo(procesos_arribados)
            
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
                
                # Intentar promover suspendidos primero (tienen prioridad)
                promovidos = self._promover_suspendidos()
                
                # Después de promover suspendidos, si todavía hay espacio,
                # intentar asignar memoria a procesos nuevos
                asignados_nuevos, suspendidos_nuevos, _ = self._intentar_asignar_memoria_desde_colas()
                
                # Seleccionar siguiente proceso
                self.planificador.seleccionar_siguiente(self.tiempo_actual)
                
                # Construir mensaje del evento
                mensaje = f"TERMINÓ {proceso_terminado.id_proceso}"
                if promovidos:
                    mensaje_promocion = self.formateador.mensaje_promocion(promovidos)
                    mensaje += f" - {mensaje_promocion}"
                if asignados_nuevos:
                    mensaje_asignacion = self.formateador.mensaje_asignacion(asignados_nuevos)
                    if promovidos:
                        mensaje += f" - {mensaje_asignacion}"
                    else:
                        mensaje = f"{mensaje} - {mensaje_asignacion}"
                
                self.mostrar_estado(mensaje)
                self.formateador.esperar_entrada()
            
            # Procesar arribos
            if hay_arribos:
                procesos_arribados = self._procesar_arribos()
                
                # Intentar asignar memoria a los nuevos procesos
                asignados, suspendidos, en_cola_por_grado = self._intentar_asignar_memoria_desde_colas()
                
                # Filtrar en_cola_por_grado para incluir solo procesos que arribaron en este instante
                en_cola_por_grado_este_instante = [
                    p for p in en_cola_por_grado 
                    if p in procesos_arribados
                ]
                
                # Verificar preemption con SRTF
                self.planificador.seleccionar_siguiente(self.tiempo_actual)
                
                # Construir mensaje del evento
                if asignados:
                    mensaje_asignacion = self.formateador.mensaje_asignacion(asignados)
                    if suspendidos:
                        mensaje_suspendido = self.formateador.mensaje_suspendido(suspendidos)
                        mensaje = f"{mensaje_asignacion} - {mensaje_suspendido}"
                    elif en_cola_por_grado_este_instante:
                        mensaje_arribo = self.formateador.mensaje_arribo(en_cola_por_grado_este_instante)
                        mensaje = f"{mensaje_asignacion} - {mensaje_arribo} (GRADO DE MULTIPROGRAMACIÓN MÁXIMO ALCANZADO)"
                    else:
                        mensaje = mensaje_asignacion
                elif suspendidos:
                    mensaje_arribo = self.formateador.mensaje_arribo(suspendidos)
                    mensaje = f"{mensaje_arribo} (SIN MEMORIA DISPONIBLE)"
                elif en_cola_por_grado_este_instante:
                    mensaje_arribo = self.formateador.mensaje_arribo(en_cola_por_grado_este_instante)
                    mensaje = f"{mensaje_arribo} (GRADO DE MULTIPROGRAMACIÓN MÁXIMO ALCANZADO)"
                else:
                    mensaje = self.formateador.mensaje_arribo(procesos_arribados)
                
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
            console.print(f"\n[red]Error:[/red] {e}")
            console.print("[dim]Por favor, verifique que el archivo existe.[/dim]")
        except ValueError as e:
            console.print(f"\n[red]Error en el archivo de entrada:[/red] {e}")

