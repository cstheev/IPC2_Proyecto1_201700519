import xml.etree.ElementTree as ET
from modelo import CampoAgricola, EstacionBase, SensorSuelo, SensorCultivo
from lista import Lista, DiccionarioEnlazado, ListaEnteros

def cargar_xml(ruta):
    campos = Lista()
    tree = ET.parse(ruta)
    root = tree.getroot()

    for campo in root.findall('campo'):
        c = CampoAgricola(campo.get('id'), campo.get('nombre'))

        for est in campo.find('estacionesBase').findall('estacion'):
            c.estaciones.agregar(EstacionBase(est.get('id'), est.get('nombre')))

        for sensor in campo.find('sensoresSuelo').findall('sensorS'):
            s = SensorSuelo(sensor.get('id'), sensor.get('nombre'))
            for freq in sensor.findall('frecuencia'):
                s.frecuencias.asignar(freq.get('idEstacion'), int(freq.text))
            c.sensores_suelo.agregar(s)

        for sensor in campo.find('sensoresCultivo').findall('sensorT'):
            t = SensorCultivo(sensor.get('id'), sensor.get('nombre'))
            for freq in sensor.findall('frecuencia'):
                t.frecuencias.asignar(freq.get('idEstacion'), int(freq.text))
            c.sensores_cultivo.agregar(t)

        campos.agregar(c)
    return campos

def generar_matriz_frecuencia(campo, tipo):
    matriz = DiccionarioEnlazado()
    sensores = campo.sensores_suelo if tipo == "suelo" else campo.sensores_cultivo

    for estacion in campo.estaciones.recorrer():
        submatriz = DiccionarioEnlazado()
        for sensor in sensores.recorrer():
            freq = sensor.frecuencias.obtener(estacion.id)
            if freq is None:
                freq = 0
            submatriz.asignar(sensor.id, freq)
        matriz.asignar(estacion.id, submatriz)
    return matriz

def generar_matriz_patron(matriz):
    patrones = DiccionarioEnlazado()
    for est_id, sensores in matriz.recorrer():
        patron = ListaEnteros()
        for _, freq in sensores.recorrer():
            patron.agregar(1 if freq > 0 else 0)
        patrones.asignar(est_id, patron)
    return patrones

def generar_matriz_reducida(matriz_original, grupos):
    matriz_reducida = DiccionarioEnlazado()

    for grupo in grupos.recorrer():
        # Crear un ID único para el grupo
        ids = [est_id for est_id in grupo.estaciones.recorrer()]
        id_grupo = "_".join(ids)
        submatriz = DiccionarioEnlazado()

        sensores = set()
        for est_id in ids:
            sensores_dict = matriz_original.obtener(est_id)
            if sensores_dict:
                for sensor_id, _ in sensores_dict.recorrer():
                    sensores.add(sensor_id)

        for sensor_id in sensores:
            total = 0
            for est_id in ids:
                sensores_dict = matriz_original.obtener(est_id)
                if sensores_dict:
                    freq = sensores_dict.obtener(sensor_id)
                    if freq:
                        total += freq
            submatriz.asignar(sensor_id, total)

        matriz_reducida.asignar(id_grupo, submatriz)

    return matriz_reducida

def agrupar_estaciones(patrones_suelo, patrones_cultivo):
    grupos = Lista()

    class Grupo:
        def __init__(self, patron_s, patron_t):
            self.patron_s = patron_s
            self.patron_t = patron_t
            self.estaciones = Lista()

    for est_id, patron_s in patrones_suelo.recorrer():
        patron_t = patrones_cultivo.obtener(est_id)
        if patron_t is None:
            patron_t = ListaEnteros()

        encontrado = False
        for grupo in grupos.recorrer():
            if grupo.patron_s.es_igual(patron_s) and grupo.patron_t.es_igual(patron_t):
                grupo.estaciones.agregar(est_id)
                encontrado = True
                break

        if not encontrado:
            nuevo_grupo = Grupo(patron_s, patron_t)
            nuevo_grupo.estaciones.agregar(est_id)
            grupos.agregar(nuevo_grupo)

    return grupos

def escribir_salida(campo, grupos, matriz_suelo, matriz_cultivo, ruta_salida):
    root = ET.Element("camposAgricolas")
    campo_elem = ET.SubElement(root, "campo", id=campo.id, nombre=campo.nombre)

    estaciones_elem = ET.SubElement(campo_elem, "estacionesBaseReducidas")
    id_map = DiccionarioEnlazado()
    contador = 1

    for grupo in grupos.recorrer():
        nombre = ""
        ids = []
        for est_id in grupo.estaciones.recorrer():
            nombre += est_id + ", "
            ids.append(est_id)
        nombre = nombre.rstrip(", ")
        id_reducido = f"e{contador:02}"
        for eid in ids:
            id_map.asignar(eid, id_reducido)
        ET.SubElement(estaciones_elem, "estacion", id=id_reducido, nombre=nombre)
        contador += 1

    def agregar_sensores(tag, sensores, matriz):
        sensores_elem = ET.SubElement(campo_elem, tag)
        for sensor in sensores.recorrer():
            sensor_elem = ET.SubElement(sensores_elem, sensor.__class__.__name__, id=sensor.id, nombre=sensor.nombre)
            freqs = DiccionarioEnlazado()
            for est_id, frec_dict in matriz.recorrer():
                freq = frec_dict.obtener(sensor.id)
                if freq and freq > 0:
                    id_red = id_map.obtener(est_id)
                    actual = freqs.obtener(id_red)
                    if actual is None:
                        freqs.asignar(id_red, freq)
                    else:
                        freqs.asignar(id_red, actual + freq)
            for est_id, freq in freqs.recorrer():
                ET.SubElement(sensor_elem, "frecuencia", idEstacion=est_id).text = str(freq)

    agregar_sensores("sensoresSuelo", campo.sensores_suelo, matriz_suelo)
    agregar_sensores("sensoresCultivo", campo.sensores_cultivo, matriz_cultivo)

    tree = ET.ElementTree(root)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)