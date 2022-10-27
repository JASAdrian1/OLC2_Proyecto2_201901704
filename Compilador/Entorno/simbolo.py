


class Simbolo:
    def __init__(self, id, tipo_dato, tipo_simbolo, size,entorno,direccionRel, direccionAbs,linea,columna,dimensiones=None,tipoElementos=None):
        self.id = id
        self.tipo_dato = tipo_dato
        self.tipo_simbolo = tipo_simbolo
        self.size = size
        self.entorno = entorno
        self.direccionRel = direccionRel
        self.direccionAbs = direccionAbs
        self.dimensiones = dimensiones
        self.tipo_elementos = tipoElementos
        self.parametros = []
        self.linea = linea
        self.columna = columna
