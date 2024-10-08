"""
Network Discovery Project - Menu Module

Este módulo contiene funciones para mostrar el menú principal, limpiar la pantalla y gestionar la continuación o salida del programa.

Author: Felipe A Baeza B
Date: 25-07-2024
"""

import os

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Muestra el menú principal del programa."""
    print("\n1. DESCUBRIR")
    print("  1.1 DESCUBRIR SERVIDORES CONECTADOS")
    print("  1.2 DESCUBRIR PUERTOS")
    print("  1.3 DESCUBRIR PUERTOS DE SERVIDORES CONECTADOS")
    print("\n2. BUSCAR VULNERABILIDADES POR API")
    print("  2.1 BUSCAR VULNERABILIDADES POR CVE")
    print("  2.2 BUSCAR VULNERABILIDADES POR CRITICIDAD")
    print("\n3. GENERAR REPORTES (No disponible)")
    print("4. SALIR")

def continuar_o_salir():
    """Pregunta al usuario si desea continuar o salir del programa."""
    while True:
        decision = input("¿Desea continuar? (Si/No): ").strip().lower()
        if decision == 'si':
            return True
        elif decision == 'no':
            return False
        else:
            print("Entrada no válida. Por favor, ingrese 'Si' o 'No'.")