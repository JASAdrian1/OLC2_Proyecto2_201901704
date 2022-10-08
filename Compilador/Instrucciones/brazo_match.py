from Compilador.Interfaces.nodo import Nodo
from Compilador import generador


class Brazo_Match(Nodo):
    def __init__(self, token, idnodo, coincidencias, instrucciones, linea, columna):
        super().__init__(token, idnodo)
        self.coincidencias = coincidencias
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        pass

    def crearCodigo3D(self,ts, condicion, etiF, etiSalida):
        etiV = []
        etiV.append(generador.nuevaEtiqueta())
        for coincidencia in self.coincidencias:
            self.expresion += "if (" + str(condicion.ref) + " == " + str(coincidencia.ref) + ") goto " + etiV[0] + "\n"
        self.expresion += "goto " + etiF + "\n"

        self.expresion += generador.soltarEtiqueta(etiV)
        self.expresion += "//AQUI SE EJECUTAN LAS INSTRUCCIONES DENTRO DEL BRAZO\n"
        for instruccion in self.instrucciones:
            exp_instruccion = instruccion.crearCodigo3d(ts)
            if exp_instruccion == "break":
                self.expresion += "goto " + ts.listaEtiquetas[-1] + "\n"
            elif exp_instruccion == "continue":
                self.expresion += "goto " + ts.listaEtiquetas[-2] + "\n"
            else:
                self.expresion += exp_instruccion

        self.expresion += "goto " + etiSalida + "\n"
        return self.expresion