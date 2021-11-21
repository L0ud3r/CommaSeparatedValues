# test0.1
import webbrowser

import ply.lex as lex
from my_utils import slurp


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
    def t_COUNTRY(self, t):
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
        headers = ("COUNTRY", "CAPITAL", "CURRENCY", "LANGUAGE")
        self.lexer.input(slurp(filename))

        # PARA DEIXAR A PRINTAR COMO ANTES COPIAR TUDO O QUE ESTA DENTRO DO if value not in list:
        if value not in headers:
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

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)

        html = '<html><head><link rel="stylesheet" href="styles.css"></head><body><table><tr>'

        if value not in headers:
            i = 0
            j = 0
            for token in iter(self.lexer.token, None):
                if i < len(headers):
                    i += 1
                    tokenFinal = token.value.replace('"', '')
                    html += f"<th>{tokenFinal}</th>"
                    if i == len(headers):
                        html += "</tr>"
                        i += 1
                else:
                    if j == len(headers):
                        html += "</tr><tr>"
                        j = 0
                    tokenFinal = token.value.replace('"', '')
                    html += f"<td>{tokenFinal}</td>"
                    j += 1
        else:
            i = 0
            for token in iter(self.lexer.token, None):
                if value == token.type:
                    if i < 1:
                        html += f"<th>{token.value}</th></tr>"
                        i += 1
                    else:
                        html += f"</tr><tr><td>{token.value}</td>"

        html += "</table></body></html>"
        f.write(html)
        f.close()
        webbrowser.open_new_tab("file.html")

    def latex(self, filename):
        f = open("file.tex", "w")
        self.lexer.input(slurp(filename))
        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)

        latex = '\documentclass{article}\\begin{document}\\begin{center}\\begin{tabular}{||'




        if value not in headers:
            for element in headers:
                latex += 'c '
            latex += '||} \hline '

            i = 0
            j = 0
            for token in iter(self.lexer.token, None):
                if i < len(headers)-1:
                    tokenFinal = token.value.replace('"', '')
                    latex += f"{tokenFinal} & "
                    i += 1
                elif i == len(headers)-1:
                    tokenFinal = token.value.replace('"', '')
                    latex += f"{tokenFinal} \\\\ [0.5ex] \hline \hline"
                    i += 1
                else:
                    if j<len(headers)-1:
                        tokenFinal = token.value.replace('"', '')
                        latex += f"\makecell{{{tokenFinal}}}"
                        j += 1
                    elif j == len(headers)-1:
                        tokenFinal = token.value.replace('"', '')
                        latex += f"\makecell{{{tokenFinal}}} \\\\ \hline"
                        j = 0



        else:
            latex += 'c ||} \hline'
            i = 0
            for token in iter(self.lexer.token, None):
                if value == token.type:
                    if i < 1:
                        latex += f"{token.value}\\\\[0.5ex] \hline\hline"
                        i += 1
                    else:
                        latex += f"{token.value} \\\\ \hline"

        latex += "\end{tabular}\end{center}\end{document}"
        f.write(latex)
        f.close()
        webbrowser.open_new_tab("file.tex")