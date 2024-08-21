"""
Network Discovery Project - export vulnerabilities

Este módulo define la clase Host utilizada para representar un servidor en la red.

Author: Felipe A Baeza B
date: 15-08-2024
"""

import csv
import sqlite3

def exportar_csv(vulnerabilidades, nombre_archivo):

    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CVE ID', 'Descripción', 'Nivel de Criticidad', 'Fecha de Publicación', 'Fecha de Última Modificación'])
        for vul in vulnerabilidades:
            writer.writerow([vul['cve_id'], vul['descripcion'], vul['criticidad'], vul['fecha_publicacion'], vul['fecha_modificacion']])

def exportar_sqlite(vulnerabilidades, nombre_db):

    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vulnerabilidades (
            cve_id TEXT PRIMARY KEY,
            descripcion TEXT,
            criticidad TEXT,
            fecha_publicacion TEXT,
            fecha_modificacion TEXT
        )
    ''')

    for vul in vulnerabilidades:
        cursor.execute('''
            INSERT OR REPLACE INTO vulnerabilidades (cve_id, descripcion, criticidad, fecha_publicacion, fecha_modificacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (vul['cve_id'], vul['descripcion'], vul['criticidad'], vul['fecha_publicacion'], vul['fecha_modificacion']))
    
    conn.commit()
    conn.close()
