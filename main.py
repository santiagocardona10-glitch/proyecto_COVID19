"""
Aplicación principal para consultar datos de COVID-19 en Colombia

Proyecto: Fundamentos Básicos de Python
Docente: Alejandro Rodas Vásquez
Universidad Tecnológica de Pereira
"""

# Importar módulos del proyecto
from api import api_module
from ui import ui_module


def main():
    """
    Función principal que controla el flujo de la aplicación
    """
    print("🚀 Iniciando aplicación COVID-19...")

    # Verificar dependencias al inicio
    try:
        import pandas as pd
        import sodapy
        print("✅ Dependencias verificadas correctamente")
    except ImportError as e:
        print(f"❌ Error: Falta instalar dependencias: {e}")
        print("   Ejecute: pip install pandas sodapy")
        return

    while True:
        try:
            # Mostrar menú principal
            ui_module.mostrar_menu()

            # Obtener opción del usuario
            opcion = input("\n🔍 Seleccione una opción (1-2): ").strip()

            if opcion == "1":
                print("\n🔍 NUEVA CONSULTA INICIADA")

                # Obtener parámetros del usuario
                nombre_departamento, limite_registros = ui_module.solicitar_parametros()

                print(f"\n⏳ Procesando consulta...")
                print(f"   📍 Departamento: {nombre_departamento}")
                print(f"   📊 Registros solicitados: {limite_registros}")

                # Realizar consulta a la API
                datos_raw = api_module.consultar_datos_covid(
                    nombre_departamento,
                    limite_registros
                )

                # Si falla la consulta por departamento, intentar método alternativo
                if datos_raw is None or datos_raw.empty:
                    print("\n🔄 Intentando consulta general...")
                    datos_raw = api_module.consultar_datos_covid_alternativo(limite_registros)

                    # Si obtuvimos datos, filtrar por departamento localmente
                    if datos_raw is not None and not datos_raw.empty:
                        if 'departamento_nom' in datos_raw.columns:
                            # Filtrar por departamento localmente
                            mask = datos_raw['departamento_nom'].str.upper().str.contains(
                                nombre_departamento.upper(), na=False
                            )
                            datos_departamento = datos_raw[mask]

                            if not datos_departamento.empty:
                                datos_raw = datos_departamento
                                print(f"✅ Filtrado local: {len(datos_raw)} registros para {nombre_departamento}")
                            else:
                                print(f"⚠️ No se encontraron datos para {nombre_departamento}")
                                print("   Mostrando muestra de datos generales...")
                                datos_raw = datos_raw.head(10)

                if datos_raw is not None and not datos_raw.empty:
                    # Filtrar y mostrar resultados
                    datos_filtrados = api_module.filtrar_columnas_relevantes(datos_raw)
                    ui_module.mostrar_resultados(datos_filtrados)




                else:
                    print("\n CONSULTA SIN RESULTADOS")
                    print("   Posibles causas:")
                    print("   • Nombre del departamento incorrecto")
                    print("   • Problemas de conectividad")
                    print("   • API temporalmente no disponible")
                    print("\n Sugerencias:")
                    print("   • Verifique la ortografía del departamento")
                    print("   • Use nombres en MAYÚSCULAS")
                    print("   • Intente con otro departamento")

                input("\n⏸️  Presione Enter para continuar...")

            elif opcion == "2":
                print("\n👋 ¡Gracias por usar la aplicación!")
                print("   Desarrollado para Universidad Tecnológica de Pereira")
                break

            else:
                print("\n❌ Opción no válida. Por favor seleccione 1 o 2")

        except KeyboardInterrupt:
            print("\n\n⚠️ Aplicación interrumpida por el usuario")
            print("👋 ¡Hasta pronto!")
            break

        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("🔄 La aplicación continuará ejecutándose...")
            input("\n⏸️  Presione Enter para continuar...")


if __name__ == "__main__":
    main()