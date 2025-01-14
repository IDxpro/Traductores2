from ply import lex, yacc

# Definición de tokens
tokens = (
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'SEMICOLON', 'ASSIGN', 'PRINT', 'INT', 'RETURN','LBRACES', 'RBRACES'
)

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACES = r'\{'
t_RBRACES = r'\}'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_PRINT = r'printf'
t_ignore = ' \t'
t_INT = r'int'
t_RETURN =r'return'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value == 'int' or t.value == 'float':
        t.type = t.value.upper()  # Palabras clave
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Reglas de gramática
def p_statement_assign(p):
    'statement : ID ASSIGN expr SEMICOLON'
    p[0] = ('assign', p[1], p[3])

def p_statement_print(p):
    'statement : PRINT LPAREN expr RPAREN SEMICOLON'
    p[0] = ('print', p[3])

def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr'''
    p[0] = (p[2], p[1], p[3])

def p_expr_number(p):
    'expr : NUMBER'
    p[0] = ('number', p[1])

def p_expr_id(p):
    'expr : ID'
    p[0] = ('id', p[1])

def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)

# Construcción del parser
parser = yacc.yacc()

# Prueba del parser
input_code ="""
int main() {
    int a = 10;
    int b = 20;
    int c = a - b;
    return 0;
}
"""
lexer.input(input_code)
for tok in lexer:
    print(tok)

result = parser.parse(input_code)
print(result)