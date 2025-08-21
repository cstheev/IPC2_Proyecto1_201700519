# procesador.py
import xml.etree.ElementTree as ET
from modelo import CampoAgricola, EstacionBase, SensorSuelo, SensorCultivo
from lista import Lista

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
                s.frecuencias[freq.get('idEstacion')] = int(freq.text)
            c.sensores_suelo.agregar(s)

        for sensor in campo.find('sensoresCultivo').findall('sensorT'):
            t = SensorCultivo(sensor.get('id'), sensor.get('nombre'))
            for freq in sensor.findall('frecuencia'):
                t.frecuencias[freq.get('idEstacion')] = int(freq.text)
            c.sensores_cultivo.agregar(t)

        campos.agregar(c)
    return campos

def generar_matriz_frecuencia(campo, tipo):
    matriz = {}
    sensores = campo.sensores_suelo if tipo == "suelo" else campo.sensores_cultivo
    for estacion in campo.estaciones.recorrer():
        matriz[estacion.id] = {}
        for sensor in sensores.recorrer():
            freq = sensor.frecuencias.get(estacion.id, 0)
            matriz[estacion.id][sensor.id] = freq
    return matriz

def generar_matriz_patron(matriz):
    patrones = {}
    for estacion_id, sensores in matriz.items():
        patron = tuple(1 if freq > 0 else 0 for freq in sensores.values())
        patrones[estacion_id] = patron
    return patrones

def agrupar_estaciones(patrones_suelo, patrones_cultivo):
    grupos = {}
    for est_id in patrones_suelo:
        patron_s = patrones_suelo[est_id]
        patron_t = patrones_cultivo.get(est_id, ())
        clave = (patron_s, patron_t)
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(est_id)
    return grupos

def escribir_salida(campo, grupos, matriz_suelo, matriz_cultivo, ruta_salida):
    root = ET.Element("camposAgricolas")
    campo_elem = ET.SubElement(root, "campo", id=campo.id, nombre=campo.nombre)

    estaciones_elem = ET.SubElement(campo_elem, "estacionesBaseReducidas")
    id_map = {}
    for i, grupo in enumerate(grupos.values(), start=1):
        nombre = ", ".join(grupo)
        id_reducido = f"e{i:02}"
        id_map.update({eid: id_reducido for eid in grupo})
        ET.SubElement(estaciones_elem, "estacion", id=id_reducido, nombre=nombre)

    def agregar_sensores(tag, sensores, matriz, tipo):
        sensores_elem = ET.SubElement(campo_elem, tag)
        for sensor in sensores.recorrer():
            sensor_elem = ET.SubElement(sensores_elem, sensor.__class__.__name__, id=sensor.id, nombre=sensor.nombre)
            freqs = {}
            for est_id, frec_dict in matriz.items():
                freq = frec_dict.get(sensor.id, 0)
                if freq > 0:
                    id_red = id_map.get(est_id)
                    freqs[id_red] = freqs.get(id_red, 0) + freq
            for est_id, freq in freqs.items():
                ET.SubElement(sensor_elem, "frecuencia", idEstacion=est_id).text = str(freq)

    agregar_sensores("sensoresSuelo", campo.sensores_suelo, matriz_suelo, "suelo")
    agregar_sensores("sensoresCultivo", campo.sensores_cultivo, matriz_cultivo, "cultivo")

    tree = ET.ElementTree(root)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)
