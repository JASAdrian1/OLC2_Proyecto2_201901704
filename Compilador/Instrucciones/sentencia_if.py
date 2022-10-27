from Compilador import generador
from Compilador.Entorno import entorno
from Compilador.Entorno.entorno import Entorno
from Compilador.Entorno.error import Error
from Compilador.Expresiones.primitivo import Primitivo
from Compilador.Instrucciones.println import Println
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo, Tipo


class Sentencia_If(Nodo):
    def __init__(self,token, idnodo, condicion, instruccionesif,instruccioneselse,linea,columna):
        super().__init__(token,idnodo)
        self.condicion = condicion
        self.instruccionesif = instruccionesif
        self.instruccioneselse = instruccioneselse
        self.etiSalida = []
        self.entornoIf = Entorno("if")
        self.entornoElse = Entorno("else")
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        self.entornoIf.entornoAnterior = ts
        self.entornoElse.entornoAnterior = ts
        self.entornoIf.funcionEnEjecucion = ts.funcionEnEjecucion
        self.entornoElse.funcionEnEjecucion = ts.funcionEnEjecucion

        self.entornoIf.crearListaNombresEntorno()
        self.entornoElse.crearListaNombresEntorno()

        for instruccion in self.instruccionesif:
            instruccion.crearTabla(self.entornoIf)

        if self.instruccioneselse is not None:
            for instruccion in self.instruccioneselse:
                instruccion.crearTabla(self.entornoElse)

    def crearCodigo3d(self,ts):
        self.etiSalida = []
        self.etiSalida.append(generador.nuevaEtiqueta())  # SE GENERA UNA ETIQUETA PARA SALIR DE LA INSTRUCCION IF

        print(self.condicion.tipo.tipo_enum)
        if self.condicion.tipo.tipo_enum != tipo.BOOL:
            entorno.lista_errores.append(Error("SEMANTICO", "La condicion del if no es de tipo booleano", 1, 1))
            error = Primitivo(self.token, -1,
                              "ERROR.La condicion del if no es de tipo booleano", "STRING", 0,
                              0)
            impresionError = Println(self.token, -1, error, None, self.linea, self.columna)
            impresionError.crearCodigo3d(ts)
            self.expresion += impresionError.expresion
            self.tipo = Tipo("ERROR")
            return self.expresion

        self.expresion += self.condicion.crearCodigo3d(ts)
        self.expresion += generador.soltarEtiqueta(self.condicion.etiV) #SE MUESTRAN LAS ETIQUETAS VERDADERAS

        self.entornoIf.listaEtiquetas = ts.listaEtiquetas
        self.entornoElse.listaEtiquetas = ts.listaEtiquetas

        #<---- EN ESTE ESPACIO DE AQUI SE DEBERIA GENERA EL CODIGO DE LAS INSTRUCCIONES----->
        self.expresion += "//CODIGO GENERADO POR LAS INSTRUCCIONES DENTRO DE IF\n"
        for instruccion in self.instruccionesif:
            exp_instruccion = instruccion.crearCodigo3d(self.entornoIf)
            if exp_instruccion == "break":
                print(ts.nombre)
                print(ts.listaEtiquetas)
                if len(ts.listaEtiquetas) == 0:
                    entorno.lista_errores.append(Error("SEMANTICO", "El break no se encuentra dentro de un ciclo", 1, 1))
                    error = Primitivo(self.token, -1,
                                      "ERROR.El break no se encuentra dentro de un ciclo", "STRING", 0,
                                      0)
                    impresionError = Println(self.token, -1, error, None, self.linea, self.columna)
                    impresionError.crearCodigo3d(ts)
                    self.expresion = impresionError.expresion
                    self.tipo = Tipo("ERROR")
                    return self.expresion
                self.expresion += generador.generarGoto(ts.listaEtiquetas[-1])      #Se insertas las etiquetas en listaEtiquetas desde las instrucciones de los bucles
            elif exp_instruccion == "continue":
                self.expresion += generador.generarGoto(ts.listaEtiquetas[-2])
            else:
                self.expresion += exp_instruccion


        self.expresion += generador.generarGoto(self.etiSalida[0])  #SE MUESTRAN LAS ETIQUETAS DE LA CONDICION FALAS
        self.expresion += generador.soltarEtiqueta(self.condicion.etiF)

        # <---- EN ESTE ESPACIO DE AQUI SE DEBERIA GENERA EL CODIGO DE LAS INSTRUCCIONES ELSE----->
        self.expresion += "//CODIGO GENERADO POR LAS INSTRUCCIONES DENTRO DE ELSE EN CASO EXISTA\n"
        if self.instruccioneselse is not None:
            for instruccion in self.instruccioneselse:
                exp_instruccion = instruccion.crearCodigo3d(self.entornoElse)
                if exp_instruccion == "break":
                    self.expresion += generador.generarGoto(ts.listaEtiquetas[-1])
                elif exp_instruccion == "continue":
                    self.expresion += generador.generarGoto(ts.listaEtiquetas[-2])
                else:
                    self.expresion += exp_instruccion


        self.expresion += generador.soltarEtiqueta(self.etiSalida)
        print("-----------------")
        entorno.mostrarSimbolos(self.entornoIf)
        return self.expresion

    def calcTam(self):
        tam = 0
        for instruccion in self.instruccionesif:
            tam += instruccion.calcTam()
        if self.instruccioneselse is not None:
            for instruccion in self.instruccioneselse:
                tam += instruccion.calcTam()
        return tam