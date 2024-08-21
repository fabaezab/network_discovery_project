"""
Network Discovery Project - Host Model

Este módulo define la clase Host utilizada para representar un servidor en la red.

Author: Felipe A Baeza B
Date: 25-07-2024
"""

class Host:
    def __init__(self, ip, nombre=None):
        self.ip = ip
        self.nombre = nombre
        self.puertos_abiertos = []

    def agregar_puerto(self, puerto):
        self.puertos_abiertos.append(puerto)
