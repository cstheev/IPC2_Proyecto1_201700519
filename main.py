from procesador import (
    cargar_xml,
    generar_matriz_frecuencia,
    generar_matriz_patron,
    agrupar_estaciones,
    generar_matriz_reducida,
    escribir_salida
)
from graficador import graficar_matriz, graficar_patrones

def menu():
    campos = None
    while True:
        print("\n----- Menú Principal -----")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salida")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ruta = input("Escriba la ruta y nombre del archivo: ")
            campos = cargar_xml(ruta)
            print("- El archivo fue cargado correctamente.")

        elif opcion == "2":
            if campos is None:
                print("- Primero debes cargar un archivo.")
                continue
            print("- Procesando archivo...")
            for campo in campos.recorrer():
                matriz_suelo = generar_matriz_frecuencia(campo, "suelo")
                matriz_cultivo = generar_matriz_frecuencia(campo, "cultivo")
                patrones_suelo = generar_matriz_patron(matriz_suelo)
                patrones_cultivo = generar_matriz_patron(matriz_cultivo)
                grupos = agrupar_estaciones(patrones_suelo, patrones_cultivo)
                campo._matrices = (matriz_suelo, matriz_cultivo, grupos)
                print(f"- Cargando {campo.nombre}")
            print("- Carga completa.")

        elif opcion == "3":
            if campos is None:
                print("- Primero debes cargar y procesar un archivo.")
                continue
            ruta = input("Escriba el nombre del archivo de salida: ")
            for campo in campos.recorrer():
                if campo._matrices is None:
                    print(f"- El campo {campo.id} no ha sido procesado.")
                    continue
                matriz_suelo, matriz_cultivo, grupos = campo._matrices
                escribir_salida(campo, grupos, matriz_suelo, matriz_cultivo, ruta)
            print("- Archivo de salida generado correctamente.")

        elif opcion == "4":
            print("\n--- Datos del estudiante ---")
            print("Nombre: Stheeven Coc")
            print("Carnet: 201700519")
            print("Curso: Introducción a la Programación y Computación 2")
            print("Carrera: Ingeniería en Ciencias y Sistemas")
            print("Semestre: 4to. Semestre")
            print("Documentación: https://github.com/cstheev/IPC2_Proyecto1_201700519")

        elif opcion == "5":
            if campos is None:
                print("- Primero debes cargar y procesar un archivo.")
                continue

            print("\nSeleccione el tipo de matriz a graficar:")
            print("1. Frecuencia")
            print("2. Patrón")
            print("3. Reducida")
            tipo_opcion = input("- Opción: ").strip()

            tipos_validos = {"1": "frecuencia", "2": "patron", "3": "reducida"}
            tipo_matriz = tipos_validos.get(tipo_opcion)

            if not tipo_matriz:
                print("- Tipo inválido.")
                continue

            print("\nCampos agrícolas disponibles:")
            lista_campos = list(campos.recorrer())
            for i, campo in enumerate(lista_campos):
                print(f"{i + 1}. {campo.nombre} (ID: {campo.id})")

            campo_opcion = input("Seleccione el campo: ").strip()
            try:
                campo_seleccionado = lista_campos[int(campo_opcion) - 1]
            except:
                print("- Campo inválido.")
                continue

            if campo_seleccionado._matrices is None:
                print(f"- El campo {campo_seleccionado.id} no ha sido procesado.")
                continue

            matriz_suelo, matriz_cultivo, grupos = campo_seleccionado._matrices

            if tipo_matriz == "frecuencia":
                graficar_matriz(matriz_suelo, f"frecuencia_{campo_seleccionado.id}_suelo")
                graficar_matriz(matriz_cultivo, f"frecuencia_{campo_seleccionado.id}_cultivo")

            elif tipo_matriz == "patron":
                patrones_suelo = generar_matriz_patron(matriz_suelo)
                patrones_cultivo = generar_matriz_patron(matriz_cultivo)
                graficar_patrones(patrones_suelo, f"patron_{campo_seleccionado.id}_suelo")
                graficar_patrones(patrones_cultivo, f"patron_{campo_seleccionado.id}_cultivo")

            elif tipo_matriz == "reducida":
                matriz_reducida_suelo = generar_matriz_reducida(matriz_suelo, grupos)
                matriz_reducida_cultivo = generar_matriz_reducida(matriz_cultivo, grupos)
                graficar_matriz(matriz_reducida_suelo, f"reducida_{campo_seleccionado.id}_suelo")
                graficar_matriz(matriz_reducida_cultivo, f"reducida_{campo_seleccionado.id}_cultivo")

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no implementada aún.")

menu()