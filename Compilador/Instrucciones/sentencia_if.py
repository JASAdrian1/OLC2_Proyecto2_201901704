from Compilador import generador
from Compilador.Interfaces.nodo import Nodo


class Sentencia_If(Nodo):
    def __init__(self,token, idnodo, condicion, instruccionesif,instruccioneselse):
        super().__init__(token,idnodo)
        self.condicion = condicion
        self.instruccionesif = instruccionesif
        self.instruccioneselse = instruccioneselse

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.expresion += self.condicion.crearCodigo3d(ts)
        self.expresion += generador.mostrarEtiquetas(self.condicion.etiV,self.condicion.etiF)
        return self.expresion