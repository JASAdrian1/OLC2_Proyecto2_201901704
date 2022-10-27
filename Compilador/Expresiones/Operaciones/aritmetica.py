from Compilador import generador
from Compilador.Entorno import entorno
from Compilador.Entorno.error import Error
from Compilador.Expresiones.primitivo import Primitivo
from Compilador.Instrucciones.println import Println
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo, Tipo
from Compilador.generador import nuevoTemporal


class Aritmetica(Nodo):
    def __init__(self, token, idNodo, exp1, exp2, expu, signo,linea,columna):
        super().__init__(token,idNodo)
        self.exp1 = exp1
        self.exp2 = exp2
        self.tipo = exp1.tipo
        print("Exp1 tipo: ",exp1.tipo)
        self.expu = expu
        self.signo = signo
        self.linea =linea
        self.columna = columna

    def crearCodigo3d(self,ts):
        if self.expu is False:
            self.exp1.crearCodigo3d(ts)
            self.exp2.crearCodigo3d(ts)
            tipoVar = self.exp1.tipo
            if len(self.exp1.expresion) >1:
                self.expresion += self.exp1.expresion
            if len(self.exp2.expresion) >1:
                self.expresion += self.exp2.expresion
            self.ref = nuevoTemporal()
            signo = " "+self.signo+" "  #variable creada unicamente para agregar espacios al signo
            print("TTTT ",self.tipo)
            print(self.exp1.tipo.tipo_enum)
            print(self.exp2.tipo.tipo_enum)
            if self.exp1.tipo.tipo_enum != self.exp2.tipo.tipo_enum:
                entorno.lista_errores.append(Error("SEMANTICO","Operacion aritmetica entre dos operadores no validos",1,1))
                print("Error encontrado en expresiones aritmeticas. Linea: "+ str(self.linea))
                error = Primitivo(self.token, -1, "ERROR. Los tipos de los operadores no coinciden en la operacion aritmetica"
                                                  " Linea: "+ str(self.linea), "STRING",self.linea,self.columna)
                impresionError = Println(self.token, -1, error, None, 0, 0)
                impresionError.crearCodigo3d(ts)
                self.expresion += impresionError.expresion
                self.tipo = Tipo("ERROR")
                return self.expresion
            if tipoVar.tipo_enum != tipo.STR and tipoVar.tipo_enum != tipo.STRING:
                if self.signo == "+" or self.signo == "-" or self.signo == "*" or self.signo == "/" or self.signo == "^":
                    if self.signo == "/":
                        etiError = [generador.nuevaEtiqueta()]
                        etiSalida = [generador.nuevaEtiqueta()]

                        self.expresion += "if (" + str(self.exp2.ref) + " == 0)" + generador.generarGoto(etiError[0])
                        self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + signo + str(self.exp2.ref) + ";\n"
                        self.expresion += generador.generarGoto(etiSalida[0])
                        self.expresion += generador.soltarEtiqueta(etiError)
                        self.expresion += "//*ERROR*. Se ha dividido un valor dentro de 0\n"
                        error = Primitivo(self.token,-1,"ERROR. Division entre 0","STRING",0,0)
                        impresionError = Println(self.token,-1,error,None,0,0)
                        impresionError.crearCodigo3d(ts)
                        self.expresion += impresionError.expresion
                        self.expresion += generador.soltarEtiqueta(etiSalida)
                    else:
                        self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + signo + str(self.exp2.ref) + ";\n"
            else:
                tempPosExp1 = generador.nuevoTemporal()
                tempPosExp2 = generador.nuevoTemporal()

                etiSalida = [generador.nuevaEtiqueta()]
                etiInicio = [generador.nuevaEtiqueta()]

                self.expresion += tempPosExp1 + " = " + str(self.exp1.ref) + ";\n"
                self.expresion += tempPosExp2 + " = heap[(int)" + tempPosExp1 + "];\n"

                print("ssssss")
                print(self.exp1.ref)
                #simboloExp1 = ts.get(self.exp1.pos)
                self.expresion += generador.soltarEtiqueta(etiInicio)
                self.expresion += "if(" + tempPosExp2 + " == -1)" + generador.generarGoto(etiSalida[0])
                self.expresion += tempPosExp1 + " = " + tempPosExp1 + "+ 1;\n"
                self.expresion += tempPosExp2 + " = heap[(int)" + tempPosExp1 + "];\n"
                self.expresion += generador.generarGoto(etiInicio[0])

                self.expresion += generador.soltarEtiqueta(etiSalida)
                self.expresion += "heap[(int)" + tempPosExp1 + "] = " + str(self.exp2.ref) + ";\n"
                self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + ";\n"


            #***ASIGNACION DE TIPO PROVISIONAL (FALTA QUE REALIZAR LA VALIDACION QUE LOS TIPOS DE LAS DOS EXPRESIONES COINCIDAN)
            self.tipo = self.exp1.tipo
            #print("tipo (expresion): ",self.tipo.tipo_string)
            #print(self.expresion, end="")
        else:
            self.exp1.crearCodigo3d(ts)
            if len(self.exp1.expresion) >1:
                self.expresion += self.exp1.expresion
            self.ref = nuevoTemporal()
            self.expresion += str(self.ref) + " = " + self.signo + str(self.exp1.ref) + ";\n"
            signo = " " + self.signo + " "  # variable creada unicamente para agregar espacios al signo
        return self.expresion

    def crearTabla(self,ts):
        self.exp1.crearTabla(ts)
        self.tipo = self.exp1.tipo


    def calcTam(self):
        return 0

