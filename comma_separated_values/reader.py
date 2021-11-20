# test0.1
import webbrowser

import ply.lex as lex
from my_utils import slurp


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
    def t_STR(self, t):
        r"[^,]+"
        t.type = "COUNTRY"
        t.lexer.begin("capital")
        return t

    def t_capital_STR(self, t):
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CAPITAL"
        t.lexer.begin("currency")
        return t

    def t_currency_STR(self, t):
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CURRENCY"
        t.lexer.begin("language")
        return t

    def t_language_STR(self, t):
        r'".+"|(([A-Z]|[a-z])[^\n]+)'
        t.type = "LANGUAGE"
        t.lexer.begin("INITIAL")
        return t

    def t_NEWLINE(self, t):
        r"\n"
        pass

    def t_ANY_error(self, t):
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

    def print(self, filename):
        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()
        lista = ("COUNTRY", "CAPITAL", "CURRENCY", "LANGUAGE")
        self.lexer.input(slurp(filename))

        # PARA DEIXAR A PRINTAR COMO ANTES COPIAR TUDO O QUE ESTA DENTRO DO if value not in list:
        if value not in lista:
            i = 0
            for token in iter(self.lexer.token, None):
                if i < 4:
                    i += 1
                else:
                    # print teste
                    print(f"{token.value}\t", end='')
        else:
            i = 0
            for token in iter(self.lexer.token, None):
                if i < 4:
                    i += 1
                else:
                    if value == token.type:
                        # Remover \n do inicio dos tokens.type COUNTRY
                        if token.type == "COUNTRY":
                            token.value = token.value.replace('\n','')
                        # print teste
                        print(f"{token.value}\n", end='')

    def html(self, filename):
        f = open("file.html", "w")
        self.lexer.input(slurp(filename))
        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()
        lista = ("COUNTRY", "CAPITAL", "CURRENCY", "LANGUAGE")
        html = "<html>\n<head>\t\n" \
               "<body>\n<h1> "

        if value not in lista:
            i = 0
            j = 0
            for token in iter(self.lexer.token, None):
                if i < 4:
                    html += f"{token.value}  "
                    i += 1
                elif i == 4:
                    html += "\n<\h1>\n" \
                            "<h3> "
                    i += 1
                else:
                    if j == 4:
                        html += "\n"
                    html += f"{token.value}  "
                    j += 1
        else:
            i = 0
            for token in iter(self.lexer.token, None):
                if i < 4:
                    i += 1
                else:
                    if value == token.type:
                        # Remover \n do inicio dos tokens.type COUNTRY
                        if token.type == "COUNTRY":
                            token.value = token.value.replace('\n','')
                        # print teste
                        print(f"{token.value}\n", end='')

        html += " <\h3>\n<body>\n<\html>"

        f.write(html)
        f.close()
        webbrowser.open_new_tab("file.html")
