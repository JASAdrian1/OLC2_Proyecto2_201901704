from Compilador.Entorno import entorno
from Compilador.Interfaces.nodo import Nodo
from Compilador import generador


class Sentencia_Loop(Nodo):
    def __init__(self, token, idnodo, instrucciones, linea, columna):
        super().__init__(token,idnodo)
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
        self.etiInicio = []
        self.etiSalida = []
        self.entorno = entorno.Entorno("loop")

    def crearTabla(self,ts):
        self.entorno.entornoAnterior = ts
        self.entorno.crearListaNombresEntorno()

        for instruccion in self.instrucciones:
            instruccion.crearTabla(self.entorno)

    def crearCodigo3d(self,ts):
        self.etiInicio = []
        self.etiSalida = []

        self.etiInicio.append(generador.nuevaEtiqueta())
        self.etiSalida.append(generador.nuevaEtiqueta())

        self.entorno.listaEtiquetas.append(self.etiInicio[0])
        self.entorno.listaEtiquetas.append(self.etiSalida[0])

        self.expresion += generador.soltarEtiqueta(self.etiInicio)
        if self.instrucciones is not None:
            for instruccion in self.instrucciones:
                expresion_instruccion = instruccion.crearCodigo3d(self.entorno)
                if expresion_instruccion == "break":
                    self.expresion += "goto " + self.etiSalida[0] + "\n"
                elif expresion_instruccion == "continue":
                    self.expresion += "goto " + self.etiInicio[0] + "\n"
                else:
                    self.expresion += expresion_instruccion

        self.expresion += "goto "+ self.etiInicio[0]+"\n"
        self.expresion += generador.soltarEtiqueta(self.etiSalida)

        # Se remueven las dos etiquetas que se agregaro a la listas de etiquetas
        del self.entorno.listaEtiquetas[-1]
        del self.entorno.listaEtiquetas[-1]

        return self.expresion


    def calcTam(self):
        tam = 0
        for instruccion in self.instrucciones:
            tam += instruccion.calcTam()
        return tam
