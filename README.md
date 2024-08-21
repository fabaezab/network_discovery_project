# Network Discovery Project

Author: Felipe A. Baeza B.  
License: Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE.

## Descripción del Proyecto

Este proyecto es una herramienta de descubrimiento de red que permite descubrir servidores, escanear puertos abiertos en una subred específica, y buscar vulnerabilidades de seguridad utilizando identificadores CVE o niveles de criticidad.

## Estructura del Proyecto

- `src/`: Contiene el código fuente del proyecto.
- `tests/`: Contiene los archivos de pruebas unitarias.
- `requirements.txt`: Lista de dependencias del proyecto.
- `README.md`: Descripción general del proyecto.
- `.gitignore`: Archivos y carpetas que Git debe ignorar.

## Características

- **Descubrir servidores conectados**: Encuentra servidores activos en una subred.
- **Escanear puertos**: Identifica puertos abiertos en un servidor específico.
- **Escanear puertos de servidores conectados**: Descubre puertos abiertos en todos los servidores conectados en una subred.
- **Buscar vulnerabilidades por CVE**: Permite buscar información sobre vulnerabilidades específicas utilizando un identificador CVE.
- **Buscar vulnerabilidades por criticidad**: Permite buscar vulnerabilidades según su nivel de criticidad (baja, media, alta, crítica).
- **Exportación de resultados**: Los resultados de las búsquedas de vulnerabilidades se pueden exportar en formatos CSV y SQLite.

## Requisitos

- Python 3.6 o superior
- pip (el gestor de paquetes de Python)

## Dependencias del Proyecto

```plaintext
pytest==7.3.1           # Para pruebas unitarias
pytest-mock==3.10.0     # Para facilitar el uso de mocks en pruebas
requests==2.28.1        # Para futuras expansiones como la búsqueda de vulnerabilidades por API
netifaces==0.11.0       # Para obtener información de la interfaz de red
tqdm==4.64.1            # Para la barra de progreso durante el escaneo
unittest2==1.1.0        # Para pruebas unitarias (aunque unittest viene con Python, unittest2 es una extensión)
```
