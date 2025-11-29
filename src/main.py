"""
Punto de entrada principal del simulador de asignación de memoria.
"""

import sys
from rich.console import Console
from utils.menu_principal import MenuPrincipal

# Instancia de consola para mensajes de error
console = Console()

def main():
    try:
        menu = MenuPrincipal() # Menu principal para la interacción con el usuario
        menu.ejecutar()
    except KeyboardInterrupt:
        # El usuario interrumpió el programa con Ctrl+C
        try:
            print("\n\n  Programa interrumpido por el usuario. ¡Hasta luego!\n")
        except:
            pass
        sys.exit(0)
    except Exception as e:
        # Error inesperado durante la ejecución
        try:
            console.print(f"\n  [red]Error inesperado:[/red] {e}")
        except:
            print(f"\n  Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
