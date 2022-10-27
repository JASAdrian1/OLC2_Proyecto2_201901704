from Compilador import generador
from Compilador.Entorno import entorno
from Compilador.Entorno.entorno import Entorno
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import Tipo


class Sentencia_for(Nodo):
    def __init__(self,token,idnodo,recorrido,instruciones,linea,columna):
        super().__init__(token,idnodo)
        self.recorrido = recorrido
        self.instrucciones = instruciones
        self.linea = linea
        self.columna = columna
        self.entorno = Entorno("for")


    def crearTabla(self,ts):
        self.entorno.entornoAnterior = ts
        self.entorno.funcionEnEjecucion = ts.funcionEnEjecucion
        self.entorno.crearListaNombresEntorno()

        if self.recorrido.objetoARecorrer is None:
            nuevoSimbolo = Simbolo(self.recorrido.id.id,Tipo("I64"),"variable",1,self.entorno.nombre,self.entorno.getUltimaPosStack(),self.recorrido.id.posHeap,self.linea,self.columna)
            self.entorno.put(self.recorrido.id.id,nuevoSimbolo)
            entorno.tabla_simbolos_global.append(nuevoSimbolo)
        else:
            nuevoSimbolo = Simbolo(self.recorrido.id.id, self.recorrido.objetoARecorrer.tipo_dato, "variable", 1, self.entorno.nombre,
                                   self.entorno.getUltimaPosStack(), self.recorrido.id.posHeap,self.linea,self.columna)
            self.entorno.put(self.recorrido.id.id, nuevoSimbolo)
            entorno.tabla_simbolos_global.append(nuevoSimbolo)

        self.recorrido.id.crearTabla(self.entorno)

        for instruccion in self.instrucciones:
            instruccion.crearTabla(self.entorno)

    def crearCodigo3d(self,ts):
        self.etiquetaInicio = []
        self.etiquetaSalida = []



        self.etiquetaInicio.append(generador.nuevaEtiqueta())
        self.etiquetaSalida.append(generador.nuevaEtiqueta())


        if self.recorrido.objetoARecorrer is None:
            tempRecorrido = generador.nuevoTemporal()
            self.recorrido.id.ref = tempRecorrido

            simbolo = self.entorno.get(self.recorrido.id.id, "variable")
            tempPosSimb = generador.nuevoTemporal()
            self.expresion += tempPosSimb + " = P + " + str(simbolo.direccionRel) + ";\n"

            tempDesplazamiento = generador.nuevoTemporal()

            self.recorrido.inicio.crearCodigo3d(self.entorno)
            self.recorrido.fin.crearCodigo3d(self.entorno)

            self.expresion += self.recorrido.inicio.expresion
            self.expresion += tempRecorrido + " = " + str(self.recorrido.inicio.ref) + ";\n"
            self.expresion += "stack[(int)" + tempPosSimb + "] =" + tempRecorrido + ";\n"
            self.expresion += self.recorrido.fin.expresion

            self.expresion += tempDesplazamiento + " = 1;\n"
            self.expresion += "if (" + str(self.recorrido.inicio.ref) + "<" + str(self.recorrido.fin.ref) + ") " + \
                              generador.generarGoto(self.etiquetaInicio[0])
            self.expresion += tempDesplazamiento + " = -1;\n"
            self.expresion += generador.soltarEtiqueta(self.etiquetaInicio)
            self.expresion += "if (" + str(self.recorrido.id.ref) + "==" + str(self.recorrido.fin.ref) + ") " + \
                              generador.generarGoto(self.etiquetaSalida[0])
            for instruccion in self.instrucciones:
                instruccion.crearCodigo3d(self.entorno)
                self.expresion += instruccion.expresion

            self.expresion += tempRecorrido + " = " + tempRecorrido + " + " + tempDesplazamiento + ";\n"
            self.expresion += "stack[(int)" + tempPosSimb + "] =" + tempRecorrido + ";\n"
            self.expresion += generador.generarGoto(self.etiquetaInicio[0])

            self.expresion += generador.soltarEtiqueta(self.etiquetaSalida)


        return self.expresion

    def calcTam(self):
        return 1