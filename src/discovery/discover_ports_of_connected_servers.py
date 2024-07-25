"""
Network Discovery Project - Discover Ports of Connected Servers Module

Este módulo contiene funciones para descubrir puertos abiertos de servidores conectados en una subred específica.

Autor: Felipe A Baeza B
Fecha: 25-07-2024
"""

from .discover_servers import descubrir_servidores
from .discover_ports import scan_puertos

def descubrir_puertos_de_servidores_conectados(subred, puerto_inicio, puerto_fin):
    hosts = descubrir_servidores(subred)
    for host in hosts:
        host.puertos_abiertos = scan_puertos(host.ip, puerto_inicio, puerto_fin)
    return hosts
