import json

def cargar_datos(ruta):
    with open(ruta) as contenido:
        asignaciones = json.load(contenido)
        for asignacion in asignaciones["platoonAssignments"]:
            for k, v in asignacion.items():
                print(k, v)


if __name__ == '__main__':
    ruta = 'echobase-assignments-ROTE-P1_1_1.json'
    cargar_datos(ruta)