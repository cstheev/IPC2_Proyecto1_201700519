from procesador import cargar_xml
from procesador import generar_matriz_frecuencia, generar_matriz_patron, agrupar_estaciones, escribir_salida
from graficador import graficar_matriz

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
            ruta = input("Escriba la ruta del archivo: ")
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
                print("- Procesando matriz...")
            print("- Procesamiento completo.")
        elif opcion == "3":
            if campos is None:
                print("- Primero debes cargar y procesar un archivo.")
                continue
            ruta = input("Escriba la ruta de salida: ")
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
            for campo in campos.recorrer():
                if campo._matrices is None:
                    print(f"- El campo {campo.id} no ha sido procesado.")
                    continue
                matriz_suelo, matriz_cultivo, _ = campo._matrices
                tipo = input(f"¿Qué matriz desea graficar para el campo {campo.id}? (suelo/cultivo): ").strip().lower()
                if tipo not in ["suelo", "cultivo"]:
                    print("- Tipo inválido. Debe ser 'suelo' o 'cultivo'.")
                    continue
                matriz = matriz_suelo if tipo == "suelo" else matriz_cultivo
                if matriz.recorrer():
                    graficar_matriz(matriz, f"grafico_{campo.id}_{tipo}")
                    print(f"- Gráfico generado para campo {campo.id} ({tipo}).")
                else:
                    print(f"- La matriz de {tipo} está vacía para el campo {campo.id}.")
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no implementada aún.")

menu()