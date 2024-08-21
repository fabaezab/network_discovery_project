"""
Tests para el módulo de búsqueda de vulnerabilidades (search.py).

Este archivo contiene pruebas unitarias para las funciones de búsqueda de vulnerabilidades por CVE y criticidad.

Author: Felipe A. Baeza B.
Date: 15-08-2024
"""

import unittest
from unittest.mock import patch
from src.vulnerabilities.search import buscar_por_cve, buscar_por_criticidad

class TestBuscarVulnerabilidades(unittest.TestCase):
    @patch('vulnerabilities.search.requests.get')
    def test_buscar_por_cve(self, mock_get):
        # Simula la respuesta de la API del NVD para un CVE específico
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'totalResults': 1,
            'result': {
                'CVE_Items': [
                    {
                        'cve': {
                            'CVE_data_meta': {
                                'ID': 'CVE-2021-34527'
                            },
                            'description': {
                                'description_data': [
                                    {'value': 'Descripción de prueba'}
                                ]
                            }
                        },
                        'impact': {
                            'baseMetricV3': {
                                'cvssV3': {
                                    'baseSeverity': 'CRITICAL'
                                }
                            }
                        },
                        'publishedDate': '2021-06-30T14:15Z',
                        'lastModifiedDate': '2021-07-01T16:22Z'
                    }
                ]
            }
        }

        cve_id = 'CVE-2021-34527'
        resultado = buscar_por_cve(cve_id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['cve']['CVE_data_meta']['ID'], cve_id)

    @patch('vulnerabilities.search.requests.get')
    def test_buscar_por_criticidad(self, mock_get):
        # Simula la respuesta de la API del NVD para una búsqueda por criticidad
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'totalResults': 2,
            'result': {
                'CVE_Items': [
                    {
                        'cve': {
                            'CVE_data_meta': {
                                'ID': 'CVE-2021-34527'
                            },
                            'description': {
                                'description_data': [
                                    {'value': 'Descripción de prueba'}
                                ]
                            }
                        },
                        'impact': {
                            'baseMetricV3': {
                                'cvssV3': {
                                    'baseSeverity': 'CRITICAL'
                                }
                            }
                        },
                        'publishedDate': '2021-06-30T14:15Z',
                        'lastModifiedDate': '2021-07-01T16:22Z'
                    },
                    {
                        'cve': {
                            'CVE_data_meta': {
                                'ID': 'CVE-2021-3156'
                            },
                            'description': {
                                'description_data': [
                                    {'value': 'Otra descripción de prueba'}
                                ]
                            }
                        },
                        'impact': {
                            'baseMetricV3': {
                                'cvssV3': {
                                    'baseSeverity': 'CRITICAL'
                                }
                            }
                        },
                        'publishedDate': '2021-05-30T14:15Z',
                        'lastModifiedDate': '2021-06-01T16:22Z'
                    }
                ]
            }
        }

        criticidad = 'CRITICAL'
        resultados = buscar_por_criticidad(criticidad)
        self.assertEqual(len(resultados), 2)
        self.assertEqual(resultados[0]['cve']['CVE_data_meta']['ID'], 'CVE-2021-34527')

if __name__ == '__main__':
    unittest.main()
