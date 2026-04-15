import ply.lex as lex
import ply.yacc as yacc
import sys
import os

# LEXER
# 

reserved = {
    'and':   'AND',
    'or':    'OR',
    'not':   'NOT',
    'xor':   'XOR',
    'true':  'TRUE',
    'false': 'FALSE',
}

tokens = ['LPAREN', 'RPAREN', 'AND', 'OR', 'NOT', 'XOR', 'TRUE', 'FALSE']

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_NOT(t):
    r'!'
    return t

def t_XOR(t):
    r'\^\^'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    lower = t.value.lower()
    if lower in reserved:
        t.type = reserved[lower]
        if lower == 'true':
            t.value = True
        elif lower == 'false':
            t.value = False
        else:
            t.value = lower
    elif t.value in ('1', '0'):
        t.type = 'TRUE' if t.value == '1' else 'FALSE'
        t.value = t.value == '1'
    else:
        print(f"Token desconocido: {t.value!r}")
        t.lexer.skip(len(t.value))
        return None
    return t

def t_NUMBER(t):
    r'[01]'
    t.type = 'TRUE' if t.value == '1' else 'FALSE'
    t.value = t.value == '1'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal: {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex()


precedence = (
    ('left',  'OR'),
    ('left',  'XOR'),
    ('left',  'AND'),
    ('right', 'NOT'),
)

def p_expr_or(p):
    'expr : expr OR expr'
    p[0] = p[1] or p[3]

def p_expr_and(p):
    'expr : expr AND expr'
    p[0] = p[1] and p[3]

def p_expr_xor(p):
    'expr : expr XOR expr'
    p[0] = bool(p[1]) ^ bool(p[3])

def p_expr_not(p):
    'expr : NOT expr'
    p[0] = not p[2]

def p_expr_group(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr_true(p):
    'expr : TRUE'
    p[0] = True

def p_expr_false(p):
    'expr : FALSE'
    p[0] = False

def p_error(p):
    if p:
        print(f"Error de sintaxis en: {p.value!r}")
    else:
        print("Error de sintaxis: fin de entrada inesperado")

parser = yacc.yacc(debug=False, errorlog=yacc.NullLogger())

# para escribir


def repl():
    print("CALCULADORA BOOLEANA ")
    print("  Operadores: AND  OR  NOT  XOR  &&  ||  !  ^^")
    print("  Literales:  true  false  1  0")
    print("  Escribe 'salir' para terminar")
    while True:
        try:
            entrada = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAdios.")
            break
        if entrada.lower() in ('salir', 'exit', 'quit'):
            break
        if not entrada:
            continue
        resultado = parser.parse(entrada, lexer=lexer.clone())
        if resultado is not None:
            print(f"    = {resultado}")


# MAIN


if __name__ == '__main__':

    if len(sys.argv) > 1:
        # Evaluar expresion pasada como argumento
        expr = ' '.join(sys.argv[1:])
        resultado = parser.parse(expr, lexer=lexer.clone())
        print(f"  {expr!r} = {resultado}")
    else:
        repl()
