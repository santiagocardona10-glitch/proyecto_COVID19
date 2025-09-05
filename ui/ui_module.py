"""
Módulo para interfaz de usuario - Aplicación COVID-19
"""

import pandas as pd


def mostrar_menu():
    """
    Muestra el menú principal de la aplicación
    """
    print("\n" + "="*60)
    print("CONSULTA DE DATOS COVID-19 COLOMBIA ".center(60))
    print("="*60)
    print(" 1. Realizar consulta de datos")
    print(" 2. Salir de la aplicación")
    print("="*60)


def solicitar_parametros():
    """
    Solicita al usuario los parámetros necesarios para la consulta

    Returns:
        tuple: (nombre_departamento, limite_registros)
    """
    print("\n" + " CONFIGURACIÓN DE CONSULTA".center(50, "-"))

    # Mostrar ejemplos de departamentos
    print("\n Ejemplos de departamentos válidos:")
    departamentos_ejemplo = [
        "ANTIOQUIA", "CUNDINAMARCA", "VALLE DEL CAUCA",
        "SANTANDER", "BOLIVAR", "ATLANTICO", "RISARALDA"
    ]

    for i, dep in enumerate(departamentos_ejemplo, 1):
        print(f"   {i}. {dep}")

    # Solicitar departamento
    print("\n Departamento:")
    nombre_departamento = input("Ingrese el nombre del departamento: ").strip().upper()

    # Solicitar límite de registros con validación
    print("\n Número de registros:")
    print("  Recomendación: Use entre 10-100 registros para evitar demoras")

    while True:
        try:
            limite_registros = int(input("Ingrese el número de registros: "))
            if limite_registros > 0:
                if limite_registros > 500:
                    confirm = input(f" {limite_registros} registros pueden tardar mucho. ¿Continuar? (s/n): ")
                    if confirm.lower() in ['s', 'si', 'yes', 'y']:
                        break
                else:
                    break
            else:
                print(" El número debe ser positivo")
        except ValueError:
            print(" Por favor ingrese un número válido")

    return nombre_departamento, limite_registros


def mostrar_resultados(dataframe):
    """
    Muestra los resultados de la consulta en formato tabular

    Args:
        dataframe (pandas.DataFrame): DataFrame con los resultados
    """
    if dataframe is None or dataframe.empty:
        print("\n No se encontraron datos para mostrar")
        print("   Verifique el nombre del departamento e intente nuevamente")
        return

    print("\n" + "=" * 80)
    print(" RESULTADOS DE LA CONSULTA".center(80))
    print("=" * 80)

    # Información general
    print(f" Total de registros encontrados: {len(dataframe)}")
    print(f" Columnas mostradas: {len(dataframe.columns)}")
    print("-" * 80)

    # Configurar pandas para mejor visualización
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 25)
    pd.set_option('display.expand_frame_repr', False)

    # Mostrar TODOS los registros solicitados
    print(f" Mostrando los {len(dataframe)} registros obtenidos:")
    print(dataframe.to_string(index=True))
    print("=" * 80)


def pausar():
    """
    Pausa la ejecución hasta que el usuario presione Enter
    """
    input("\n  Presione Enter para continuar...")

