"""
Network Discovery Project - Discover Servers Module

Este módulo contiene funciones para descubrir servidores conectados en una subred específica.

Author: Felipe A Baeza B
Date: 25-07-2024
"""

from ..models.host import Host
import ipaddress
import subprocess
from tqdm import tqdm
import socket

def ping(ip):
    try:
        # Ping the IP address
        output = subprocess.check_output(["ping", "-n", "1", "-w", "1000", str(ip)], universal_newlines=True)
        if "TTL=" in output:
            return True
    except subprocess.CalledProcessError:
        return False
    return False

def descubrir_servidores(subred):
    red = ipaddress.IPv4Network(subred)
    hosts = []
    total_ips = len(list(red.hosts()))

    for ip in tqdm(red.hosts(), desc="Escaneando la red", unit=" IP", total=total_ips):
        if ping(ip):
            try:
                nombre_host = socket.gethostbyaddr(str(ip))[0]
            except socket.herror:
                nombre_host = "Desconocido"
            host = Host(ip=str(ip), nombre=nombre_host)
            hosts.append(host)
    
    return hosts
