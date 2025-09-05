"""
Módulo para manejo de consultas API - Datos COVID-19 Colombia
"""

import pandas as pd
from sodapy import Socrata


def consultar_datos_covid(nombre_departamento, limite_registros):
    """
    Consulta datos de COVID-19 desde la API de Datos Abiertos de Colombia

    Args:
        nombre_departamento (str): Nombre del departamento a consultar
        limite_registros (int): Número máximo de registros a obtener

    Returns:
        pandas.DataFrame: DataFrame con los datos consultados
    """
    try:
        print(f"Conectando a la API de Datos Abiertos...")

        # Cliente no autenticado para datos públicos
        client = Socrata("www.datos.gov.co", None)

        # Consulta a la API usando departamento_nom (nombre del departamento)
        print(f"Consultando {limite_registros} registros para {nombre_departamento}...")

        # La API usa 'departamento_nom' para filtrar por nombre de departamento
        results = client.get("gt2j-8ykr",
                           limit=limite_registros,
                           departamento_nom=nombre_departamento.upper())

        # Convertir a DataFrame de pandas
        results_df = pd.DataFrame.from_records(results)

        # Cerrar cliente
        client.close()

        if len(results_df) > 0:
            print(f" Consulta exitosa: {len(results_df)} registros obtenidos")
        else:
            print(f" Consulta exitosa pero sin registros para {nombre_departamento}")

        return results_df

    except Exception as e:
        print(f"❌ Error al consultar la API: {e}")
        print(f"   Verifique el nombre del departamento: {nombre_departamento}")
        return None


def consultar_datos_covid_alternativo(limite_registros):
    """
    Consulta datos generales sin filtro de departamento (método alternativo)

    Args:
        limite_registros (int): Número máximo de registros a obtener

    Returns:
        pandas.DataFrame: DataFrame con los datos consultados
    """
    try:
        print(f"Probando consulta general (sin filtro de departamento)...")

        # Cliente no autenticado para datos públicos
        client = Socrata("www.datos.gov.co", None)

        # Consulta sin filtro de departamento - obtiene datos generales
        results = client.get("gt2j-8ykr", limit=limite_registros)

        # Convertir a DataFrame de pandas
        results_df = pd.DataFrame.from_records(results)

        # Cerrar cliente
        client.close()

        print(f" Consulta general exitosa: {len(results_df)} registros obtenidos")
        return results_df

    except Exception as e:
        print(f" Error en consulta general: {e}")
        return None


def obtener_departamentos_disponibles():
    """
    Obtiene lista de departamentos disponibles en los datos

    Returns:
        list: Lista de departamentos únicos
    """
    try:
        print("Obteniendo lista de departamentos disponibles...")
        client = Socrata("www.datos.gov.co", None)

        # Obtener una muestra pequeña para ver los departamentos
        results = client.get("gt2j-8ykr", limit=100)
        df = pd.DataFrame.from_records(results)
        client.close()

        if 'departamento_nom' in df.columns:
            departamentos = sorted(df['departamento_nom'].unique())
            return [dep for dep in departamentos if dep and dep.strip()]
        else:
            return []

    except Exception as e:
        print(f"Error al obtener departamentos: {e}")
        return []


def filtrar_columnas_relevantes(dataframe):
    """
    Filtra el DataFrame para mostrar solo las columnas requeridas

    Args:
        dataframe (pandas.DataFrame): DataFrame original

    Returns:
        pandas.DataFrame: DataFrame filtrado con columnas específicas
    """
    if dataframe is None or dataframe.empty:
        return dataframe

    # Columnas que queremos mostrar según los requerimientos
    columnas_deseadas = {
        'ciudad_municipio_nom': 'Ciudad',
        'departamento_nom': 'Departamento',
        'edad': 'Edad',
        'tipo': 'Tipo',
        'estado': 'Estado',
        'pais_viajo_1_nom': 'País Procedencia'
    }

    try:
        # Verificar qué columnas están disponibles
        print("\n--- Verificando columnas disponibles ---")
        columnas_disponibles = list(dataframe.columns)
        print(f"Total columnas en datos: {len(columnas_disponibles)}")

        # Filtrar solo las columnas que existen
        columnas_filtrar = []
        nuevos_nombres = []

        for col_original, col_nueva in columnas_deseadas.items():
            if col_original in columnas_disponibles:
                columnas_filtrar.append(col_original)
                nuevos_nombres.append(col_nueva)
                print(f" {col_original} → {col_nueva}")
            else:
                print(f" {col_original} no encontrada")

        if not columnas_filtrar:
            print("⚠️ No se encontraron columnas esperadas. Mostrando primeras 6 columnas...")
            return dataframe.iloc[:, :6]  # Mostrar primeras 6 columnas

        # Crear DataFrame filtrado
        df_filtrado = dataframe[columnas_filtrar].copy()

        # Renombrar columnas para mejor presentación
        df_filtrado.columns = nuevos_nombres

        return df_filtrado

    except Exception as e:
        print(f" Error al filtrar columnas: {e}")
        print("Mostrando datos originales...")
        return dataframe