from Compilador import generador
from Compilador.Entorno import entorno
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo
import numpy as np



class Declaracion_arreglo(Nodo):
    def __init__(self,token,idnodo,id,valor,tipo,tipoElementos,estructuraArreglos,esMutable,linea,columna):
        super().__init__(token,idnodo)
        self.listaid = id
        self.valor = valor
        self.tipo = tipo
        self.tipoElementos = tipoElementos
        self.estructuraArreglos = estructuraArreglos
        self.esMutable = esMutable
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        dimensiones = self.estructuraArreglos[:]
        dimensiones.pop(0)
        dimensiones.reverse()
        for id in self.listaid:
            posHeap = entorno.posHeap
            nuevoSimbolo = Simbolo(id,self.tipo,"variable",1,ts.nombre,ts.getUltimaPosStack(),posHeap,dimensiones,self.tipoElementos)
            ts.put(id,nuevoSimbolo)
            entorno.tabla_simbolos_global.append(nuevoSimbolo)

            #Se calcula el espacion que ocupa el arreglo en el heap para mover el puntero
            #print(self.estructuraArreglos)
            #print(self.valor)
            #print(dimensiones)
            espacioOcupado = 1
            for dimension in dimensiones:
                espacioOcupado *= dimension
            espacioOcupado += len(dimensiones)
            print("Espacio que ocupa arreglo en heap: ",espacioOcupado)
            entorno.posHeap += espacioOcupado


    def crearCodigo3d(self,ts):
        dimensiones = self.estructuraArreglos[:]
        dimensiones.pop(0)
        dimensiones.reverse()
        print("dimensiones",dimensiones)

        tempInicioArray = generador.nuevoTemporal()
        tempPosVariable = generador.nuevoTemporal()

        self.expresion += tempInicioArray + " = H;\n"
        for dimension in dimensiones:
            self.expresion += "heap[(int)H] = " + str(dimension) + ";\n"
            self.expresion += generador.generarAumentoHeap()

        arrLineal = np.array(self.valor)
        arrLineal = arrLineal.flatten()
        for elemento in arrLineal:
            elemento.crearCodigo3d(ts)
            self.expresion += elemento.expresion
            self.expresion += "heap[(int)H] = " + str(elemento.ref) + ";\n"
            self.expresion += generador.generarAumentoHeap()

        self.expresion += tempPosVariable + " = P + "+str(ts.get(self.listaid[0]).direccionRel)+";\n"
        self.expresion += "stack[(int)" + tempPosVariable +"] = " + tempInicioArray + ";\n"


        return self.expresion

    def calcTam(self):
        return 1
