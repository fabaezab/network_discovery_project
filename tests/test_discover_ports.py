"""
Network Discovery Project - Tests for Discover Ports

Este módulo contiene pruebas unitarias para la función scan_puertos.

Autor: Felipe A Baeza B
Fecha: 25-07-2024
"""

import unittest
from src.discovery.discover_ports import scan_puertos

class TestDescubrirPuertos(unittest.TestCase):
    def test_descubrir_puertos(self):
        ip = "192.168.1.1"
        puertos = scan_puertos(ip, 20, 25)  # Escanear un rango pequeño de puertos para la prueba
        self.assertIsInstance(puertos, list)
        for puerto, servicio in puertos:
            self.assertIsInstance(puerto, int)
            self.assertIsInstance(servicio, str)

if __name__ == '__main__':
    unittest.main()
