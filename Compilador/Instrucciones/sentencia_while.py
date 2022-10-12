from Compilador.Entorno import entorno
from Compilador.Interfaces.nodo import Nodo
from Compilador import generador
from Compilador.Instrucciones.sentencia_if import Sentencia_If
from Compilador.Instrucciones.sentencia_match import Sentencia_Match



class Sentencia_While(Nodo):
    def __init__(self, token, idnodo, condicion, instrucciones, linea, columna):
        super().__init__(token, idnodo)
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
        self.etiquetaInicio = []
        self.etiquetaSalida = []
        self.entorno = entorno.Entorno("while")

    def crearTabla(self, ts):
        self.entorno.entornoAnterior = ts
        self.entorno.crearListaNombresEntorno()

        for instruccion in self.instrucciones:
            instruccion.crearTabla(self.entorno)


    def crearCodigo3d(self,ts):
        self.etiquetaInicio = []
        self.etiquetaSalida = []

        self.etiquetaInicio.append(generador.nuevaEtiqueta())
        self.condicion.crearCodigo3d(ts)

        self.etiquetaSalida = (self.condicion.etiF)
        self.etiV = self.condicion.etiV


        self.entorno.listaEtiquetas.append(self.etiquetaInicio[0])
        self.entorno.listaEtiquetas.append(self.etiquetaSalida[0])

        self.expresion += generador.soltarEtiqueta(self.etiquetaInicio)
        self.expresion += self.condicion.expresion

        self.expresion += generador.soltarEtiqueta(self.etiV)
        if self.instrucciones is not None:
            for instruccion in self.instrucciones:
                exp_instruccion = instruccion.crearCodigo3d(self.entorno)
                if exp_instruccion == "break":
                    self.expresion += generador.generarGoto(self.etiquetaSalida[0])
                elif exp_instruccion == "continue":
                    self.expresion += generador.generarGoto(self.etiquetaInicio[0])
                else:
                    self.expresion += exp_instruccion

        #Se remueven las dos etiquetas que se agregaro a la listas de etiquetas
        del self.entorno.listaEtiquetas[-1]
        del self.entorno.listaEtiquetas[-1]

        self.expresion += generador.soltarEtiqueta(self.etiquetaSalida)

        return self.expresion


    def calcTam(self):
        tam = 0
        for instruccion in self.instrucciones:
            tam += instruccion.calcTam()
        return tam