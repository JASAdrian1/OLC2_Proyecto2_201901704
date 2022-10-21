from Compilador.Interfaces.nodo import Nodo


class Acceso_Vector(Nodo):
    def __init__(self,token,idnodo,id,accesoVector,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.accesoVector = accesoVector
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        pass

    def calcTam(self):
        return 0