"""
Punto de entrada principal del simulador de memoria y planificación de procesos.

Este programa simula:
- Asignación de memoria con particiones fijas usando Best-Fit
- Planificación de CPU con algoritmo SRTF (Shortest Remaining Time First)
- Grado de multiprogramación de 5 procesos
- Máximo de 10 procesos
"""

import os
from simulador import Simulador
from lector_csv import LectorCSV
from formato_salida import FormateadorSalida


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
        print("\n" + "=" * 70)
        print("   SIMULADOR DE ASIGNACIÓN DE MEMORIA Y PLANIFICACIÓN DE PROCESOS")
        print("=" * 70)
        print("\nConfiguración del sistema:")
        print("  - Asignación de memoria: Particiones fijas con Best-Fit")
        print("  - Planificación de CPU: SRTF (Shortest Remaining Time First)")
        print("  - Grado de multiprogramación: 5")
        print("  - Particiones: SO(100KB), 250KB, 150KB, 50KB")
        print("  - Máximo de procesos: 10")
    
    def mostrar_menu(self):
        """Muestra las opciones del menú principal."""
        print("\n" + "-" * 50)
        print("MENÚ PRINCIPAL")
        print("-" * 50)
        
        # Mostrar estado actual del archivo cargado
        if self.ruta_archivo:
            print(f"\n  Archivo cargado: {self.ruta_archivo}")
            if self.procesos_cargados:
                print(f"  Procesos cargados: {len(self.procesos_cargados)}")
        else:
            print("\n  [!] No hay archivo cargado")
        
        print("\n  1. Cargar archivo de procesos (CSV)")
        print("  2. Ver procesos cargados")
        print("  3. Iniciar simulación")
        print("  4. Salir")
        print("-" * 50)
    
    def obtener_opcion(self) -> str:
        """
        Obtiene la opción seleccionada por el usuario.
        
        Returns:
            La opción ingresada por el usuario
        """
        return input("\nSeleccione una opción (1-4): ").strip()
    
    def cargar_archivo(self):
        """Solicita y carga un archivo CSV de procesos."""
        print("\n" + "-" * 50)
        print("CARGAR ARCHIVO DE PROCESOS")
        print("-" * 50)
        
        # Mostrar ruta actual si existe
        if self.ruta_archivo:
            print(f"\nArchivo actual: {self.ruta_archivo}")
        
        # Buscar procesos.csv en el directorio de trabajo actual
        archivo_defecto = "procesos.csv"
        existe_defecto = os.path.isfile(archivo_defecto)
        
        if existe_defecto:
            print(f"\nSe encontró '{archivo_defecto}' en el directorio actual.")
            print("(Presione Enter para usar este archivo)")
        
        ruta = input("\nIngrese la ruta del archivo CSV: ").strip()
        
        # Usar archivo por defecto si no se ingresa nada y existe
        if not ruta:
            if existe_defecto:
                ruta = archivo_defecto
            else:
                print("\n✗ Debe ingresar una ruta de archivo.")
                input("\nPresione Enter para continuar...")
                return
        
        # Expandir ~ a directorio home si es necesario
        ruta = os.path.expanduser(ruta)
        
        # Validar y cargar el archivo
        print(f"\nValidando archivo: {ruta}")
        es_valido, mensaje = LectorCSV.validar_archivo(ruta)
        
        if es_valido:
            try:
                self.procesos_cargados = LectorCSV.leer_procesos(ruta)
                self.ruta_archivo = ruta
                print(f"\n✓ {mensaje}")
                print("  Archivo cargado exitosamente.")
            except Exception as e:
                print(f"\n✗ Error al cargar archivo: {e}")
        else:
            print(f"\n✗ Error: {mensaje}")
        
        input("\nPresione Enter para continuar...")
    
    def ver_procesos(self):
        """Muestra los procesos cargados."""
        print("\n" + "-" * 50)
        print("PROCESOS CARGADOS")
        print("-" * 50)
        
        if not self.procesos_cargados:
            print("\n[!] No hay procesos cargados.")
            print("    Use la opción 1 para cargar un archivo CSV.")
        else:
            print(f"\nArchivo: {self.ruta_archivo}")
            print("-" * 60)
            print(f"{'ID':<8} {'Tamaño':<12} {'T. Arribo':<12} {'T. Irrupción':<12}")
            print("-" * 60)
            
            for proceso in self.procesos_cargados:
                print(f"{proceso.id_proceso:<8} {proceso.tamaño:<12} "
                      f"{proceso.tiempo_arribo:<12} {proceso.tiempo_irrupcion:<12}")
            
            print("-" * 60)
            print(f"Total: {len(self.procesos_cargados)} procesos")
        
        input("\nPresione Enter para continuar...")
    
    def iniciar_simulacion(self):
        """Inicia la simulación con los procesos cargados."""
        if not self.procesos_cargados:
            print("\n[!] No hay procesos cargados.")
            print("    Use la opción 1 para cargar un archivo CSV primero.")
            input("\nPresione Enter para continuar...")
            return
        
        # Confirmar inicio de simulación
        print("\n" + "-" * 50)
        print("INICIAR SIMULACIÓN")
        print("-" * 50)
        print(f"\nArchivo: {self.ruta_archivo}")
        print(f"Procesos: {len(self.procesos_cargados)}")
        
        confirmacion = input("\n¿Desea iniciar la simulación? (s/n): ").strip().lower()
        
        if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
            self.limpiar_pantalla()
            
            # Crear y ejecutar el simulador
            simulador = Simulador()
            simulador.cargar_procesos(self.ruta_archivo)
            
            self.formateador.mostrar_bienvenida()
            self.formateador.mostrar_procesos_cargados(simulador.procesos)
            self.formateador.esperar_entrada()
            
            simulador.simular()
            
            input("\nPresione Enter para volver al menú principal...")
        else:
            print("\nSimulación cancelada.")
            input("\nPresione Enter para continuar...")
    
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
                print("\n¡Hasta luego!")
                break
            else:
                print("\n[!] Opción no válida. Por favor seleccione 1, 2, 3 o 4.")
                input("\nPresione Enter para continuar...")


def main():
    """Función principal que ejecuta el menú del simulador."""
    try:
        menu = MenuPrincipal()
        menu.ejecutar()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    main()
