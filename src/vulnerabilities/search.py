"""
Network Discovery Project - search vulnerabilities

Este módulo define la clase Host utilizada para representar un servidor en la red.

Author: Felipe A Baeza B
date: 15-08-2024
"""

import requests
import json
from tqdm import tqdm
import itertools
import threading
import time
import sys

loading = False

API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def mostrar_indicador_carga(mensaje="Recopilando información"):
    for frame in itertools.cycle(['|', '/', '-', '\\']):
        if not loading:
            break
        sys.stdout.write(f'\r{mensaje} {frame}')
        sys.stdout.flush()
        time.sleep(0.1)

def buscar_por_cve(cve_id):

    params = {'cveId': cve_id}
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        try:
            data = response.json()
        except ValueError:
            print("Error al decodificar la respuesta JSON")
            print(f"Contenido de la respuesta: {response.text}")
            return None
        
        if data.get('totalResults', 0) == 0:
            print(f"No se encontró información para el CVE proporcionado: {cve_id}")
            return None
        
        return data['vulnerabilities'][0]
        
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a la API: {e}")
        return None

def buscar_por_criticidad(criticidad):
    global loading
    params = {
        'cvssV3Severity': criticidad,
        'resultsPerPage': 2000,  # Máximo permitido por la API
        'startIndex': 0
    }
    vulnerabilidades = []
    
    try:
        loading = True
        indicador_thread = threading.Thread(target=mostrar_indicador_carga)
        indicador_thread.start()

        while True:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                print("\nError al decodificar la respuesta JSON")
                print(f"Contenido de la respuesta: {response.text}")
                return []

            vulnerabilidades.extend(data.get('vulnerabilities', []))
            
            if len(vulnerabilidades) >= data.get('totalResults', 0):
                break
            
            params['startIndex'] += params['resultsPerPage']
            
    except requests.exceptions.RequestException as e:
        print(f"\nError en la solicitud a la API: {e}")
        return []
    finally:
        loading = False
        indicador_thread.join()
        print("\n") 

    return vulnerabilidades