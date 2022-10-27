from Compilador import generador
from Compilador.Interfaces.nodo import Nodo


class Absoluto(Nodo):
    def __init__(self,token,idnodo,valor,linea,columna):
        super().__init__(token,idnodo)
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.valor.crearCodigo3d(ts)
        self.expresion += self.valor.expresion
        self.tipo = self.valor.tipo

        etiSalida = [generador.nuevaEtiqueta()]
        etiSalida2 = [generador.nuevaEtiqueta()]
        tempNuevo = generador.nuevoTemporal()
        tempMenosUno = generador.nuevoTemporal()

        self.expresion += tempMenosUno + " = -1; \n"
        self.expresion += "if( " + str(self.valor.ref) + " > 0 )" + generador.generarGoto(etiSalida[0])
        self.expresion += tempNuevo + " = " + str(self.valor.ref) + " * " + tempMenosUno + ";\n"
        generador.generarGoto(etiSalida[0])
        self.expresion += generador.soltarEtiqueta(etiSalida)
        self.expresion += tempNuevo + " = " + str(self.valor.ref) + ";\n"
        self.expresion += generador.soltarEtiqueta(etiSalida2)

        self.ref = tempNuevo
        return self.expresion


    def calcTam(self):
        return 0