"""
Punto de entrada principal del simulador de memoria y planificación de procesos.

Este programa simula:
- Asignación de memoria con particiones fijas usando Best-Fit
- Planificación de CPU con algoritmo SRTF (Shortest Remaining Time First)
- Grado de multiprogramación de 5 procesos
- Máximo de 10 procesos
"""

import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from simulador import Simulador
from lector_csv import LectorCSV
from formato_salida import FormateadorSalida


# Consola global
console = Console()


class MenuPrincipal:
    """
    Menú interactivo para el simulador de memoria.
    """
    
    def __init__(self):
        """Inicializa el menú con valores por defecto."""
        self.ruta_archivo = None
        self.procesos_cargados = None
        self.formateador = FormateadorSalida()
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_encabezado(self):
        """Muestra el encabezado del programa."""
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
            "  • Particiones: [magenta]SO(100KB), 250KB, 150KB, 50KB[/magenta]\n"
            "  • Máximo de procesos: [cyan]10[/cyan]"
        )
        console.print(Panel(config_text, border_style="dim"))
    
    def mostrar_menu(self):
        """Muestra las opciones del menú principal."""
        console.print()
        console.rule("[bold cyan]MENÚ PRINCIPAL[/bold cyan]", style="cyan")
        
        # Mostrar estado actual del archivo cargado
        if self.ruta_archivo:
            console.print(f"\n  [green]✓[/green] Archivo cargado: [bold]{self.ruta_archivo}[/bold]")
            if self.procesos_cargados:
                console.print(f"    Procesos cargados: [cyan]{len(self.procesos_cargados)}[/cyan]")
        else:
            console.print("\n  [yellow]![/yellow] [dim]No hay archivo cargado[/dim]")
        
        console.print("\n  [bold]1.[/bold] Cargar archivo de procesos (CSV)")
        console.print("  [bold]2.[/bold] Ver procesos cargados")
        console.print("  [bold]3.[/bold] Iniciar simulación")
        console.print("  [bold]4.[/bold] Salir")
        console.rule(style="dim")
    
    def obtener_opcion(self) -> str:
        """
        Obtiene la opción seleccionada por el usuario.
        
        Returns:
            La opción ingresada por el usuario
        """
        return console.input("\n[bold]Seleccione una opción (1-4):[/bold] ").strip()
    
    def cargar_archivo(self):
        """Solicita y carga un archivo CSV de procesos."""
        console.print()
        console.rule("[bold cyan]CARGAR ARCHIVO DE PROCESOS[/bold cyan]", style="cyan")
        
        # Mostrar ruta actual si existe
        if self.ruta_archivo:
            console.print(f"\n  Archivo actual: [dim]{self.ruta_archivo}[/dim]")
        
        # Buscar procesos.csv en el directorio de trabajo actual
        archivo_defecto = "procesos.csv"
        existe_defecto = os.path.isfile(archivo_defecto)
        
        if existe_defecto:
            console.print(f"\n  [green]✓[/green] Se encontró '[bold]{archivo_defecto}[/bold]' en el directorio actual.")
            console.print("  [dim](Presione Enter para usar este archivo)[/dim]")
        
        ruta = console.input("\n  [bold]Ingrese la ruta del archivo CSV:[/bold] ").strip()
        
        # Usar archivo por defecto si no se ingresa nada y existe
        if not ruta:
            if existe_defecto:
                ruta = archivo_defecto
            else:
                console.print("\n  [red]✗[/red] Debe ingresar una ruta de archivo.")
                console.input("\n  [dim]Presione Enter para continuar...[/dim]")
                return
        
        # Expandir ~ a directorio home si es necesario
        ruta = os.path.expanduser(ruta)
        
        # Validar y cargar el archivo
        console.print(f"\n  Validando archivo: [cyan]{ruta}[/cyan]")
        es_valido, mensaje = LectorCSV.validar_archivo(ruta)
        
        if es_valido:
            try:
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
        """Muestra los procesos cargados."""
        console.print()
        console.rule("[bold cyan]PROCESOS CARGADOS[/bold cyan]", style="cyan")
        
        if not self.procesos_cargados:
            console.print("\n  [yellow]![/yellow] No hay procesos cargados.")
            console.print("    [dim]Use la opción 1 para cargar un archivo CSV.[/dim]")
        else:
            console.print(f"\n  Archivo: [bold]{self.ruta_archivo}[/bold]")
            
            table = Table(
                box=box.ROUNDED,
                show_header=True,
                header_style="bold cyan"
            )
            
            table.add_column("ID", justify="center", style="white")
            table.add_column("Tamaño", justify="right", style="yellow")
            table.add_column("T. Arribo", justify="right", style="green")
            table.add_column("T. Irrupción", justify="right", style="magenta")
            
            for proceso in self.procesos_cargados:
                table.add_row(
                    proceso.id_proceso,
                    f"{proceso.tamaño} KB",
                    str(proceso.tiempo_arribo),
                    str(proceso.tiempo_irrupcion)
                )
            
            console.print()
            console.print(table)
            console.print(f"\n  [dim]Total: {len(self.procesos_cargados)} procesos[/dim]")
        
        console.input("\n  [dim]Presione Enter para continuar...[/dim]")
    
    def iniciar_simulacion(self):
        """Inicia la simulación con los procesos cargados."""
        if not self.procesos_cargados:
            console.print("\n  [yellow]![/yellow] No hay procesos cargados.")
            console.print("    [dim]Use la opción 1 para cargar un archivo CSV primero.[/dim]")
            console.input("\n  [dim]Presione Enter para continuar...[/dim]")
            return
        
        # Confirmar inicio de simulación
        console.print()
        console.rule("[bold cyan]INICIAR SIMULACIÓN[/bold cyan]", style="cyan")
        console.print(f"\n  Archivo: [bold]{self.ruta_archivo}[/bold]")
        console.print(f"  Procesos: [cyan]{len(self.procesos_cargados)}[/cyan]")
        
        confirmacion = console.input("\n  [bold]¿Desea iniciar la simulación? (s/n):[/bold] ").strip().lower()
        
        if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
            self.limpiar_pantalla()
            
            # Crear y ejecutar el simulador
            simulador = Simulador()
            simulador.cargar_procesos(self.ruta_archivo)
            
            self.formateador.mostrar_bienvenida()
            self.formateador.mostrar_procesos_cargados(simulador.procesos)
            self.formateador.esperar_entrada()
            
            simulador.simular()
            
            console.input("\n  [dim]Presione Enter para volver al menú principal...[/dim]")
        else:
            console.print("\n  [yellow]Simulación cancelada.[/yellow]")
            console.input("\n  [dim]Presione Enter para continuar...[/dim]")
    
    def ejecutar(self):
        """Ejecuta el bucle principal del menú."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_menu()
            
            opcion = self.obtener_opcion()
            
            if opcion == '1':
                self.cargar_archivo()
            elif opcion == '2':
                self.ver_procesos()
            elif opcion == '3':
                self.iniciar_simulacion()
            elif opcion == '4':
                console.print("\n  [bold green]¡Hasta luego![/bold green]\n")
                break
            else:
                console.print("\n  [red]![/red] Opción no válida. Por favor seleccione 1, 2, 3 o 4.")
                console.input("\n  [dim]Presione Enter para continuar...[/dim]")


def main():
    """Función principal que ejecuta el menú del simulador."""
    try:
        menu = MenuPrincipal()
        menu.ejecutar()
    except KeyboardInterrupt:
        console.print("\n\n  [yellow]Programa interrumpido por el usuario.[/yellow]\n")
    except Exception as e:
        console.print(f"\n  [red]Error inesperado:[/red] {e}")


if __name__ == "__main__":
    main()
