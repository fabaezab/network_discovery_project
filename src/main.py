"""
Network Discovery Project - Main Script

Este script principal gestiona el menú principal y la interacción del usuario para
realizar tareas de descubrimiento de red y escaneo de puertos.

Author: Felipe A Baeza B
date: 25-07-2024
"""

from .menu import mostrar_menu, continuar_o_salir, limpiar_pantalla
from .discovery.discover_servers import descubrir_servidores
from .discovery.discover_ports import scan_puertos
from .discovery.discover_ports_of_connected_servers import descubrir_puertos_de_servidores_conectados
from .vulnerabilities.search import buscar_por_cve, buscar_por_criticidad
from .vulnerabilities.export import exportar_csv, exportar_sqlite
import netifaces
import ipaddress
import socket

NIVELES_CRITICIDAD = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

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

def mostrar_vulnerabilidad(vulnerabilidad):

    print("\nDetalles de la Vulnerabilidad:")
    print(f"{'CVE ID:':<22} {vulnerabilidad['cve_id']}")
    print(f"{'Descripción:':<22} {vulnerabilidad['descripcion']}")
    print(f"{'Criticidad:':<22} {vulnerabilidad['criticidad']}")
    print(f"{'Fecha de Publicación:':<22} {vulnerabilidad['fecha_publicacion']}")
    print(f"{'Fecha de Modificación:':<22} {vulnerabilidad['fecha_modificacion']}")
    print("\n")

def mostrar_resultados_paginados(resultados):
    total_vulnerabilidades = len(resultados)
    print(f"Se encontraron {total_vulnerabilidades} vulnerabilidades.")

    vulnerabilidades_para_exportar = []

    if total_vulnerabilidades > 0:
        mostrar_todas = input("¿Desea mostrar todas las vulnerabilidades? (Si/No): ").strip().lower()
        if mostrar_todas == "si":
            i = 0
            while i < total_vulnerabilidades:
                fin = min(i + 100, total_vulnerabilidades)
                for resultado in resultados[i:fin]:
                    try:
                        cve_id = resultado.get('cve', {}).get('id')
                        descripcion = resultado.get('cve', {}).get('descriptions', [{}])[0].get('value')
                        criticidad = resultado.get('cve', {}).get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseSeverity')
                        fecha_publicacion = resultado.get('cve', {}).get('published')
                        fecha_modificacion = resultado.get('cve', {}).get('lastModified')

                        if cve_id and descripcion and criticidad and fecha_publicacion and fecha_modificacion:
                            print(f"{'CVE ID:':<22} {cve_id}")
                            print(f"{'Descripción:':<22} {descripcion}")
                            print(f"{'Criticidad:':<22} {criticidad}")
                            print(f"{'Fecha de publicación:':<22} {fecha_publicacion}")
                            print(f"{'Fecha de modificación:':<22} {fecha_modificacion}")
                            print('-' * 40)
                            vulnerabilidades_para_exportar.append({
                                'cve_id': cve_id,
                                'descripcion': descripcion,
                                'criticidad': criticidad,
                                'fecha_publicacion': fecha_publicacion,
                                'fecha_modificacion': fecha_modificacion
                            })
                        else:
                            print(f"Faltan datos en la vulnerabilidad {cve_id}.")
                    except KeyError as e:
                        print(f"Error inesperado al procesar la vulnerabilidad: Falta clave {e}")
                i = fin
                if i < total_vulnerabilidades:
                    continuar = input(f"Mostrando vulnerabilidades {i + 1}-{min(i + 100, total_vulnerabilidades)}. ¿Desea continuar con las siguientes 100? (Si/No): ").strip().lower()
                    if continuar != "si":
                        # Aquí rompemos el bucle y solo exportamos lo que se ha mostrado
                        exportar_csv(vulnerabilidades_para_exportar, 'vulnerabilidades.csv')
                        exportar_sqlite(vulnerabilidades_para_exportar, 'vulnerabilidades.db')
                        print(f"Datos exportados a CSV y SQLite.")
                        return
        else:
            print("Mostrando las primeras 100 vulnerabilidades:")
            for resultado in resultados[:100]:
                try:
                    cve_id = resultado.get('cve', {}).get('id')
                    descripcion = resultado.get('cve', {}).get('descriptions', [{}])[0].get('value')
                    criticidad = resultado.get('cve', {}).get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseSeverity')
                    fecha_publicacion = resultado.get('cve', {}).get('published')
                    fecha_modificacion = resultado.get('cve', {}).get('lastModified')

                    if cve_id and descripcion and criticidad and fecha_publicacion and fecha_modificacion:
                        print(f"CVE ID: {cve_id}")
                        print(f"Descripción: {descripcion}")
                        print(f"Criticidad: {criticidad}")
                        print(f"Fecha de publicación: {fecha_publicacion}")
                        print(f"Fecha de modificación: {fecha_modificacion}")
                        print('-' * 40)
                        vulnerabilidades_para_exportar.append({
                            'cve_id': cve_id,
                            'descripcion': descripcion,
                            'criticidad': criticidad,
                            'fecha_publicacion': fecha_publicacion,
                            'fecha_modificacion': fecha_modificacion
                        })
                    else:
                        print(f"Faltan datos en la vulnerabilidad {cve_id}.")
                except KeyError as e:
                    print(f"Error inesperado al procesar la vulnerabilidad: Falta clave {e}")

            # Exportar los primeros 100 resultados
            exportar_csv(vulnerabilidades_para_exportar, 'vulnerabilidades.csv')
            exportar_sqlite(vulnerabilidades_para_exportar, 'vulnerabilidades.db')
            print(f"Datos exportados a CSV y SQLite.")
    else:
        print("No se encontraron vulnerabilidades para el nivel de criticidad proporcionado.")

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
        elif opcion == "2.1":
            cve_id = input("Ingrese el identificador CVE: ").strip()
            resultado = buscar_por_cve(cve_id)
            if resultado:
                try:
                    vulnerabilidad = {
                        'cve_id': resultado['cve']['id'],
                        'descripcion': resultado['cve']['descriptions'][0]['value'],
                        'criticidad': resultado['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseSeverity'],
                        'fecha_publicacion': resultado['cve']['published'],
                        'fecha_modificacion': resultado['cve']['lastModified'],
                    }
                    mostrar_vulnerabilidad(vulnerabilidad)
                    exportar_csv([vulnerabilidad], 'vulnerabilidades.csv')
                    exportar_sqlite([vulnerabilidad], 'vulnerabilidades.db')
                    print(f"Vulnerabilidad exportada a CSV y SQLite.")
                except KeyError as e:
                    print(f"Error al procesar la vulnerabilidad: Falta clave {e}")
            else:
                print("No se encontró información para el CVE proporcionado.")
        
        elif opcion == "2.2":
            print(f"Niveles de criticidad disponibles: {', '.join(NIVELES_CRITICIDAD)}")
            criticidad = input("Ingrese el nivel de criticidad: ").strip().upper()

            if criticidad in NIVELES_CRITICIDAD:
                resultados = buscar_por_criticidad(criticidad)
                mostrar_resultados_paginados(resultados)
            else:
                print(f"Criticidad '{criticidad}' no es válida. Intente de nuevo.")                        
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

        if not continuar_o_salir():
            break

if __name__ == "__main__":
    main()
