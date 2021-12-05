# reader.py

import ply.lex as lex
from my_utils import slurp, replace_multiple, getKeyFromIndex


class Reader:
    # Tokens
    tokens = ("COUNTRY", "CAPITAL", "CURRENCY", "LANGUAGE", "COMMENTARY", "NEWLINE")

    # States
    states = (
        ("capital", "exclusive"),
        ("currency", "exclusive"),
        ("language", "exclusive"),
    )

    # Ignore rule
    t_ANY_ignore = r","

    # Funcoes de definicao de campo lexical


    # Função que serve para reconhecer o campo Country do ficheiro de texto
    def t_COUNTRY(self, t):
        r"([A-Z]|[a-z])[^,]+"
        t.type = "COUNTRY"
        t.lexer.begin("capital")
        return t

    # Função que serve para reconhecer o campo Capital do ficheiro de texto
    def t_capital_STR(self, t):
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CAPITAL"
        t.lexer.begin("currency")
        return t

    # Função que serve para reconhecer o campo Currency do ficheiro de texto
    def t_currency_STR(self, t):
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CURRENCY"
        t.lexer.begin("language")
        return t

    # Função que serve para reconhecer o campo Language do ficheiro de texto
    def t_language_STR(self, t):
        r'".+"|(([A-Z]|[a-z])[^\n]+)'
        t.type = "LANGUAGE"
        t.lexer.begin("INITIAL")
        return t

    # Função para reconhecer comentários
    def t_COMMENTARY(self, t):
        r"\#[^\n]+"
        pass

    # Função que serve para reconhecer o "parágrafo"/"\n"/nova linha
    def t_NEWLINE(self, t):
        r"\n"
        pass

    # Função que retorna um erro caso o token lido não seja o esperado
    def t_ANY_error(self, t):
        print(f"Unexpected token: {t.value[:20]}")
        exit(1)

    # Inicializador do objeto
    def __init__(self, filename):
        self.lexer = None
        self.filename = filename

    # Construtor
    @staticmethod
    def builder(filename, **kwargs):
        obje = Reader(filename)
        obje.lexer = lex.lex(module=obje, **kwargs)
        return obje

    # Função de leitura do doc csv, armazenando o conteudo numa dictionary
    def read(self):
        my_dict = {}
        self.lexer.input(slurp(self.filename))

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)
            if element == "COMMENTARY":
                headers.remove(element)

        i=0
        for token in iter(self.lexer.token, None):
            if i< len(headers):
                my_dict[token.type] = []
                i+=1
            else:
                my_dict[token.type].append(token.value)
        return my_dict