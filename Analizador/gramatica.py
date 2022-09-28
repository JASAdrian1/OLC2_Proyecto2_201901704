

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
    '&str': 'STR',
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
    '''inicio : instrucciones
    '''
    t[0] = t[1]
    return t[1]


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
                    | RETURN expresion
                    | RETURN expresion PYC
                    | push_vector PYC
                    | insertar_en_vector PYC
                    | remove_vector PYC
                    | llamada_funcion PYC
    '''

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
                        | push_vector
                        | insertar_en_vector
                        | remove_vector
                        | llamada_funcion
    '''
    t[0] = t[1]
    return t


# =============================DECLARACION DE VARIABLES============================================
def p_declaracion(t):
    '''declaracion : LET MUT lista_id DOSP tipo IGUAL expresion
                    | LET MUT lista_id IGUAL expresion
                    | LET lista_id DOSP tipo IGUAL expresion
                    | LET lista_id IGUAL expresion
    '''
    print("Reconociendo declaracion", t)


def p_asignacion(t):
    '''asignacion : ID IGUAL expresion
                    | ID dimensiones_acceso_arreglo IGUAL expresion
    '''


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
            | STR
            | USIZE
    '''


# ------------------------------ARREGLOS------------------------------------------
def p_declaracion_arreglo(t):
    ''' declaracion : LET MUT lista_id DOSP CORA dimension_arreglo_declaracion CORC IGUAL expresion
                    | LET lista_id DOSP CORA dimension_arreglo_declaracion CORC IGUAL expresion
    '''


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

def p_push_en_vector(t):
    ''' push_vector : ID PUNTO PUSH PARA expresion PARC
    '''

def p_insertar_en_vector(t):
    ''' insertar_en_vector : ID PUNTO INSERT PARA expresion COMA expresion PARC
    '''

def p_remove_vector(t):
    ''' remove_vector : ID PUNTO REMOVE PARA expresion PARC
    '''


# -------------------------FUNCIONES NATIVAS--------------------------------------
def p_impresion(t):
    '''impresion : PRINTLN NOT PARA CADENA PARC
                | PRINTLN NOT PARA CADENA COMA lista_expresiones PARC
    '''


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

def p_sentencia_match(t):
    ''' sentencia_match : MATCH expresion LLAVEA lista_casos_match LLAVEC
                        | MATCH expresion LLAVEA lista_casos_match GUIONBAJO IGUAL MAYORQUE instrucciones_match LLAVEC
                        | MATCH expresion LLAVEA lista_casos_match GUIONBAJO IGUAL MAYORQUE instruccion_match COMA LLAVEC
    '''


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

#CICLO WHILE
def p_while(t):
    ''' bucle_while : WHILE expresion LLAVEA instrucciones LLAVEC
    '''

#CICLO FOR
def p_for(t):
    ''' bucle_for : FOR recorrido_for LLAVEA instrucciones LLAVEC
    '''

def p_recorrido_for(t):
    ''' recorrido_for : expresion IN expresion
                    | expresion IN expresion DOSPUNTOSCONTINUO expresion
    '''


# ------------------------------FUNCIONES-----------------------------------------
def p_funcion(t):  # ----PENDIENTE------
    ''' funcion : FN ID PARA lista_parametros PARC LLAVEA instrucciones LLAVEC
                | FN ID PARA lista_parametros PARC MENOS MAYORQUE tipo LLAVEA instrucciones LLAVEC
                | FN ID PARA PARC LLAVEA instrucciones LLAVEC
                | FN ID PARA PARC MENOS MAYORQUE tipo LLAVEA instrucciones LLAVEC
    '''

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


def p_tipo_parametro(t):
    ''' tipo_parametro : I64
                        | F64
                        | BOOL
                        | CHAR
                        | STRING
                        | STR
                        | USIZE
                        | VECN MENORQUE tipo MAYORQUE
                        | CORA tipo CORC
                        | CORA tipo_parametro PYC ENTERO CORC
    '''


#---------------FUNCION COMO INSTRUCCION----------------------------------

def p_llamada_funcion(t):
    ''' llamada_funcion : ID PARA lista_parametros_llamada PARC
                        | ID PARA PARC
    '''

# ===================PRDUCCIONES PARA EXPRESIONES==========================
# ==========================================================================
def p_expresion(t):  # ----PENDIENTE------
    '''expresion : PARA expresion AS tipo PARC
                | PARA expresion PARC
    '''


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


def p_expresion_logica(t):
    '''expresion : NOT expresion %prec NOT
                | expresion AND expresion
                | expresion OR expresion

    '''


def p_expresion_relacional(t):
    '''expresion : expresion IGUALIGUAL expresion
                | expresion DIFERENTE expresion
                | expresion MENORIGUAL expresion
                | expresion MENORQUE expresion
                | expresion MAYORIGUAL expresion
                | expresion MAYORQUE expresion

    '''


def p_expresion_primitivos(t):
    '''expresion : ENTERO
                | DECIMAL
                | CARACTER
                | CADENA
                | to_string
                | TRUE
                | FALSE
    '''

def p_expresion_to_string(t):
    ''' to_string : expresion PUNTO TO GUIONBAJO STRINGE PARA PARC
    '''


def p_expresion_id(t):
    ''' expresion : ID
    '''


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


def p_dimension_vector_declaracion(t):
    ''' expresion : VEC NOT CORA expresion PYC ENTERO CORC
                | VEC NOT CORA lista_expresiones CORC
    '''

def p_contains_vector(t):
    ''' expresion : expresion PUNTO CONTAINS PARA AMPERSAND expresion PARC
    '''

def p_len_vector(t):
    ''' expresion : expresion PUNTO LEN PARA PARC
    '''

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

def p_error(t):
    print("Error sintáctico en '%s'" % t.value, "Linea: %d" % t.lexer.lineno)
    return t


import Analizador.ply.yacc as yacc

parser = yacc.yacc()


def analizar_entrada(input):
    # print(input)
    return parser.parse(input)







