"""
Network Discovery Project - Main Script

Este script principal gestiona el menú principal y la interacción del usuario para
realizar tareas de descubrimiento de red y escaneo de puertos.

Autor: Felipe A Baeza B
Fecha: 25-07-2024
"""

from menu import mostrar_menu, continuar_o_salir, limpiar_pantalla
from discovery.discover_servers import descubrir_servidores
from discovery.discover_ports import scan_puertos
from discovery.discover_ports_of_connected_servers import descubrir_puertos_de_servidores_conectados
import netifaces
import ipaddress
import socket

def obtener_ip_local():
    for interfaz in netifaces.interfaces():
        direcciones = netifaces.ifaddresses(interfaz)
        if netifaces.AF_INET in direcciones:
            ip_info = direcciones[netifaces.AF_INET][0]
            ip_address = ip_info['addr']
            return ip_address
    return None

def obtener_subred_local():
    for interfaz in netifaces.interfaces():
        direcciones = netifaces.ifaddresses(interfaz)
        if netifaces.AF_INET in direcciones:
            ip_info = direcciones[netifaces.AF_INET][0]
            ip_address = ip_info['addr']
            netmask = ip_info.get('netmask', '255.255.255.0')
            ip_interface = ipaddress.IPv4Interface(f"{ip_address}/{netmask}")
            return str(ip_interface.network)
    return None

def obtener_nombre_host(ip):
    try:
        nombre_host = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        nombre_host = "Desconocido"
    return nombre_host

def main():
    while True:
        limpiar_pantalla()
        ip_local = obtener_ip_local()
        subred_local = obtener_subred_local()
        print(f"Tu IP es: {ip_local}")
        print(f"Tu red es: {subred_local}")
        mostrar_menu()
        
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1.1":
            subred = input("Ingrese la subred a analizar (por ejemplo, 192.168.1.0/24): ").strip()
            if subred:
                print(f"Escaneando la subred: {subred}")
                hosts = descubrir_servidores(subred)
                for host in hosts:
                    print(f"Servidor descubierto: {host.ip} ({host.nombre})")
            else:
                print("No se ingresó una subred válida.")
        elif opcion == "1.2":
            ip = input("Ingrese la dirección IP: ").strip()
            try:
                puerto_inicio = int(input("Ingrese el puerto inicial: ").strip())
                puerto_fin = int(input("Ingrese el puerto final: ").strip())
                nombre_host = obtener_nombre_host(ip)
                puertos = scan_puertos(ip, puerto_inicio, puerto_fin)
                if puertos:
                    print(f"Puertos abiertos en {ip} ({nombre_host}):")
                    for puerto, servicio in puertos:
                        print(f" - Puerto {puerto}: {servicio}")
                else:
                    print(f"No se encontraron puertos abiertos en {ip} ({nombre_host}) entre {puerto_inicio} y {puerto_fin}.")
            except ValueError:
                print("Por favor, ingrese valores válidos para los puertos.")
        elif opcion == "1.3":
            subred = input("Ingrese la subred a analizar (por ejemplo, 192.168.1.0/24): ").strip()
            try:
                puerto_inicio = int(input("Ingrese el puerto inicial: ").strip())
                puerto_fin = int(input("Ingrese el puerto final: ").strip())
                if subred:
                    print(f"Escaneando la subred: {subred}")
                    hosts = descubrir_puertos_de_servidores_conectados(subred, puerto_inicio, puerto_fin)
                    for host in hosts:
                        print(f"Servidor: {host.ip} ({host.nombre})")
                        print(f"Puertos Abiertos:")
                        for puerto, servicio in host.puertos_abiertos:
                            print(f" - Puerto {puerto}: {servicio}")
                else:
                    print("No se ingresó una subred válida.")
            except ValueError:
                print("Por favor, ingrese valores válidos para los puertos.")
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

        if not continuar_o_salir():
            break

if __name__ == "__main__":
    main()
