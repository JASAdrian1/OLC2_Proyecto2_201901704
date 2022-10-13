from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo
from Compilador.Entorno import entorno
from Compilador.TablaSimbolo.tipo import tipo


class Funcion(Nodo):
    def __init__(self,token,idnodo,id,tipoFuncion,listaParametros,listaInstrucciones,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.tipoFuncion = tipoFuncion
        self.listaParametros = listaParametros
        self.listaInstrucciones = listaInstrucciones
        self.linea = linea
        self.columna = columna
        self.tipoSimbolo = "funcion"
        self.entorno = entorno.Entorno("global")

    def crearTabla(self,ts):
        self.entorno.crearListaNombresEntorno()
        self.entorno.funcionEnEjecucion = self.id

        nuevaFuncion = Simbolo(self.id,self.tipoFuncion,self.tipoSimbolo,0,ts.nombre,-1,entorno.getHeapLibre())
        print("id: ",self.id)
        self.entorno.put(self.id,nuevaFuncion)
        entorno.tabla_simbolos_global.append(nuevaFuncion)
        for instruccion in self.listaInstrucciones:
            print("instruccion (funcion): ",instruccion)
            instruccion.crearTabla(self.entorno)
        self.entorno.get(self.id,"funcion").size = self.calcTam()

    def crearCodigo3d(self,ts):
        tipoFuncion = ""

        if self.tipoFuncion is None:
            tipoFuncion = "void"
        else:
            if self.tipoFuncion.tipo_enum == tipo.I64:
                tipoFuncion = "int"
            elif self.tipoFuncion.tipo_enum == tipo.F64:
                tipoFuncion = "float"

        self.expresion += tipoFuncion + " " + self.id + "() {\n"
        for instruccion in self.listaInstrucciones:
            exp_instruccion = instruccion.crearCodigo3d(self.entorno)

            self.expresion += exp_instruccion
        self.expresion += "}\n"
        return self.expresion


    def calcTam(self):
        #print("CALCULANDO TAMAÑO DE FUNCION")
        tam = 0
        for instruccion in self.listaInstrucciones:
            tam += instruccion.calcTam()
        #print(tam)
        return tam