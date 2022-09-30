
temporal = 0
etiqueta = 0
posHeap = 0


def nuevoTemporal():
    global temporal
    temporal += 1
    return "T"+str(temporal)

def nuevaEtiqueta():
    global etiqueta
    etiqueta += 1
    return "L"+str(etiqueta)


def soltar(etiqueta):
    for eti in etiqueta:
        print(eti,":")


def agregarEtiqueta(etiqueta1, etiqueta2):
    listaEtiquetas = etiqueta1
    listaEtiquetas.append(etiqueta2)
    return listaEtiquetas

