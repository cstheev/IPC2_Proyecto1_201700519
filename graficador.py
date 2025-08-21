from graphviz import Digraph

def graficar_matriz(matriz, nombre_archivo):
    dot = Digraph()
    for est_id, sensores in matriz.items():
        dot.node(est_id, est_id)
        for sensor_id, freq in sensores.items():
            if freq > 0:
                dot.node(sensor_id, sensor_id)
                dot.edge(est_id, sensor_id, label=str(freq))
    dot.render(nombre_archivo, format='png', cleanup=True)
