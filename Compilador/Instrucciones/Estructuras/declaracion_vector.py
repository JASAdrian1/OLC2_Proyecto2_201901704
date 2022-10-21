from Compilador import generador
from Compilador.Entorno import entorno
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo


class Declaracion_Vector(Nodo):
    def __init__(self,token,idnodo,id,inicializacion,tipo,tipoElementos,esMutable,withCapacity,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.inicializacion = inicializacion
        self.tipo = tipo
        self.tipoElementos = tipoElementos
        self.esMutable = esMutable
        self.withCapacity = withCapacity
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        for id in self.id:
            if self.withCapacity is None:
                if self.inicializacion is not None:
                    if self.inicializacion.repeticiones == 0:
                        if self.tipoElementos is None:
                            #print("++ ",self.inicializacion.expresion[0].tipo.tipo_enum)
                            tipoElementos = self.inicializacion.expresion[0].tipo
                        else:
                            tipoElementos = self.tipoElementos
                        posHeap = entorno.posHeap
                        nuevoSimbolo = Simbolo(id, self.tipo, "variable", 1, ts.nombre, ts.getUltimaPosStack(), posHeap)
                        nuevoSimbolo.tipo_elementos = tipoElementos
                        ts.put(id, nuevoSimbolo)
                        entorno.tabla_simbolos_global.append(nuevoSimbolo)

            # Se calcula el espacion que ocupa el arreglo en el heap para mover el puntero
            # print(self.estructuraArreglos)
            # print(self.valor)
            # print(dimensiones)
            espacioOcupado = len(self.inicializacion.expresion)*2
            print("Espacio que ocupa arreglo en heap: ", espacioOcupado)
            entorno.posHeap += espacioOcupado

    def crearCodigo3d(self,ts):
        tempInicioVec = generador.nuevoTemporal()
        tempPosVariable = generador.nuevoTemporal()

        self.expresion += tempInicioVec + " = H;\n"

        print(self.inicializacion.expresion)
        for elemento in self.inicializacion.expresion:
            elemento.crearCodigo3d(ts)
            self.expresion += elemento.expresion

            self.expresion += "heap[(int)H] = " + str(elemento.ref) + ";\n"
            self.expresion += generador.generarAumentoHeap()
            self.expresion += "heap[(int)H] = H + 1;\n"
            self.expresion += generador.generarAumentoHeap()

        #Se guarda al final del vector un apuntador con un -1 para indicar el final del vector
        tempUltPos = generador.nuevoTemporal()
        self.expresion += tempUltPos + " = " + "H - 1;\n"
        self.expresion += "heap[(int)"+ tempUltPos +"] = -1;\n"

        self.expresion += tempPosVariable + " = P + " + str(ts.get(self.id[0]).direccionRel) + ";\n"
        self.expresion += "stack[(int)" + tempPosVariable + "] = " + tempInicioVec + ";\n"


        return self.expresion



    def calcTam(self):
        return 1
