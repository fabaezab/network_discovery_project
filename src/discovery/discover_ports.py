"""
Network Discovery Project - Discover Ports Module

Este módulo contiene funciones para escanear puertos abiertos en una dirección IP específica.

Autor: Felipe A Baeza B
Fecha: 25-07-2024
"""

import socket
from tqdm import tqdm

def scan_puertos(ip, puerto_inicio, puerto_fin):
    puertos_abiertos = []
    for puerto in tqdm(range(puerto_inicio, puerto_fin + 1), desc="Escaneando puertos", unit="puerto"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Establecer un tiempo de espera de 1 segundo
            result = sock.connect_ex((ip, puerto))
            if result == 0:
                try:
                    servicio = socket.getservbyport(puerto)
                except OSError:
                    servicio = "Desconocido"
                puertos_abiertos.append((puerto, servicio))
    return puertos_abiertos
