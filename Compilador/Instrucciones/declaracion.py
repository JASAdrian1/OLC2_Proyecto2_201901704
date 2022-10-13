from Compilador.Entorno import entorno
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo
from Compilador import generador
from Compilador.TablaSimbolo.tipo import tipo


class Declaracion(Nodo):
    def __init__(self,token, idnodo, tipo, valor, listaid, esMutable, fila, columna):
        super().__init__(token,idnodo)
        self.listaid = listaid
        self.valor = valor
        self.tipo = tipo
        self.esMutable = esMutable
        self.fila = fila
        self.columna = columna
        self.tipoSimbolo = "variable"
        #print("Tipo (declaracion): ",self.tipo.tipo_string)

    def crearTabla(self,ts):
        for id in self.listaid:
            print(self.tipo.tipo_enum)
            if(self.tipo.tipo_enum != tipo.STR):
                nuevoSimbolo = Simbolo(id, self.tipo,self.tipoSimbolo,1, ts.nombre, ts.getUltimaPosStack(),-1)
                ts.put(id, nuevoSimbolo)
                entorno.tabla_simbolos_global.append(nuevoSimbolo)
            entorno.desplazamiento += 1     #<---Verificar si esta variable se está usando xd

    def crearCodigo3d(self,ts):
        self.expresion += "//Realizando declaracion"+"\n"
        tempValor = generador.nuevoTemporal()

        self.expresion += self.valor.crearCodigo3d(ts)
        for id in self.listaid:
            if self.tipo.tipo_enum == tipo.I64 or self.tipo.tipo_enum == tipo.F64:
                self.expresion += tempValor + " = " + str(self.valor.ref)+";\n"
            elif self.tipo.tipo_enum == tipo.BOOL:
                print("-",self.valor.exp1)

            #Se genera el temporal y la posicion del stack donde se guardara la varible
            tempPosVariable = generador.nuevoTemporal()
            #print(id)
            self.expresion += tempPosVariable + " = P + "+str(ts.get(id).direccionRel)+";\n"
            self.expresion += "stack[(int)"+tempPosVariable+"] = " + tempValor+";\n"
        return self.expresion


    def calcTam(self):
        if self.tipo.tipo_enum == tipo.I64 or self.tipo.tipo_enum == tipo.F64 or self.tipo.tipo_enum == tipo.BOOL or self.tipo.tipo_enum == tipo.CHAR:
            return 1
        return 0