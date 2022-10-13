from Compilador.Interfaces.nodo import Nodo


class Parametro_funcion(Nodo):
    def __init__(self,token,idnodo,id,tipoParametro,esMutable,esPorReferencia,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.tipoParametro = tipoParametro
        self.esMutable = esMutable
        self.esPorReferencia = esPorReferencia
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        pass

    def calcTam(self):
        return 0
