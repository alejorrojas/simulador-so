"""
Módulo para formatear la salida del simulador en terminal.
"""

from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from entities.proceso import Proceso, EstadoProceso
from entities.particion import Particion

# Consola global para todo el módulo
console = Console()

class FormateadorSalida:
    # Colores para los diferentes estados
    COLOR_EJECUTANDO = "bold green"
    COLOR_LISTOS = "yellow"
    COLOR_SUSPENDIDOS = "cyan"
    COLOR_NUEVOS = "magenta"
    COLOR_SIN_ARRIBAR = "dim"
    COLOR_TERMINADOS = "blue"
    COLOR_LIBRE = "dim green"
    COLOR_SO = "bold red"
    COLOR_OCUPADO = "bold white"
    
    @staticmethod
    def limpiar_pantalla():
        console.print("\n" * 2)
    
    @staticmethod
    def mostrar_titulo(titulo: str):
        console.print()
        console.rule(f"[bold cyan]{titulo}[/bold cyan]", style="cyan")
        console.print()
    
    @staticmethod
    def mostrar_estados_procesos(
        proceso_ejecutando: Optional[Proceso],
        cola_listos: List[Proceso],
        cola_suspendidos: List[Proceso],
        procesos_nuevos: List[Proceso],
        procesos_sin_arribar: List[Proceso],
        procesos_terminados: List[Proceso]
    ):
        console.print("[bold]ESTADOS DE LOS PROCESOS:[/bold]")
        
        if proceso_ejecutando:
            console.print(f"  • EJECUTÁNDOSE: [{FormateadorSalida.COLOR_EJECUTANDO}]{proceso_ejecutando.id_proceso}[/]")
        else:
            console.print("  • EJECUTÁNDOSE: [dim]No hay procesos ejecutándose[/dim]")
        
        # Listos
        ids_listos = [p.id_proceso for p in cola_listos]
        if ids_listos:
            console.print(f"  • LISTOS: [{FormateadorSalida.COLOR_LISTOS}]{', '.join(ids_listos)}[/]")
        else:
            console.print("  • LISTOS: [dim]-[/dim]")
        
        # Listos y Suspendidos
        ids_suspendidos = [p.id_proceso for p in cola_suspendidos]
        if ids_suspendidos:
            console.print(f"  • LISTOS Y SUSPENDIDOS: [{FormateadorSalida.COLOR_SUSPENDIDOS}]{', '.join(ids_suspendidos)}[/]")
        else:
            console.print("  • LISTOS Y SUSPENDIDOS: [dim]-[/dim]")
        
        # Nuevos
        ids_nuevos = [p.id_proceso for p in procesos_nuevos]
        if ids_nuevos:
            console.print(f"  • NUEVOS: [{FormateadorSalida.COLOR_NUEVOS}]{', '.join(ids_nuevos)}[/]")
        else:
            console.print("  • NUEVOS: [dim]-[/dim]")
        
        # Sin arribar
        ids_sin_arribar = [p.id_proceso for p in procesos_sin_arribar]
        if ids_sin_arribar:
            console.print(f"  • SIN ARRIBAR: [{FormateadorSalida.COLOR_SIN_ARRIBAR}]{', '.join(ids_sin_arribar)}[/]")
        else:
            console.print("  • SIN ARRIBAR: [dim]-[/dim]")
        
        # Terminados
        ids_terminados = [p.id_proceso for p in procesos_terminados]
        if ids_terminados:
            console.print(f"  • TERMINADOS: [{FormateadorSalida.COLOR_TERMINADOS}]{', '.join(ids_terminados)}[/]")
        else:
            console.print("  • TERMINADOS: [dim]-[/dim]")
        
        console.print()
    
    @staticmethod
    def mostrar_tabla_particiones(particiones: List[Particion]):
        table = Table(
            title="[bold]MEMORIA[/bold]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("PARTICIÓN", justify="center", style="cyan", width=12)
        table.add_column("CONTENIDO", justify="center", width=18)
        table.add_column("TAMAÑO", justify="center", style="yellow", width=15)
        table.add_column("FI/FE/EL", justify="center", width=12)
        
        for particion in particiones:
            contenido = particion.obtener_contenido()
            
            if contenido == "S.O.":
                estilo_contenido = FormateadorSalida.COLOR_SO
            elif contenido == "LIBRE":
                estilo_contenido = FormateadorSalida.COLOR_LIBRE
            else:
                estilo_contenido = FormateadorSalida.COLOR_OCUPADO
            
            fi_estado = particion.obtener_estado_fragmentacion()
            if "FI" in fi_estado:
                estilo_fi = "red"
            elif "FE" in fi_estado:
                estilo_fi = "yellow"
            else:
                estilo_fi = "dim"
            
            table.add_row(
                str(particion.id_particion),
                f"[{estilo_contenido}]{contenido}[/]",
                f"{particion.tamaño} KB",
                f"[{estilo_fi}]{fi_estado}[/]"
            )
        
        console.print(table)
        console.print()
    
    @staticmethod
    def mostrar_instante(tiempo: int):
        console.print(f"[bold blue]INSTANTE:[/bold blue] [bold white]{tiempo}[/bold white]\n")
    
    @staticmethod
    def mostrar_grado_multiprogramacion(actual: int, maximo: int):
        if actual == 0:
            color = "dim"
        elif actual < maximo:
            color = "green"
        else:
            color = "yellow"
        
        barra_llena = "█" * actual
        barra_vacia = "░" * (maximo - actual)
        barra = f"[{color}]{barra_llena}[/][dim]{barra_vacia}[/dim]"
        
        console.print(f"[bold]GRADO DE MULTIPROGRAMACIÓN:[/bold] [{color}]{actual}[/]/{maximo} {barra}\n")
    
    @staticmethod
    def mostrar_evento(mensaje: str):
        console.print()
        console.rule(f"[bold yellow]{mensaje}[/bold yellow]", style="yellow")
        console.print()
    
    @staticmethod
    def esperar_entrada():
        console.print()
        console.input("[dim]PRESIONE ENTER PARA CONTINUAR[/dim] ")
        console.print()
    
    @staticmethod
    def mostrar_estadisticas_finales(procesos_terminados: List[Proceso], tiempo_total: int):
        console.print()
        console.rule("[bold green]ESTADÍSTICAS FINALES DE LA SIMULACIÓN[/bold green]", style="green")
        console.print()
        
        if not procesos_terminados:
            console.print("[yellow]No hay procesos terminados para mostrar estadísticas.[/yellow]")
            return
        
        table = Table(
            title="[bold]Tiempos por Proceso[/bold]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("Proceso", justify="center", style="white")
        table.add_column("T. Retorno", justify="right", style="green")
        table.add_column("T. Espera", justify="right", style="yellow")
        
        suma_retorno = 0
        suma_espera = 0
        
        for proceso in procesos_terminados:
            tiempo_retorno = proceso.calcular_tiempo_retorno()
            tiempo_espera = proceso.calcular_tiempo_espera()
            
            if tiempo_retorno is not None:
                suma_retorno += tiempo_retorno
            if tiempo_espera is not None:
                suma_espera += tiempo_espera
            
            table.add_row(
                proceso.id_proceso,
                str(tiempo_retorno) if tiempo_retorno is not None else "-",
                str(tiempo_espera) if tiempo_espera is not None else "-"
            )
        
        console.print(table)
        
        cantidad = len(procesos_terminados)
        promedio_retorno = suma_retorno / cantidad if cantidad > 0 else 0
        promedio_espera = suma_espera / cantidad if cantidad > 0 else 0
        
        console.print()
        console.print("\n[bold]PROMEDIOS[/bold]")
        console.print(f"  • Tiempo de retorno promedio: [green]{promedio_retorno:.2f}[/green]")
        console.print(f"  • Tiempo de espera promedio: [yellow]{promedio_espera:.2f}[/yellow]")
        console.print("\n[bold]RENDIMIENTO DEL SISTEMA[/bold]")
        console.print(f"  • Trabajos terminados: [cyan]{cantidad}[/cyan]")
        console.print(f"  • Tiempo total de simulación: [magenta]{tiempo_total}[/magenta]")
    
    @staticmethod
    def mostrar_bienvenida():
        console.print()
        console.print(Panel(
            "[bold white]SIMULADOR DE ASIGNACIÓN DE MEMORIA\n"
            "Y PLANIFICACIÓN DE PROCESOS[/bold white]",
            style="bold blue",
            width=70
        ))
        
        config_text = (
            "[bold]Configuración del sistema:[/bold]\n"
            "  • Asignación de memoria: [cyan]Particiones fijas con Best-Fit[/cyan]\n"
            "  • Planificación de CPU: [cyan]SRTF (Shortest Remaining Time First)[/cyan]\n"
            "  • Grado de multiprogramación: [cyan]5[/cyan]\n"
            "  • Particiones: [magenta]SO(100KB), 250KB, 150KB, 50KB[/magenta]"
        )
        console.print(Panel(config_text, border_style="dim"))
        console.print()
    
    @staticmethod
    def mostrar_procesos_cargados(procesos: List[Proceso]):
        table = Table(
            title="[bold]Procesos Cargados[/bold]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("ID", justify="center", style="white")
        table.add_column("Tamaño", justify="right", style="yellow")
        table.add_column("T. Arribo", justify="right", style="green")
        table.add_column("T. Irrupción", justify="right", style="magenta")
        
        for proceso in procesos:
            table.add_row(
                proceso.id_proceso,
                f"{proceso.tamaño} KB",
                str(proceso.tiempo_arribo),
                str(proceso.tiempo_irrupcion)
            )
        
        console.print(table)
        console.print(f"\n[dim]Total: {len(procesos)} procesos[/dim]\n")
