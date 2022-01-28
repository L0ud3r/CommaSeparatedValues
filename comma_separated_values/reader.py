# reader.py

import ply.lex as lex
from my_utils import slurp, replace_multiple, getKeyFromIndex

# Classe com as funcionalidades necessárias para
class Reader:
    # Tokens
    tokens = ("COMMENTARY", "COLUMN", "COLUMNBEFORENL", "NEWLINE")

    # Ignore rule
    t_ANY_ignore = r","

# Funcoes de definicao de campo lexical

    # Função que serve para reconhecer o campo Country do ficheiro de texto
    def t_COMMENTARY(self, t):
        r"\#[^\n]+\n"
        pass

    # Função de reconhecimento de texto da coluna antes do newline
    def t_COLUMNBEFORENL(self, t):
        r'[^\n,"]+\n|"[^\n"]+"\n'
        t.type = "COLUMNBEFORENL"
        return t

    # Função de leitura de cada coluna exceto a ultima de cada linha
    def t_COLUMN(self, t):
        r'[^,\n"]+,|"[^"\n]+"'
        t.type = "COLUMN"
        return t

    # Função de reconhecimento de uma newline
    def t_NEWLINE(self, t):
        r"\n"
        pass

    # Função de controlo de erros (texto não esperado)
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

        #separate headers from non headers, save on memory
        i = 0
        j = 0
        for token in iter(self.lexer.token, None):
            #remove stuff
            if token.value[0] == '"':
                token.value = replace_multiple(token.value, {'"': '', "\n": ""})
            else:
                token.value = replace_multiple(token.value, {'"': '', "\n": "", ",": ''})
            token.value = token.value.replace("\n", "")
            if i == 0:
                my_dict[token.value] = []
                if token.type == "COLUMNBEFORENL":
                    i += 1
            else:
                my_dict[getKeyFromIndex(j, my_dict)].append(token.value)
                if token.type == "COLUMNBEFORENL":
                    j = 0
                else:
                    j += 1

        return my_dict
