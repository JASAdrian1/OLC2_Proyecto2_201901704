from Compilador import generador
from Compilador.Interfaces.nodo import Nodo
from Compilador.Entorno.entorno import getFuncionTablaGlobal


class Llamada_funcion_exp(Nodo):
    def __init__(self,token,idnodo,id,parametros,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.parametros = parametros
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        #Se busca en la tabla la funcion desde la que se ejecutara la llamada de la funcion
        funcionRaiz = getFuncionTablaGlobal(ts.funcionEnEjecucion)

        if self.parametros is not None:
            for parametro in self.parametros:
                parametro.crearCodigo3d(ts)
                self.expresion += parametro.expresion

        #Se aumenta le valor del apuntador del stack para empezar a almacenar los parametros de la funcion
        self.expresion += "P = P + " + str(funcionRaiz.size) + ";\n"

        funcionLlamada = getFuncionTablaGlobal(self.id)
        self.tipo = funcionLlamada.tipo_dato    #Se asigna el tipo que sera la llamada
        if funcionLlamada is not None:
            #EN DADO CASO LA FUNCION TENGA PARAMETROS, SE CREARA EL CODIGO 3 DE ESTOS
            if self.parametros is not None:
                desplazamientoParametro = 1  # Este desplazamiento se utiliza para ir guardando los parametros en el stack
                for parametro in self.parametros:
                    #parametro.crearCodigo3d(ts)
                    #self.expresion += parametro.expresion
                    tempPosParametro = generador.nuevoTemporal()
                    self.expresion += tempPosParametro + " = P + " + str(desplazamientoParametro) + ";\n"
                    self.expresion += "stack[(int)" + tempPosParametro + "] = " + str(parametro.ref) + ";\n"
                    desplazamientoParametro += 1
                #____________________FINALIZA CREACION DE CODIGO 3D PARA PARAMETROS______________________________-


            #generacion de codigo de llamada
            self.expresion += self.id + "();\n"

            tempPosReturn = generador.nuevoTemporal()
            self.expresion += tempPosReturn + " = P;\n"    #Posicion en la que se encuentra el valor del return de la llamada

            tempValReturn = generador.nuevoTemporal()   #Se almacena el valor del return en el stack
            self.expresion += tempValReturn + " = stack[(int)" + tempPosReturn + "]" + ";\n"
            self.ref = tempValReturn

            # Se disminuye le valor del apuntador del stack para al estado anterior a la llamada de la funcion
            self.expresion += "P = P - " + str(funcionRaiz.size) + ";\n"

            #self.expresion += ts.actualizarValorVariable()


        else:
            print("***ERROR*** La funcion que se esta llamando no de ha declarado, funcion:",self.id)

        return self.expresion

    def calcTam(self):
        return 0