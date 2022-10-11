from Compilador.Interfaces.nodo import Nodo


class Parametro(Nodo):
    def __init__(self,token,idnodo,id,tipo,esMutable,esReferencia,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.tipo = tipo
        self.esMutable = esMutable
        self.esReferencia = esReferencia
        self.linea = linea
        self.columna = columna