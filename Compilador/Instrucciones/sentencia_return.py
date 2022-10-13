from Compilador.Interfaces.nodo import Nodo


class Return(Nodo):
    def __init__(self,token,idnodo,valorRetornado,linea,columna):
        super().__init__(token,idnodo)
        self.valorRetornado = valorRetornado
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        return "return"

    def calcTam(self):
        return 0