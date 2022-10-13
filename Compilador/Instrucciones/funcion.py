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

        # Primero se inserta el return por lo que se verifica si la funcion cuenta con el return
        for instruccion in self.listaInstrucciones:
            if instruccion.nombre == "RETURN":
                instruccion.crearTabla(self.entorno)
                break


        #Se insertan en la tabla de simbolos los parametros si es que posee
        if self.listaParametros is not None:
            for parametro in self.listaParametros:
                parametro.crearTabla(self.entorno)


        #***Se insertan en la tabla de simbolos las declaraciones que se encuntren en las instrucciones de la funcion***
        for instruccion in self.listaInstrucciones:
            if instruccion.nombre != "RETURN":
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

        if self.id == "main":
            self.expresion += "return 0;\n"
        self.expresion += "}\n"
        return self.expresion



    def calcTam(self):
        #print("CALCULANDO TAMAÑO DE FUNCION")
        tam = 0
        if self.listaParametros is not None:
            for parametro in self.listaParametros:
                tam += parametro.calcTam()
        for instruccion in self.listaInstrucciones:
            tam += instruccion.calcTam()
        #print(tam)
        return tam