# reader.py
import webbrowser

import ply.lex as lex
from my_utils import slurp, replace_multiple, getKeyFromIndex


class Reader:
    # Tokens
    tokens = ("COUNTRY", "CAPITAL", "CURRENCY", "LANGUAGE", "NEWLINE")

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
        r"[^,]+"
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

    # Função que serve para reconhecer o "parágrafo"/"\n"/nova linha
    def t_NEWLINE(self, t):
        r"\n"
        pass

    # Função que retorna um erro caso o token lido não seja o esperado
    def t_ANY_error(self, t):
        print(f"Unexpected token: {t.value[:20]}")
        exit(1)

    # to fix (decidir se o input do user na consola vira atributo da classe
    def __init__(self, filename):
        self.lexer = None
        self.filename = filename

    @staticmethod
    def builder(filename, **kwargs):
        obje = Reader(filename)
        obje.lexer = lex.lex(module=obje, **kwargs)
        return obje

    def read(self):
        myDict = {}
        self.lexer.input(slurp(self.filename))
        i=0
        for token in iter(self.lexer.token, None):
            if i<4:
                myDict[token.type] = []
                i+=1
            else:
                myDict[token.type].append(token.value)
        return myDict

    # Procedimento para printar o dicionário que é lido pela função read
    # Recebe o dicionário
    def print(self, dict1):
        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()
        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)

        if value not in headers:
            for key in dict1:
                print(key)
                for x in dict1[key]:
                    string_final = replace_multiple(x, {'"': '', "\n": ""})
                    print(string_final)
        else:
            print(value)
            for x in dict1[value]:
                string_final = replace_multiple(x, {'"': '', "\n": ""})
                print(string_final)

    # Procedimento para imprimir num ficheiro HTML o dicionário que é lido pela função read
    # Recebe o dicionário
    def html(self, dict1):
        f = open("file.html", "w")

        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)

        html = '<html><head><link rel="stylesheet" href="styles.css"></head><body><table><tr>'

        if value not in headers:
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            for key in dict1:
                html += f"<th>{key}</th>"

            html+="</tr>"
            valueIndex = 0
            while valueIndex < list_length:
                keyIndex = 0
                html += "</tr><tr>"
                while keyIndex < 4:
                    string_final = dict1[getKeyFromIndex(keyIndex, dict1)][valueIndex]
                    string_final = replace_multiple(string_final, {'"': '', "\n": ""})
                    html += f"<td>{string_final}</td>"
                    keyIndex += 1
                valueIndex += 1

        else:
            html+=f"<th>{value}</th></tr>"
            for x in dict1[value]:
                string_final = replace_multiple(x, {'"': '', "\n": ""})
                html+=f"</tr><tr><td>{string_final}</td>"

        html += "</table></body></html>"
        f.write(html)
        f.close()
        webbrowser.open_new_tab("file.html")

    # Procedimento para escrever num ficheiro .tex (Latex) as colunas lidas do ficheiro de texto
    # Recebe o filename do ficheiro de texto
    def latex(self, dict1):
        f = open("file.tex", "w")

        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)

        latex = '\documentclass{article}\\begin{document}\\begin{center}\\begin{tabular}{||'

        if value not in headers:
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            for element in headers:
                latex += 'c '
            latex += '||} \hline '

            # Printar headers
            headers_length = len(headers)
            i = 0

            for key in dict1:
                if i < headers_length-1:
                    string_final = replace_multiple(key, {'"': '', "&": "\\&"})
                    latex += f"{string_final} & "
                else:
                    string_final = replace_multiple(key, {'"': '', "&": "\\&"})
                    latex += f"{string_final} \\\\ [0.5ex] \hline \hline "
                i+=1

            # Printar linhas

            value_index = 0
            while value_index < list_length:
                keyIndex = 0
                while keyIndex < 4:
                    if keyIndex < 3:
                        string_final = dict1[getKeyFromIndex(keyIndex, dict1)][value_index]
                        string_final = replace_multiple(string_final, {'"': '', "\n": "", "&": "\\&"})
                        latex += f"{string_final} & "
                        keyIndex += 1
                    else:
                        string_final = dict1[getKeyFromIndex(keyIndex, dict1)][value_index]
                        string_final = replace_multiple(string_final, {'"': '', "\n": "", "&": "\\&"})
                        latex += f"{string_final} \\\\ \hline "
                        keyIndex += 1
                value_index += 1

        else:
            latex += 'c ||} \hline '
            latex+= f"{value}\\\\[0.5ex] \hline\hline "
            for x in dict1[value]:
                string_final = replace_multiple(x, {'"': '', "&": "\\&"})
                latex += f"{string_final} \\\\ \hline "


        latex += "\end{tabular}\end{center}\end{document}"
        f.write(latex)
        f.close()
        webbrowser.open_new_tab("file.tex")
