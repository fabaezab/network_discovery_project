"""
Network Discovery Project - Tests for Discover Servers

Este módulo contiene pruebas unitarias para la función descubrir_servidores.

Autor: Felipe A Baeza B
Fecha: 25-07-2024
"""

import unittest
from src.discovery.discover_servers import descubrir_servidores

class TestDescubrirServidores(unittest.TestCase):

    def test_descubrir_servidores(self):
        subred = "192.168.1.0/24"
        hosts = descubrir_servidores(subred)
        self.assertGreater(len(hosts), 0)
        self.assertIsInstance(hosts[0].ip, str)
        self.assertIsInstance(hosts[0].nombre, str)

if __name__ == '__main__':
    unittest.main()
