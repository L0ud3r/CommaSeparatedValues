# test0.1
import ply.lex as lex
from my_utils import slurp
from pprint import PrettyPrinter


class Reader:
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
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CAPITAL"
        t.lexer.begin("currency")
        return t

    def t_currency_STR(t):
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CURRENCY"
        t.lexer.begin("language")
        return t

    def t_language_STR(t):
        r'".+"|(([A-Z]|[a-z])[^\n]+)'
        t.type = "LANGUAGE"
        t.lexer.begin("INITIAL")
        return t

    def t_NEWLINE(t):
        r"\n"
        pass

    def t_ANY_error(t):
        print(f"Unexpected token: {t.value[:20]}")
        exit(1)

    # to fix (decidir se o input do user na consola vira atributo da classe
    # Caso input == None, fazer output tabela toda)
    def __init__(self):
        self.lexer = None

    @staticmethod
    def builder(**kwargs):
        obje = Reader()
        obje.lexer = lex.lex(module=obje, **kwargs)
        return obje

    def parse(self, filename):
        self.lexer.input(slurp(filename))
        i = 0
        for token in iter(self.lexer.token, None):
            if i < 4:
                i += 1
            else:
                # print teste
                print(f"{token.value} <- {token.type}\t", end='')


reader = Reader.builder()
reader.parse("list1.csv")
# ----------------------------
# Montar o lexer com as tokens em cima
# lexer = lex.lex()
# Ler o documento data
# lexer.input(slurp("list1.csv"))
# i = 0

# printagem em console do lexer
# for token in iter(lexer.token, None):
#    if i < 4:
#        i += 1
#    else:
#        # print teste
#        print(f"{token.value} <- {token.type}\t", end = '')

        # print por Type
        # if token.type == "COUNTRY":
            # print(f"{token.value}", end='')

        # print ALL
        # print(f"{token.value}\t", end='')







    # TESTE
    # "[[[A-Z|a-z]+,|[[A-Z|a-z]+
    # "[.+]"|[^,]+
    # "[A-Z]+[a-z]+,?"|[^,]+