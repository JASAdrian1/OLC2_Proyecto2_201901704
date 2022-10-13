from Compilador.Interfaces.nodo import Nodo


class Parametro_llamada(Nodo):
    def __init__(self,token,idnodo,valor,esPorReferencia,esMutable):
        super().__init__(token,idnodo)
        self.valor = valor
        self.esPorReferencia = esPorReferencia
        self.esMutable = esMutable

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.expresion += self.valor.crearCodigo3d(ts)
        self.ref = self.valor.ref
        return self.expresion

    def calcTam(self):
        return 0