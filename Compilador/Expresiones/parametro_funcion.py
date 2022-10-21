from Compilador.Entorno import entorno
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo


class Parametro_funcion(Nodo):
    def __init__(self,token,idnodo,id,tipoParametro,esMutable,esPorReferencia,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.tipoParametro = tipoParametro
        self.esMutable = esMutable
        self.esPorReferencia = esPorReferencia
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        print("TIPO (parametro funcion):",self.tipoParametro.tipo_enum)
        if self.tipoParametro.tipo_enum != tipo.ARRAY and self.tipoParametro.tipo_enum != tipo.VEC:
            nuevoSimbolo = Simbolo(self.id,self.tipoParametro,"parametro",1,ts.nombre,ts.getUltimaPosStack(),-1)
            ts.put(self.id, nuevoSimbolo)
            entorno.tabla_simbolos_global.append(nuevoSimbolo)
        else:
            nuevoSimbolo = Simbolo(self.id, self.tipoParametro, "parametro", 1, ts.nombre, ts.getUltimaPosStack(), -1)
            print("DIMENSIONES: ",self.tipoParametro.dimensiones)
            print(self.tipoParametro.tipo_enum)
            print(nuevoSimbolo.tipo_elementos)
            nuevoSimbolo.tipo_elementos = self.tipoParametro.tipoElementos
            nuevoSimbolo.dimensiones = self.tipoParametro.dimensiones
            ts.put(self.id, nuevoSimbolo)
            entorno.tabla_simbolos_global.append(nuevoSimbolo)
        #FALTA QUE AGREGAR EL CASO EN DONDE LA VARIABLE SEA DE TIPO STRING

    def crearCodigo3d(self,ts):
        pass

    def calcTam(self):
        print(self.id)
        if self.tipoParametro.tipo_enum == tipo.I64 or self.tipoParametro.tipo_enum == tipo.F64 or self.tipoParametro.tipo_enum == tipo.BOOL or self.tipoParametro.tipo_enum == tipo.CHAR:
            return 1
        return 0
