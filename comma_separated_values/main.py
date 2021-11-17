# test0.1
import ply.lex as lex
from my_utils import slurp
from pprint import PrettyPrinter

# Tokens
tokens = ("STR", "COUNTRY", "CAPITAL", "CURRENCY", "LANGUAGE", "NEWLINE")

# States
states = (
    ("capital", "exclusive"),
    ("currency", "exclusive"),
    ("language", "exclusive"),
)

# Ignore rule
t_ANY_ignore = r","

# Funcoes de definicao de campo lexical
def t_STR(t):
    r"[^,]+"
    t.type = "COUNTRY"
    t.lexer.begin("capital")
    return t

def t_capital_STR(t):
    r'"([A-Z][a-z]*,?\s?)*"|([A-Z]?[a-z]+-?\s?\'?)+'
    t.type = "CAPITAL"
    t.lexer.begin("currency")
    return t

def t_currency_STR(t):
    r"[^,]+"
    t.type = "CURRENCY"
    t.lexer.begin("language")
    return t

def t_language_STR(t):
    r'".+"|[A-Z][a-z]+' #fix no primary language (header) -> ([A-Z][a-z]*\s?)+  (not working, entra \n ns pq)
    t.type = "LANGUAGE"
    t.lexer.begin("INITIAL")
    return t

def t_NEWLINE(t):
    r"\n"
    pass

def t_ANY_error(t):
    print(f"Unexpected token: {t.value[:20]}")
    exit(1)

# Montar o lexer com as tokens em cima
lexer = lex.lex()
# Ler o documento data
lexer.input(slurp("data"))

# printagem em console do lexer
i = 0
for token in iter(lexer.token, None):
    if i < 4:
        i += 1
    else:
        # print teste
        print(f"{token.value} <- {token.type}\t", end = '')
        # print(f"{token.value}\t", end='')






# TESTE
# "[[[A-Z|a-z]+,|[[A-Z|a-z]+
# "[.+]"|[^,]+
# "[A-Z]+[a-z]+,?"|[^,]+