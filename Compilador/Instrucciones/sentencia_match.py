from Compilador.Entorno import entorno
from Compilador.Interfaces.nodo import Nodo
from Compilador import generador


class Sentencia_Match(Nodo):
    def __init__(self, token, idnodo, condicion, listaBrazo, brazoDefault, linea, columna):
        super().__init__(token,idnodo)
        self.condicion = condicion
        self.listaBrazo = listaBrazo
        self.brazoDefault = brazoDefault
        self.etiF = []
        self.etiSalida = []
        self.linea = linea
        self.columna = columna
        self.entornoDefault = entorno.Entorno("default")

    def crearTabla(self,ts):
        self.entornoDefault.entornoAnterior = ts
        self.entornoDefault.funcionEnEjecucion = ts.funcionEnEjecucion
        self.entornoDefault.crearListaNombresEntorno()

        for brazo in self.listaBrazo:
            brazo.crearTabla(ts)

        if self.brazoDefault is not None:
            for instruccion in self.brazoDefault:
                instruccion.crearTabla(self.entornoDefault)

    def crearCodigo3d(self,ts):
        self.etiF = []
        self.etiSalida = []

        self.condicion.crearCodigo3d(ts)
        self.etiF.append(generador.nuevaEtiqueta())
        self.etiSalida.append(generador.nuevaEtiqueta())

        self.expresion += self.condicion.expresion

        for brazo in self.listaBrazo:       #Se crea el codigo de cada uno de los brazos del match
            self.expresion += brazo.crearCodigo3D(ts, self.condicion, self.etiF[0], self.etiSalida[0])
            self.expresion += generador.soltarEtiqueta(self.etiF)
            self.etiF[0] = generador.nuevaEtiqueta()

        generador.etiqueta -= 1  # El ultimo brazo crea una etiqueta que no se utiliza, por lo que se diminue en 1 el conteo de etiquetas

        if self.brazoDefault is not None:
            self.expresion += "//CREANDO CODIGO DE INSTRUCCIONES DE BRAZO DEFAULT \n"
            for instruccion in self.brazoDefault:
                exp_instruccion = instruccion.crearCodigo3d(self.entornoDefault)
                if exp_instruccion == "break":
                    self.expresion += "goto " + self.entornoDefault.listaEtiquetas[-1] + "\n"
                else:
                    self.expresion += exp_instruccion


        self.expresion += generador.soltarEtiqueta(self.etiSalida)
        return self.expresion

    def calcTam(self):
        tam = 0
        for brazo in self.listaBrazo:
            tam += brazo.calcTam()
        for instruccion in self.brazoDefault:
            tam += instruccion.calcTam()
        return tam
    