# main.py
from procesador import cargar_xml
from procesador import generar_matriz_frecuencia, generar_matriz_patron, agrupar_estaciones, escribir_salida
from graficador import graficar_matriz

def menu():
    campos = None
    while True:
        print("\n--- Menú Principal ---")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salida")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo: ")
            campos = cargar_xml(ruta)
            print("Archivo cargado correctamente.")
        elif opcion == "2":
            print("Procesando archivo...")
            for campo in campos.recorrer():
                matriz_suelo = generar_matriz_frecuencia(campo, "suelo")
                matriz_cultivo = generar_matriz_frecuencia(campo, "cultivo")
                patrones_suelo = generar_matriz_patron(matriz_suelo)
                patrones_cultivo = generar_matriz_patron(matriz_cultivo)
                grupos = agrupar_estaciones(patrones_suelo, patrones_cultivo)
                campo._matrices = (matriz_suelo, matriz_cultivo, grupos)
            print("Procesamiento completo.")

        elif opcion == "3":
            ruta = input("Ruta de salida: ")
            for campo in campos.recorrer():
                matriz_suelo, matriz_cultivo, grupos = campo._matrices
                escribir_salida(campo, grupos, matriz_suelo, matriz_cultivo, ruta)
            print("Archivo de salida generado.")

        elif opcion == "5":
            for campo in campos.recorrer():
                matriz_suelo, matriz_cultivo, _ = campo._matrices
                tipo = input("¿Qué matriz desea graficar? (suelo/cultivo): ")
                matriz = matriz_suelo if tipo == "suelo" else matriz_cultivo
                graficar_matriz(matriz, f"grafico_{campo.id}_{tipo}")
                print("Gráfico generado.")
        elif opcion == "4":
            print("Nombre: Stheeven Coc")
            print("Carnet: 201700519")
            print("Curso: Introducción a la Programación y Computación 2")
            print("Carrera: Ingeniería en Sistemas")
            print("Semestre: 4to")
            print("Documentación: [Tu enlace de GitHub aquí]")
        elif opcion == "6":
            print("¡Hasta luego, Stheeven!")
            break
        else:
            print("Opción no implementada aún.")

menu()
