from Compilador.Entorno import entorno
from Compilador.Interfaces.nodo import Nodo
from Compilador import generador


class Brazo_Match(Nodo):
    def __init__(self, token, idnodo, coincidencias, instrucciones, linea, columna):
        super().__init__(token, idnodo)
        self.coincidencias = coincidencias
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
        self.entorno = entorno.Entorno("match")

    def crearTabla(self,ts):
        self.entorno.entornoAnterior = ts
        self.entorno.funcionEnEjecucion = ts.funcionEnEjecucion
        self.entorno.crearListaNombresEntorno()

        for instruccion in self.instrucciones:
            instruccion.crearTabla(self.entorno)

    def crearCodigo3d(self,ts):
        pass

    def calcTam(self):
        tam = 0
        for instruccion in self.instrucciones:
            tam += instruccion.calcTam()
        return tam

    def crearCodigo3D(self,ts, condicion, etiF, etiSalida):
        etiV = []
        etiV.append(generador.nuevaEtiqueta())
        for coincidencia in self.coincidencias:
            self.expresion += "if (" + str(condicion.ref) + " == " + str(coincidencia.ref) + ") " + generador.generarGoto(etiV[0])
        self.expresion += generador.generarGoto(etiF)

        self.expresion += generador.soltarEtiqueta(etiV)
        self.expresion += "//AQUI SE EJECUTAN LAS INSTRUCCIONES DENTRO DEL BRAZO\n"
        for instruccion in self.instrucciones:
            exp_instruccion = instruccion.crearCodigo3d(self.entorno)
            if exp_instruccion == "break":
                self.expresion += generador.generarGoto(ts.listaEtiquetas[-1])    #Se insertas las etiquetas en listaEtiquetas desde las instrucciones de los bucles
            elif exp_instruccion == "continue":
                self.expresion += generador.generarGoto(ts.listaEtiquetas[-2])
            else:
                self.expresion += exp_instruccion

        self.expresion += generador.generarGoto(etiSalida)
        return self.expresion