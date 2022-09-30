import enum


class tipo(enum.Enum):
    I64 = 0
    F64 = 1
    BOOL = 2
    CHAR = 3
    STRING = 4
    STR = 5
    USIZE = 6
    ARRAY = 7
    VEC = 8
    ERROR = 9


class Tipo:
    def __init__(self, tip):    #(self, tip: string)
        self.tipo_enum = tipo[tip]
        self.tipo = tip



global validar_tipo

validar_tipo = {
    '+': {
        tipo.I64:{
            tipo.I64: tipo.I64,
            tipo.USIZE: tipo.I64
        },
        tipo.F64:{
            tipo.F64: tipo.F64
        },
        tipo.USIZE:{
            tipo.USIZE: tipo.I64,
            tipo.I64: tipo.I64
        },
        tipo.STR:{
            tipo.STR: tipo.STR,
            tipo.STRING: tipo.STRING
        },
        tipo.STRING:{
            tipo.STRING: tipo.STRING,
            tipo.STR: tipo.STR
        }

    },
    '-':{
        tipo.F64:{
            tipo.F64: tipo.F64
        },
        tipo.I64:{
            tipo.I64: tipo.I64,
            tipo.USIZE: tipo.I64
        },
        tipo.USIZE:{
            tipo.USIZE: tipo.USIZE,
            tipo.I64: tipo.I64
        }
    },
    '*':{
        tipo.F64:{
            tipo.F64: tipo.F64
        },
        tipo.I64:{
            tipo.I64: tipo.I64
        }
    },
    '/':{
        tipo.F64:{
            tipo.F64: tipo.F64
        },
        tipo.I64:{
            tipo.I64: tipo.I64
        }
    },
    '^':{
        tipo.I64:{
            tipo.I64: tipo.I64
        }
    },
    '^^':{
        tipo.F64:{
            tipo.F64:tipo.F64
        }
    },
    '%':{
        tipo.F64:{
            tipo.F64: tipo.F64
        },
        tipo.I64:{
            tipo.I64: tipo.I64
        }
    }
}
