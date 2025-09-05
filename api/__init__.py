"""
Paquete de módulos para la aplicación COVID-19 Colombia

Este paquete contiene los módulos necesarios para consultar
datos de COVID-19 desde la API de Datos Abiertos de Colombia.

Módulos incluidos:
- api_module: Funciones para consultar y procesar datos de la API
- ui_module: Funciones para la interfaz de usuario y presentación

Autor: [santiago cardona sierra]
Universidad Tecnológica de Pereira
Fecha: septiembre 2025
"""

# Información del paquete
__version__ = "1.0.0"
__author__ = "Tu Nombre"

# Importaciones para facilitar el uso
from .api_module import (
    consultar_datos_covid,
    filtrar_columnas_relevantes,
    consultar_datos_covid_alternativo,
    obtener_departamentos_disponibles
)
from ui.ui_module import mostrar_menu, solicitar_parametros, mostrar_resultados

# Definir qué elementos son públicos cuando se hace "from api import *"
__all__ = [
    'consultar_datos_covid',
    'consultar_datos_covid_alternativo',
    'obtener_departamentos_disponibles',
    'filtrar_columnas_relevantes',
    'mostrar_menu',
    'solicitar_parametros',
    'mostrar_resultados'
]
