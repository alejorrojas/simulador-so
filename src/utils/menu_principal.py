"""
Módulo que contiene la clase MenuPrincipal para la interfaz de usuario.

Este módulo proporciona una interfaz de línea de comandos interactiva
para el simulador de asignación de memoria y planificación de procesos.
"""

import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from core.simulador import Simulador
from utils.lector_csv import LectorCSV
from utils.formato_salida import FormateadorSalida

# Instancia global de consola Rich para toda la aplicación
console = Console()


class MenuPrincipal:

    def __init__(self):
        self.ruta_archivo = None
        self.procesos_cargados = None
        self.formateador = FormateadorSalida()
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_encabezado(self):
        console.print()
        console.print(Panel(
            "[bold white]SIMULADOR DE ASIGNACIÓN DE MEMORIA\n"
            "Y PLANIFICACIÓN DE PROCESOS[/bold white]",
            style="bold blue",
            width=70
        ))
        
        # Texto descriptivo de la configuración del sistema
        config_text = (
            "[bold]Configuración del sistema:[/bold]\n"
            "  • Asignación de memoria: [cyan]Particiones fijas con Best-Fit[/cyan]\n"
            "  • Planificación de CPU: [cyan]SRTF (Shortest Remaining Time First)[/cyan]\n"
            "  • Grado de multiprogramación: [cyan]5[/cyan]\n"
            "  • Particiones: [magenta]SO(100KB), 250KB, 150KB, 50KB[/magenta]\n"
            "  • Máximo de procesos: [cyan]10[/cyan]"
        )
        console.print(Panel(config_text, border_style="dim"))
    
    def mostrar_menu(self): 
        console.print()
        console.rule("[bold cyan]MENÚ PRINCIPAL[/bold cyan]", style="cyan")
        
        # Mostrar estado del archivo cargado
        if self.ruta_archivo:
            console.print(f"\n  [green]✓[/green] Archivo cargado: [bold]{self.ruta_archivo}[/bold]")
            if self.procesos_cargados:
                console.print(f"    Procesos cargados: [cyan]{len(self.procesos_cargados)}[/cyan]")
        else:
            console.print("\n  [yellow]![/yellow] [dim]No hay archivo cargado[/dim]")
        
        # Opciones del menú
        console.print("\n  [bold]1.[/bold] Cargar archivo de procesos (CSV)")
        console.print("  [bold]2.[/bold] Ver procesos cargados")
        console.print("  [bold]3.[/bold] Iniciar simulación")
        console.print("  [bold]4.[/bold] Salir")
        console.rule(style="dim")
    
    def obtener_opcion_usuario(self) -> str:
        return console.input("\n[bold]Seleccione una opción (1-4):[/bold] ").strip()
    
    def cargar_archivo(self):
        console.print()
        console.rule("[bold cyan]CARGAR ARCHIVO DE PROCESOS[/bold cyan]", style="cyan")
        
        # Mostrar archivo actual si existe
        if self.ruta_archivo:
            console.print(f"\n  Archivo actual: [dim]{self.ruta_archivo}[/dim]")
        
        # Buscar archivo por defecto en el directorio de trabajo actual
        archivo_defecto = "procesos.csv"
        existe_defecto = os.path.isfile(archivo_defecto)
        
        # Informar si se encontró el archivo por defecto
        if existe_defecto:
            console.print(f"\n  [green]✓[/green] Se encontró '[bold]{archivo_defecto}[/bold]' en el directorio actual.")
            console.print("  [dim](Presione Enter para usar este archivo)[/dim]")
        
        # Solicitar ruta al usuario
        ruta = console.input("\n  [bold]Ingrese la ruta del archivo CSV:[/bold] ").strip()
        
        # Usar archivo por defecto si no se ingresó ruta
        if not ruta:
            if existe_defecto:
                ruta = archivo_defecto
            else:
                console.print("\n  [red]✗[/red] Debe ingresar una ruta de archivo.")
                console.input("\n  [dim]Presione Enter para continuar...[/dim]")
                return
        
        # Expandir rutas con ~ (directorio home del usuario)
        ruta = os.path.expanduser(ruta)
        
        # Validar y cargar el archivo
        console.print(f"\n  Validando archivo: [cyan]{ruta}[/cyan]")
        es_valido, mensaje = LectorCSV.validar_archivo(ruta)
        
        if es_valido:
            try:
                # Leer procesos del archivo CSV
                self.procesos_cargados = LectorCSV.leer_procesos(ruta)
                self.ruta_archivo = ruta
                console.print(f"\n  [green]✓[/green] {mensaje}")
                console.print("    Archivo cargado exitosamente.")
            except Exception as e:
                console.print(f"\n  [red]✗[/red] Error al cargar archivo: {e}")
        else:
            console.print(f"\n  [red]✗[/red] Error: {mensaje}")
        
        console.input("\n  [dim]Presione Enter para continuar...[/dim]")
    
    def ver_procesos(self):
        console.print()
        console.rule("[bold cyan]PROCESOS CARGADOS[/bold cyan]", style="cyan")
        
        if not self.procesos_cargados:
            # No hay procesos cargados
            console.print("\n  [yellow]![/yellow] No hay procesos cargados.")
            console.print("    [dim]Use la opción 1 para cargar un archivo CSV.[/dim]")
        else:
            # Mostrar información del archivo
            console.print(f"\n  Archivo: [bold]{self.ruta_archivo}[/bold]")
            
            # Crear tabla con estilo Rich
            table = Table(
                box=box.ROUNDED,
                show_header=True,
                header_style="bold cyan"
            )
            
            # Definir columnas de la tabla
            table.add_column("ID", justify="center", style="white")
            table.add_column("Tamaño", justify="right", style="yellow")
            table.add_column("T. Arribo", justify="right", style="green")
            table.add_column("T. Irrupción", justify="right", style="magenta")
            
            # Agregar una fila por cada proceso
            for proceso in self.procesos_cargados:
                table.add_row(
                    proceso.id_proceso,
                    f"{proceso.tamaño} KB",
                    str(proceso.tiempo_arribo),
                    str(proceso.tiempo_irrupcion)
                )
            
            # Renderizar tabla y total
            console.print()
            console.print(table)
            console.print(f"\n  [dim]Total: {len(self.procesos_cargados)} procesos[/dim]")
        
        console.input("\n  [dim]Presione Enter para continuar...[/dim]")
    
    def iniciar_simulacion(self):
        """
        Inicia la simulación de asignación de memoria y planificación.
        
        Este método:
        1. Verifica que haya procesos cargados
        2. Solicita confirmación al usuario
        3. Crea una instancia del Simulador
        4. Carga los procesos desde el archivo
        5. Muestra la pantalla de bienvenida
        6. Ejecuta la simulación paso a paso
        """
        # Verificar que hay procesos cargados
        if not self.procesos_cargados:
            console.print("\n  [yellow]![/yellow] No hay procesos cargados.")
            console.print("    [dim]Use la opción 1 para cargar un archivo CSV primero.[/dim]")
            console.input("\n  [dim]Presione Enter para continuar...[/dim]")
            return
        
        console.print()
        console.rule("[bold cyan]INICIAR SIMULACIÓN[/bold cyan]", style="cyan")
        console.print(f"\n  Archivo: [bold]{self.ruta_archivo}[/bold]")
        console.print(f"  Procesos: [cyan]{len(self.procesos_cargados)}[/cyan]")
        
        # Solicitar confirmación
        confirmacion = console.input("\n  [bold]¿Desea iniciar la simulación? (s/n):[/bold] ").strip().lower()
        
        # Validar respuesta afirmativa en español e inglés
        if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
            self.limpiar_pantalla()
            
            # Crear e inicializar el simulador
            simulador = Simulador()
            simulador.cargar_procesos(self.ruta_archivo)
            
            # Mostrar información inicial
            self.formateador.mostrar_bienvenida()
            self.formateador.mostrar_procesos_cargados(simulador.procesos)
            self.formateador.esperar_entrada()
            
            # Ejecutar la simulación
            simulador.simular()
            
            console.input("\n  [dim]Presione Enter para volver al menú principal...[/dim]")
        else:
            console.print("\n  [yellow]Simulación cancelada.[/yellow]")
            console.input("\n  [dim]Presione Enter para continuar...[/dim]")
    
    def ejecutar(self):
        """
        Bucle principal de ejecución del menú.
        """
        while True:
            # Preparar pantalla
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_menu()
            
            # Obtener selección del usuario
            opcion = self.obtener_opcion_usuario()
            
            # Ejecutar acción según la opción
            if opcion == '1':
                self.cargar_archivo()
            elif opcion == '2':
                self.ver_procesos()
            elif opcion == '3':
                self.iniciar_simulacion()
            elif opcion == '4':
                # Mensaje de despedida y salir del bucle
                console.print("\n  [bold green]¡Hasta luego![/bold green]\n")
                break
            else:
                # Opción no válida
                console.print("\n  [red]![/red] Opción no válida. Por favor seleccione 1, 2, 3 o 4.")
                console.input("\n  [dim]Presione Enter para continuar...[/dim]")

