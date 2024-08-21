"""
Tests para el módulo de exportación de datos (export.py).

Este archivo contiene pruebas unitarias para las funciones de exportación de datos a CSV y SQLite.

Author: Felipe A. Baeza B.
Date: 15-08-2024
"""

import unittest
import os
import sqlite3
from src.vulnerabilities.export import exportar_csv, exportar_sqlite

class TestExportarDatos(unittest.TestCase):

    def setUp(self):
        # Datos de ejemplo para las pruebas
        self.vulnerabilidades = [
            {'cve_id': 'CVE-2021-34527', 'descripcion': 'Una vulnerabilidad crítica...', 'criticidad': 'CRITICAL', 'fecha_publicacion': '2021-06-30', 'fecha_modificacion': '2021-07-01'},
            {'cve_id': 'CVE-2021-3156', 'descripcion': 'Otra vulnerabilidad importante...', 'criticidad': 'HIGH', 'fecha_publicacion': '2021-05-30', 'fecha_modificacion': '2021-06-01'}
        ]
        self.csv_file = 'test_vulnerabilidades.csv'
        self.db_file = 'test_vulnerabilidades.db'

    def tearDown(self):
        # Eliminar archivos creados durante las pruebas
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_exportar_csv(self):
        exportar_csv(self.vulnerabilidades, self.csv_file)
        self.assertTrue(os.path.exists(self.csv_file))

        with open(self.csv_file, 'r', encoding='utf-8') as file:
            contenido = file.readlines()
            self.assertEqual(len(contenido), 3)  # 2 filas de datos + 1 encabezado

    def test_exportar_sqlite(self):
        exportar_sqlite(self.vulnerabilidades, self.db_file)
        self.assertTrue(os.path.exists(self.db_file))

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vulnerabilidades")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)  # Debería haber 2 registros en la tabla

        cursor.execute("SELECT * FROM vulnerabilidades WHERE cve_id='CVE-2021-34527'")
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 'CVE-2021-34527')

        conn.close()

if __name__ == '__main__':
    unittest.main()
