"""
Network Discovery Project - Menu Module

Este módulo contiene funciones para mostrar el menú principal, limpiar la pantalla y gestionar la continuación o salida del programa.

Autor: Felipe A Baeza B
Fecha: 25-07-2024
"""

import os

def limpiar_pantalla():
    # Limpiar la pantalla
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n1. DESCUBRIR")
    print("  1.1 DESCUBRIR SERVIDORES CONECTADOS")
    print("  1.2 DESCUBRIR PUERTOS")
    print("  1.3 DESCUBRIR PUERTOS DE SERVIDORES CONECTADOS")
    print("2. BUSCAR VULNERABILIDADES POR API (No disponible)")
    print("3. GENERAR REPORTES (No disponible)")
    print("4. SALIR")

def continuar_o_salir():
    while True:
        decision = input("¿Desea continuar? (Si/No): ").strip().lower()
        if decision == 'si':
            return True
        elif decision == 'no':
            return False
