from Compilador.Entorno import entorno
from Compilador.TablaSimbolo.tipo import Tipo, Tipo_Arreglo
from Compilador.Expresiones.primitivo import Primitivo
from Compilador.Expresiones.Operaciones.aritmetica import Aritmetica
from Compilador.Expresiones.to_string import To_string
from Compilador.Entorno.entorno import Entorno, mostrarSimbolos
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Expresiones.condicion import Condicion
from Compilador.Expresiones.condicion_relacional import Condicion_Relacional
from Compilador.Expresiones.condicion_logica import Condicion_Logica
from Compilador.Expresiones.identificador import Identificador
from Compilador.Instrucciones.sentencia_if import Sentencia_If
from Compilador.Instrucciones.declaracion import Declaracion
from Compilador.Instrucciones.asignacion import Asignacion
from Compilador.Instrucciones.sentencia_match import Sentencia_Match
from Compilador.Instrucciones.brazo_match import Brazo_Match
from Compilador.Instrucciones.sentencia_while import Sentencia_While
from Compilador.Instrucciones.sentencia_loop import Sentencia_Loop
from Compilador.Instrucciones.sentencia_for import Sentencia_for
from Compilador.Instrucciones.recorrido_for import Recorrido_for
from Compilador.Instrucciones.sentencia_break import Sentencia_Break
from Compilador.Instrucciones.sentencia_continue import Sentencia_Continue
from Compilador.Instrucciones.funcion import Funcion
from Compilador.Expresiones.parametro_funcion import Parametro_funcion
from Compilador.Instrucciones.llamada_funcion_ins import Llamada_funcion_ins
from Compilador.Expresiones.llamada_funcion_exp import Llamada_funcion_exp
from Compilador.Expresiones.parametro_llamada import Parametro_llamada
from Compilador.Instrucciones.sentencia_return import Sentencia_Return
from Compilador.Instrucciones.Estructuras.declaracion_arreglo import Declaracion_arreglo
from Compilador.Expresiones.acceso_arreglo import Acceso_Arreglo
from Compilador.Expresiones.len_arreglo import Len_Arreglo
from Compilador.Instrucciones.Estructuras.inicializacion_vector import Inicializacion_Vector
from Compilador.Instrucciones.Estructuras.declaracion_vector import Declaracion_Vector
from Compilador.Instrucciones.Estructuras.push_vector import Push_Vector
from Compilador.Instrucciones.Estructuras.insert_vector import Insert_Vector

from Compilador.Instrucciones.println import Println


from Compilador import generador

noNode = 0


# Palabras reservadas
reserved = {
    'let': 'LET',
    'mut': 'MUT',
    'i64': 'I64',
    'f64': 'F64',
    'bool': 'BOOL',
    'char': 'CHAR',
    'String': 'STRING',
    'usize': 'USIZE',
    'str': 'STR',
    'pow': 'POW',
    'abs': 'ABS',
    'sqrt': 'SQRT',
    'powf': 'POWF',
    'as': 'AS',
    'true': 'TRUE',
    'false': 'FALSE',
    'vec': 'VEC',
    'Vec': 'VECN',
    'new': 'NEW',
    'fn': 'FN',
    'println': 'PRINTLN',
    'if': 'IF',
    'else': 'ELSE',
    'match': 'MATCH',
    'loop': 'LOOP',
    'while': 'WHILE',
    'for': 'FOR',
    'in':'IN',
    'break': "BREAK",
    'return':'RETURN',
    'continue':'CONTINUE',
    'with': 'WITH',
    'capacity':'CAPACITY',
    'to':'TO',
    'string':'STRINGE',
    'push':'PUSH',
    'insert':'INSERT',
    'remove':'REMOVE',
    'contains':'CONTAINS',
    'len':'LEN'
}
# Simbolos
tokens = list(reserved.values()) + [
    'MAS',
    'POR',
    'DIV',
    'MOD',
    'MENOS',
    'MAYORIGUAL',
    'MAYORQUE',
    'MENORIGUAL',
    'MENORQUE',
    'DIFERENTE',
    'NOT',
    'IGUALIGUAL',
    'IGUAL',
    'OR',
    'AND',
    'PARA',
    'PARC',
    'CORA',
    'CORC',
    'LLAVEA',
    'LLAVEC',
    'COMA',
    'PYC',
    'DOSP',
    'PUNTO',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'CARACTER',
    'ID',
    'GUIONBAJO',
    'ORMATCH',
    'DOSPUNTOSCONTINUO',
    'AMPERSAND'
]

# Asignacion de tokens
t_MAS = r'\+'
t_POR = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_MENOS = r'-'
t_MAYORIGUAL = r'>='
t_MAYORQUE = r'>'
t_MENORIGUAL = r'<='
t_MENORQUE = r'<'
t_DIFERENTE = r'!='
t_NOT = r'!'
t_IGUALIGUAL = r'=='
t_IGUAL = r'='
t_OR = r'\|\|'
t_AND = r'&&'
t_PARA = r'\('
t_PARC = r'\)'
t_CORA = r'\['
t_CORC = r']'
t_LLAVEA = r'{'
t_LLAVEC = r'}'
t_COMA = r','
t_PYC = r';'
t_DOSP = r':'
t_DOSPUNTOSCONTINUO = r'\.\.'
t_PUNTO= r'\.'
t_GUIONBAJO = r'_'
t_ORMATCH = r'\|'
t_AMPERSAND = r'&'



# Expresiones regulares
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error al recibir un decimal %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Error al recibir un entero: ", t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'"([^"\n]|(\\"))*"'
    # print("Se ha reconocido la cadena: ",t.value)
    return t

def t_CARACTER(t):
    r'\'[a-zA-Z]\''
    print("Se ha reconocido el caracter: ", t.value)
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    try:
        t.type = reserved.get(t.value, "ID")
    except ValueError:
        print("Se esperaba un identificador")
        t.value = 'ERROR'
    return t

def t_COMMENT(t):
    r'\/\*.*\*\/'
    print("Comentario")
    pass

def t_COMMETN_2(t):
    r'\/\/.*'
    print("Comentario 2")
    pass


def t_COMMENT_MULTILINE(t):
    r'\/\*[^*\/]*\*\/'
    print("Comentario multiple lineas")
    pass



t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Error al leer '%s'" % t.value[0])
    t.lexer.skip(1)


#################INICIAN PRODUCCIONES######################
import Analizador.ply.lex as lex

lexer = lex.lex()

# SE DECLARA LA PRECEDENCIA
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'IGUALIGUAL', 'DIFERENTE', 'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV'),
    ('right', 'MOD'),
    ('left', 'UMENOS'),
    ('left','PUNTO')
)


def p_inicio(t):
    '''inicio : marc_sup instrucciones
    '''
    t[0] = t[2]
    global sup
    mostrarSimbolos(sup)
    return t[2]

def p_marc_sup(t):
    'marc_sup : '
    global sup
    sup = Entorno("global")
    entorno.desplazamiento = 0
    entorno.posHeap = 0
    generador.codigoGenerado = ""
    generador.temporal = 0
    generador.etiqueta = 0

def p_instrucciones(t):
    '''instrucciones : instrucciones instruccion
                    | instruccion
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[2])
    return t


def p_instruccion(t):
    '''instruccion : declaracion PYC
                    | asignacion PYC
                    | funcion
                    | impresion PYC
                    | sentencia_if
                    | sentencia_match
                    | bucle_loop
                    | bucle_while
                    | bucle_for
                    | BREAK PYC
                    | CONTINUE PYC
                    | RETURN PYC
                    | RETURN expresion PYC
                    | push_vector PYC
                    | insertar_en_vector PYC
                    | remove_vector PYC
                    | llamada_funcion PYC
    '''
    if t[1] == "break":
        t[0] = Sentencia_Break(t.slice[1],getNoNodo(),t.lexer.lineno,1)
    elif t[1] == "continue":
        t[0] = Sentencia_Continue(t.slice[1],getNoNodo(),t.lexer.lineno,1)
    elif t[1] == "return":
        if len(t) == 3:
            t[0] = Sentencia_Return(t.slice[1],getNoNodo(),None,t.lexer.lineno,1)
        else:
            t[0] = Sentencia_Return(t.slice[1],getNoNodo(),t[2],t.lexer.lineno,1)
    else:
        t[0] = t[1]
    return t

# ======================INSTRUCCION PARA SOLO UNA LINEA MATCH====================================
def p_instrucciones_match(t):
    '''instrucciones_match : instrucciones_match instruccion_match
                    | instruccion_match
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[2])
    return t


def p_instruccion_match(t):
    '''instruccion_match : declaracion
                        | asignacion
                        | impresion
                        | sentencia_if
                        | sentencia_match
                        | bucle_while
                        | bucle_for
                        | BREAK
                        | CONTINUE
                        | RETURN expresion
                        | push_vector
                        | insertar_en_vector
                        | remove_vector
                        | llamada_funcion
    '''
    if t[1] == "break":
        t[0] = Sentencia_Break(t.slice[1], getNoNodo(), t.lexer.lineno, 1)
    elif t[1] == "continue":
        t[0] = Sentencia_Continue(t.slice[1], getNoNodo(), t.lexer.lineno, 1)
    elif t[1] == "return":
        if len(t) == 2:
            t[0] = Sentencia_Return(t.slice[1], getNoNodo(), None, t.lexer.lineno, 1)
        else:
            t[0] = Sentencia_Return(t.slice[1], getNoNodo(), t[2], t.lexer.lineno, 1)
    else:
        t[0] = t[1]
    return t
    return t


# =============================DECLARACION DE VARIABLES============================================
def p_declaracion(t):
    '''declaracion : LET MUT lista_id DOSP tipo IGUAL expresion
                    | LET MUT lista_id IGUAL expresion
                    | LET lista_id DOSP tipo IGUAL expresion
                    | LET lista_id IGUAL expresion
    '''
    global desplazamiento
    global sup
    print("Reconociendo declaracion", t)
    if len(t) == 8:
        tipo = t[5]
    else:
        tipo = t[4]
    if len(t) == 6 and isinstance(t[5],Inicializacion_Vector):
        t[0] = Declaracion_Vector(t.slice[0],getNoNodo(),t[3],t[5],Tipo("VEC"),None,True,None,t.lexer.lineno,1)
    elif len(t) == 5 and isinstance(t[4], Inicializacion_Vector):
        t[0] = Declaracion_Vector(t.slice[0], getNoNodo(), t[2], t[4], Tipo("VEC"), None, False, None,t.lexer.lineno, 1)
    elif len(t) == 7:
        t[0] = Declaracion(t.slice[0],getNoNodo(),tipo,t[6],t[2],False,t.lexer.lineno,1)
    elif len(t) == 5:
        t[0] = Declaracion(t.slice[0],getNoNodo(),None,t[4],t[2],False,t.lexer.lineno,1)
    elif len(t) == 6:
        t[0] = Declaracion(t.slice[0],getNoNodo(),None,t[5],t[3],True,t.lexer.lineno,1)
    elif len(t) == 8:
        t[0] = Declaracion(t.slice[0], getNoNodo(),tipo,t[7],t[3],True,t.lexer.lineno,1)
    return t


def p_asignacion(t):
    '''asignacion : ID IGUAL expresion
                    | ID dimensiones_acceso_arreglo IGUAL expresion
    '''
    if len(t) == 4:
        t[0] = Asignacion(t.slice[0],getNoNodo(),t[1],t[3],t.lexer.lineno,1)
    elif len(t) == 5:
        t[0] = Acceso_Arreglo(t.slice[0],getNoNodo(),t[1],t[2],t.lexer.lineno,1,t[4])
    return t


def p_lista_id(t):
    '''lista_id : ID COMA lista_id
                | ID
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[3])
    return t


def p_tipo(t):
    '''tipo : I64
            | F64
            | BOOL
            | CHAR
            | STRING
            | AMPERSAND STR
            | USIZE
    '''
    if len(t) == 2:
        t[0] = Tipo(t[1].upper())
    else:
        t[0] = Tipo(t[2].upper())
    return t

# ------------------------------ARREGLOS------------------------------------------
def p_declaracion_arreglo(t):
    ''' declaracion : LET MUT lista_id DOSP CORA dimension_arreglo_declaracion CORC IGUAL expresion
                    | LET lista_id DOSP CORA dimension_arreglo_declaracion CORC IGUAL expresion
    '''
    if len(t) == 10:
        t[0] = Declaracion_arreglo(t.slice[0],getNoNodo(),t[3],t[9],Tipo("ARRAY"),t[6][0],t[6],True,t.lexer.lineno,1)
    elif len(t) == 9:
        t[0] = Declaracion_arreglo(t.slice[0],getNoNodo(),t[2],t[8],Tipo("ARRAY"),t[5][0],t[5],False,t.lexer.lineno,1)
    return t


def p_dimension_arreglo_declaracion(t):
    ''' dimension_arreglo_declaracion : dimension_arreglo_declaracion PYC ENTERO
                                    | CORA dimension_arreglo_declaracion PYC ENTERO CORC
                                    | tipo
    '''
    if len(t) == 2:  # t[0][0] = tipo principal del arreglo
        t[0] = []
        t[0].append(t[1])  # t[0][1] = tamaño del sub arreglo
        print(t[0])
    elif len(t) == 4:
        t[0] = t[1]
        t[0].append(t[3])
        print(t[0])
    else:
        t[0] = t[2]
        t[0].append(t[4])
    return t


def p_dimensiones_acceso_arreglo(t):
    '''dimensiones_acceso_arreglo : dimensiones_acceso_arreglo CORA expresion CORC
                            | CORA expresion CORC
    '''
    print("Se reconocio una dimension con valor")
    if len(t) == 4:
        t[0] = []
        t[0].append(t[2])
    else:
        t[0] = t[1]
        t[0].append(t[3])
    return t


# -------------------------------VECTORES-------------------------------------------
def p_declaracion_vector(t):
    ''' declaracion :  LET MUT lista_id DOSP VECN MENORQUE tipo MAYORQUE IGUAL VECN DOSP DOSP NEW PARA PARC
                    | LET lista_id DOSP VECN MENORQUE tipo MAYORQUE IGUAL VECN DOSP DOSP NEW PARA PARC
                    | LET MUT lista_id DOSP VECN MENORQUE tipo MAYORQUE IGUAL VECN DOSP DOSP WITH GUIONBAJO CAPACITY PARA expresion PARC
                    | LET lista_id DOSP VECN MENORQUE tipo MAYORQUE IGUAL VECN DOSP DOSP WITH GUIONBAJO CAPACITY PARA expresion PARC
    '''
    if t[2] == "mut":
        tipo = t[7]
        mut = True
    else:
        tipo = t[6]
        mut = False
    if len(t) == 19:
        t[0] = Declaracion_Vector(t.slice[0],getNoNodo(),t[3], None, Tipo("VEC"), tipo, mut, t[17], t.lexer.lineno, 1)
    elif len(t) == 18:
        t[0] = Declaracion_Vector(t.slice[0],getNoNodo(),t[2], None, Tipo("VEC"), tipo, mut,t[16], t.lexer.lineno, 1)
    elif len(t) == 15:
        t[0] = Declaracion_Vector(t.slice[0],getNoNodo(),t[2], None, Tipo("VEC"), tipo, mut, 0, t.lexer.lineno, 1)
    elif len(t) == 16:
        t[0] = Declaracion_Vector(t.slice[0],getNoNodo(),t[3], None, Tipo("VEC"), tipo, mut, 0, t.lexer.lineno, 1)
    #print(tipo)
    return t

def p_push_en_vector(t):
    ''' push_vector : ID PUNTO PUSH PARA expresion PARC
    '''
    t[0] = Push_Vector(t.slice[0],getNoNodo(),t[1],t[5],t.lexer.lineno,1)
    return t

def p_insertar_en_vector(t):
    ''' insertar_en_vector : ID PUNTO INSERT PARA expresion COMA expresion PARC
    '''
    t[0] = Insert_Vector(t.slice[0],getNoNodo(),t[1],t[5],t[7],t.lexer.lineno,1)
    return t

def p_remove_vector(t):
    ''' remove_vector : ID PUNTO REMOVE PARA expresion PARC
    '''


# -------------------------FUNCIONES NATIVAS--------------------------------------
def p_impresion(t):
    '''impresion : PRINTLN NOT PARA CADENA PARC
                | PRINTLN NOT PARA CADENA COMA lista_expresiones PARC
    '''
    if len(t) == 6:
        cadena = Primitivo(t.slice[1],getNoNodo(),t[4][1:-1],"STR",t.lexer.lineno,1)
        t[0] = Println(t.slice[0],getNoNodo(),cadena,None,t.lexer.lineno,1)
    elif len(t) == 8:
        t[0] = Println(t.slice[0],getNoNodo(),t[4][1:-1],t[6],t.lexer.lineno,1)
    return t


def p_lista_expresion(t):
    '''lista_expresiones : lista_expresiones COMA expresion
                        | expresion
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[3])
    return t


# ------------------------SENTENCIAS DE CONTROL-----------------------------------
# ================================================================================
def p_sentencia_if(t):
    '''sentencia_if : IF expresion LLAVEA instrucciones LLAVEC
                    | IF expresion LLAVEA instrucciones LLAVEC ELSE  sentencia_if
                    | IF expresion LLAVEA instrucciones LLAVEC ELSE LLAVEA instrucciones LLAVEC
    '''
    if len(t) == 6:
        t[0] = Sentencia_If(t.slice[0],getNoNodo(),t[2],t[4],None)
    elif len(t) == 8:
        t[0] = Sentencia_If(t.slice[0],getNoNodo(),t[2],t[4],[t[7]])
    elif len(t) == 10:
        t[0] = Sentencia_If(t.slice[0],getNoNodo(),t[2],t[4],t[8])
    return t



#def p_marc_and(t):
#    'marc_and :'
#    print("WEWEWEWEWE")
#    print(t[0])
#    generador.soltarEtiqueta(t[0])


def p_sentencia_match(t):
    ''' sentencia_match : MATCH expresion LLAVEA lista_casos_match LLAVEC
                        | MATCH expresion LLAVEA lista_casos_match GUIONBAJO IGUAL MAYORQUE instruccion_match COMA LLAVEC
                        | MATCH expresion LLAVEA lista_casos_match GUIONBAJO IGUAL MAYORQUE instrucciones_match  LLAVEC
    '''
    if len(t) == 6:
        t[0] = Sentencia_Match(t.slice[0],getNoNodo(), t[2], t[4], None, t.lexer.lineno, 1)
    elif len(t) == 11:
        t[0] = Sentencia_Match(t.slice[0],getNoNodo(), t[2], t[4], [t[8]], t.lexer.lineno, 1)
    else:
        t[0] = Sentencia_Match(t.slice[0],getNoNodo(), t[2], t[4], t[8], t.lexer.lineno, 1)
    return t

def p_lista_casos_match(t):
    ''' lista_casos_match : lista_casos_match caso_match
                        | caso_match
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[2])
    return t


def p_casos_match(t):
    ''' caso_match : opciones_match IGUAL MAYORQUE LLAVEA instrucciones LLAVEC
                    | opciones_match IGUAL MAYORQUE instruccion_match COMA
    '''
    if len(t) == 7:
        t[0] = Brazo_Match(t.slice[0],getNoNodo(), t[1], t[5], t.lexer.lineno, 1)
    else:
        t[0] = Brazo_Match(t.slice[0],getNoNodo(), t[1], [t[4]], t.lexer.lineno, 1)
    return t

def p_opciones_match(t):
    ''' opciones_match : opciones_match ORMATCH expresion
                        | expresion
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[3])
    return t


# -------------------------------BUCLES-------------------------------------------
# ================================================================================
#CICLO LOOP
def p_loop(t):
    ''' bucle_loop : LOOP LLAVEA instrucciones LLAVEC
    '''
    t[0] = Sentencia_Loop(t.slice[0], getNoNodo(), t[3],t.lexer.lineno,1)
    return t

#CICLO WHILE
def p_while(t):
    ''' bucle_while : WHILE expresion LLAVEA instrucciones LLAVEC
    '''
    t[0] = Sentencia_While(t.slice[0], getNoNodo(),t[2],t[4], t.lexer.lineno, 1)
    return t


#CICLO FOR
def p_for(t):
    ''' bucle_for : FOR recorrido_for LLAVEA instrucciones LLAVEC
    '''
    t[0] = Sentencia_for(t.slice[0],getNoNodo(),t[2],t[4],t.lexer.lineno,1)
    return t

def p_recorrido_for(t):
    ''' recorrido_for : expresion IN expresion
                    | expresion IN expresion DOSPUNTOSCONTINUO expresion
    '''
    if len(t) == 4:
        t[0] = Recorrido_for(t[1],t[3],None,None)
    else:
        t[0] = Recorrido_for(t[1],None,t[3],t[5])
    return t


# ------------------------------FUNCIONES-----------------------------------------
def p_funcion(t):  # ----PENDIENTE------
    ''' funcion : FN ID PARA lista_parametros PARC LLAVEA instrucciones LLAVEC
                | FN ID PARA lista_parametros PARC MENOS MAYORQUE tipo LLAVEA instrucciones LLAVEC
                | FN ID PARA PARC LLAVEA instrucciones LLAVEC
                | FN ID PARA PARC MENOS MAYORQUE tipo LLAVEA instrucciones LLAVEC
    '''
    if len(t) == 9:     #<--- Primera expresion de la regla funcion
        t[0] = Funcion(t.slice[0],getNoNodo(),t[2],None,t[4],t[7],t.lexer.lineno,1)
    elif len(t) == 12:  #<--- Segunda expresion de la regla funcion
        t[0] = Funcion(t.slice[0],getNoNodo(),t[2],t[8],t[4],t[10],t.lexer.lineno,1)
    elif len(t) == 8:   #<--- Tercera expresion de la regla funcion
        t[0] = Funcion(t.slice[0],getNoNodo(),t[2],None,None,t[6],t.lexer.lineno,1)
    else:               #<--- Cuarta expresion de la regla funcion
        t[0] = Funcion(t.slice[0],getNoNodo(),t[2],t[7],None,t[9],t.lexer.lineno,1)
    return t



def p_lista_parametros(t):  # ----PENDIENTE------
    '''lista_parametros : lista_parametros COMA parametro
                        | parametro
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[3])
    return t


def p_parametro(t):  # ----PENDIENTE------
    '''parametro : ID DOSP tipo_parametro
                | ID DOSP AMPERSAND MUT tipo_parametro
                | ID DOSP MUT tipo_parametro
    '''
    if len(t) == 4:
        t[0] = Parametro_funcion(t.slice[0],getNoNodo(),t[1],t[3],False,False,t.lexer.lineno,1)
    elif len(t) == 6:
        t[0] = Parametro_funcion(t.slice[0],getNoNodo(),t[1],t[5],True,True,t.lexer.lineno,1)
    else:
        t[0] = Parametro_funcion(t.slice[0],getNoNodo(),t[1],t[4],True,False,t.lexer.lineno,1)
    return t


def p_tipo_parametro(t):
    ''' tipo_parametro : I64
                        | F64
                        | BOOL
                        | CHAR
                        | STRING
                        | STR
                        | USIZE
                        | VECN MENORQUE tipo_parametro MAYORQUE
                        | CORA tipo_parametro PYC ENTERO CORC
                        | CORA tipo_parametro CORC
    '''
    if len(t) == 2:
        t[0] = Tipo(t[1].upper())
        t[0].tipoElementos = t[0]
    elif len(t) == 5:
        t[0] = Tipo("VEC")
        t[0].dimensiones.append(t[3].dimensiones)
        t[0].tipoElementos = t[3].tipoElementos
    elif len(t) == 6:
        t[0] = Tipo("ARRAY")
        if len(t[2].dimensiones) >0:
            for dimension in t[2].dimensiones:
                t[0].dimensiones.append(dimension)
        t[0].dimensiones.append(t[4])
        t[0].tipoElementos = t[2].tipoElementos
    else:
        t[0] = Tipo("ARRAY")
        t[0].dimensiones.append(1)
        t[0].tipoElementos = t[2].tipoElementos
    return t

#---------------FUNCION COMO INSTRUCCION----------------------------------

def p_llamada_funcion(t):
    ''' llamada_funcion : ID PARA lista_parametros_llamada PARC
                        | ID PARA PARC
    '''
    if len(t) == 4:
        t[0] = Llamada_funcion_ins(t.slice[0],getNoNodo(),t[1],None,t.lexer.lineno,1)
    else:
        t[0] = Llamada_funcion_ins(t.slice[0],getNoNodo(),t[1],t[3],t.lexer.lineno,1)
    return t

# ===================PRDUCCIONES PARA EXPRESIONES==========================
# ==========================================================================
def p_expresion(t):  # ----PENDIENTE------
    '''expresion : PARA expresion AS tipo PARC
    '''
    #arreglar problema de gramatica para PARA expresion PARA con la produccion condicion
    t[0] = t[2]
    return t



def p_expresion_aritmeticas(t):
    '''expresion : I64 DOSP DOSP POW PARA expresion COMA expresion PARC
                | F64 DOSP DOSP POWF PARA expresion COMA expresion PARC
                | expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIV expresion
                | expresion MOD expresion
                | MENOS expresion %prec UMENOS
    '''
    if len(t) == 4:
        t[0] = Aritmetica(t.slice[0],getNoNodo(),t[1],t[3],False, t[2])
    elif len(t) == 3:
        t[0] = Aritmetica(t.slice[0],getNoNodo(),t[2],None,True,t[1])
    return t


def p_condicion_relacional(t):
    ''' expresion : expresion IGUALIGUAL expresion
                | expresion DIFERENTE expresion
                | expresion MENORIGUAL expresion
                | expresion MENORQUE expresion
                | expresion MAYORIGUAL expresion
                | expresion MAYORQUE expresion
    '''
    #t[0] = Condicion(generador.nuevaEtiqueta(),generador.nuevaEtiqueta())
    #cadenaCondicion = str(t[1].ref)+" "+" "+t[2]+" "+str(t[3].ref)
    #t[0].expresion += "if " + cadenaCondicion + " then "+t[0].etiVerdaderas[0]+"\n"
    #t[0].expresion += "goto "+t[0].etiFalsas[0]+"\n"
    #generador.generarCodigo(t[0].expresion)

    t[0] = Condicion_Relacional(t.slice[0],getNoNodo(),t[1],t[3],t[2])
    return t

def p_condicion_logica(t):
    ''' expresion : NOT expresion %prec NOT
                | expresion AND expresion
                | expresion OR expresion
                | PARA expresion PARC
                | TRUE
                | FALSE
    '''
    if t[1] == "(":
        t[0] = t[2]
    elif t[1] == "!":
        t[0] = Condicion_Logica(t.slice[0],getNoNodo(),t[2],None,"!")
    elif len(t)>2:
        t[0] = Condicion_Logica(t.slice[0],getNoNodo(),t[1],t[3],t[2])
    elif len(t) == 2:
        t[0] = Condicion_Logica(t.slice[0],getNoNodo(),t[1],None,None)
    return t



def p_expresion_primitivos(t):
    '''expresion : ENTERO
                | DECIMAL
                | CARACTER
                | CADENA
                | to_string
    '''
    if type(t[1]) == float:
        tipo = "F64"
    elif type(t[1]) == int:
        tipo = "I64"
    elif t[1] == "true" or t[1] == "false":
        tipo = "BOOL"
    elif type(t[1]) == str:
        if t[1].find("'") != -1:
            #print("HOLLLALALAL")
            tipo = "CHAR"
        else:
            tipo = "STR"
    elif isinstance(t[1],To_string):
        tipo = "STRING"
    else:
        tipo = "ERROR"
    valor = t[1]
    if tipo == "CHAR" or tipo == "STR":
        valor = valor[1:-1]
    elif tipo == "STRING":
        valor = t[1].valor.valor
        print(valor)
    t[0] = Primitivo(t.slice[1],getNoNodo(),valor,tipo,t.lexer.lineno,1)
    return t

def p_expresion_to_string(t):
    ''' to_string : expresion PUNTO TO GUIONBAJO STRINGE PARA PARC
    '''
    t[0] = To_string(t[1])
    return t


def p_expresion_id(t):
    ''' expresion : ID
    '''
    t[0] = Identificador(t.slice[0],getNoNodo(),t[1],t.lexer.lineno,1)
    return t


def p_expresion_absoluto(t):
    ''' expresion : expresion PUNTO ABS PARA PARC
    '''

def p_expresion_raiz(t):
    ''' expresion : expresion PUNTO SQRT PARA PARC
    '''

def p_expresion_arreglo(t):
    ''' expresion : CORA lista_expresiones CORC
    '''
    t[0] = t[2]
    return t

def p_acceso_arreglo(t):
    ''' expresion : ID dimensiones_acceso_arreglo
    '''
    t[0] = Acceso_Arreglo(t.slice[0],getNoNodo(),t[1],t[2],t.lexer.lineno,1)
    return t


def p_dimension_vector_declaracion(t):
    ''' expresion : VEC NOT CORA expresion PYC ENTERO CORC
                | VEC NOT CORA lista_expresiones CORC
    '''
    if len(t) == 8:  # t[0][0] = tipo principal del arreglo
        t[0] = Inicializacion_Vector(t[4], t[6])
    else:
        t[0] = Inicializacion_Vector(t[4], 0)
    return t

def p_contains_vector(t):
    ''' expresion : expresion PUNTO CONTAINS PARA AMPERSAND expresion PARC
    '''

def p_len_vector(t):
    ''' expresion : expresion PUNTO LEN PARA PARC
    '''
    t[0] = Len_Arreglo(t.slice[0],getNoNodo(),t[1],t.lexer.lineno,1)

def p_capacity_vector(t):
    ''' expresion : expresion PUNTO CAPACITY PARA PARC
    '''

def p_remove_vector_expresion(t):
    ''' expresion : expresion PUNTO REMOVE PARA expresion PARC
    '''


def p_llamada_funcion_expresion(t):
    ''' expresion : ID PARA lista_parametros_llamada PARC
                | ID PARA PARC
    '''
    if len(t) == 4:
        t[0] = Llamada_funcion_exp(t.slice[0],getNoNodo(),t[1],None,t.lexer.lineno,1)
    else:
        t[0] = Llamada_funcion_exp(t.slice[0],getNoNodo(),t[1],t[3],t.lexer.lineno,1)
    return t

def p_parametros_funcion_llamada(t):
    ''' lista_parametros_llamada : lista_parametros_llamada COMA parametro_llamada
                                | parametro_llamada
    '''
    if len(t) == 2:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = t[1]
        t[0].append(t[3])
    return t

def p_parametro_llamada(t):
    ''' parametro_llamada : AMPERSAND MUT expresion
                          | expresion
    '''
    if len(t) == 2:
        t[0] = Parametro_llamada(t.slice[0],getNoNodo(),t[1],False,False)
    else:
        t[0] = Parametro_llamada(t.slice[0],getNoNodo(),t[3],True,True)

def p_error(t):
    print("Error sintáctico en '%s'" % t.value, "Linea: %d" % t.lexer.lineno)
    return t


import Analizador.ply.yacc as yacc

parser = yacc.yacc()

def getNoNodo():
    global noNode
    noNode = noNode + 1
    return noNode

def analizar_entrada(input):
    # print(input)
    return parser.parse(input)







