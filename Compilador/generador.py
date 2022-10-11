
temporal = 0
etiqueta = 0
codigoGenerado = ""

def nuevoTemporal():
    global temporal
    temporal += 1
    return "t"+str(temporal)

def nuevaEtiqueta():
    global etiqueta
    etiqueta += 1
    return "L"+str(etiqueta)


def soltarEtiqueta(etiqueta):
    cadena = ""
    for eti in etiqueta:
        cadena += eti + ":\n"
    return cadena

def unirEtiquetas(etiqueta1, etiqueta2):
    listaEtiquetas = etiqueta1
    for eti in etiqueta2:
        listaEtiquetas.append(eti)
    return listaEtiquetas


def generarGoto(eti):
    return "goto "+eti+";\n"

def mostrarEtiquetas(etiV, etiF):
    expresion = ""
    expresion += "#Etiquetas verdaderas\n"
    expresion += soltarEtiqueta(etiV)
    expresion += "#Etiquetas falsas\n"
    expresion += soltarEtiqueta(etiF)
    return expresion

def generarCodigo(cadena):
    global codigoGenerado
    codigoGenerado+=cadena+"\n"


def generarListaTemporales():
    lista = "float t0"
    for i in range(1,temporal+1):
        lista += ",t"+str(i)
    lista += ";"
    return lista
