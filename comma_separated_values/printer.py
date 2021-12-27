# printer.py
import webbrowser
from my_utils import getKeyFromIndex


# Procedimento para printar o dicionário que é lido pela função read
# Recebe o dicionário
def values_print(dict1):
    # Inicializar lista que será usada caso o utilizador use virgulas para selecionar as colunas
    value_list = []

    # Input do utilizador
    value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                  "Caso contrário insira um token:  ").upper()

    # Caso existam virgulas no input, o input é dividido para a lista
    if "," in value:
        value_list = value.split(",")

    headers = [key for key in dict1]

    # Caso a value_list não esteja vazia (printa colunas escolhidas pelo user)
    if value_list:
        key_indexes = []
        list_length = len(dict1[getKeyFromIndex(0, dict1)])
        for value_single in value_list:
            i = 0
            for key in dict1:
                if key == value_single:
                    key_indexes.append(i)
                    print(key, end="\t")
                i += 1

        print()
        key_indexes_size = len(key_indexes)

        value_index = 0

        while value_index < list_length:
            key_index = 0
            while key_index < key_indexes_size:
                string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                print(string_final, end="\t")
                key_index += 1
            print()
            value_index += 1


    # Caso o input do user não exista nos headers (printa todas as colunas)
    elif value not in headers:
        list_length = len(dict1[getKeyFromIndex(0, dict1)])
        for key in dict1:
            print(key, end="\t")
        print()

        value_index = 0
        while value_index < list_length:
            key_index = 0
            while key_index < len(headers):
                string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                print(string_final, end="\t")
                key_index += 1
            print()
            value_index += 1

    # Caso o utilizador tenha inserido apenas o nome de uma coluna (printa apenas uma coluna)
    else:
        print(value)
        for x in dict1[value]:
            print(x)


# Procedimento para imprimir num ficheiro HTML o dicionário que é lido pela função read
# Recebe o dicionário
def values_to_html(dict1):
    f = open("file.html", "w")

    # Inicializar lista que será usada caso o utilizador use virgulas para selecionar as colunas
    value_list = []

    # Input do utilizador
    value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                  "Caso contrário insira um token:  ").upper()

    # Caso existam virgulas no input, o input é dividido para a lista
    if "," in value:
        value_list = value.split(",")

    headers = [key for key in dict1]

    html = '<html><head><link rel="stylesheet" href="styles.css"></head><body><table><tr>'

    # Caso a value_list não esteja vazia (imprime colunas escolhidas pelo user)
    if value_list:
        key_indexes = []
        list_length = len(dict1[getKeyFromIndex(0, dict1)])
        for value_single in value_list:
            i = 0
            for key in dict1:
                if key == value_single:
                    key_indexes.append(i)
                    html += f"<th>{key}</th>"
                i += 1

        html += "</tr>"
        key_indexes_size = len(key_indexes)

        value_index = 0

        while value_index < list_length:
            key_index = 0
            html += "</tr><tr>"
            while key_index < key_indexes_size:
                string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                html += f"<td>{string_final}</td>"
                key_index += 1

            value_index += 1

        html += "</tr>"

    # Caso o input do user não exista nos headers (imprime todas as colunas)
    elif value not in headers:
        list_length = len(dict1[getKeyFromIndex(0, dict1)])
        for key in dict1:
            html += f"<th>{key}</th>"

        html += "</tr>"
        value_index = 0
        while value_index < list_length:
            key_index = 0
            html += "</tr><tr>"
            while key_index < len(headers):
                string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                html += f"<td>{string_final}</td>"
                key_index += 1
            value_index += 1

    # Caso o utilizador tenha inserido apenas o nome de uma coluna (imprime apenas uma coluna)
    else:
        html += f"<th>{value}</th></tr>"
        for x in dict1[value]:

            html += f"</tr><tr><td>{x}</td>"

    html += "</table></body></html>"
    f.write(html)
    f.close()
    webbrowser.open_new_tab("file.html")
    print("Documento HTML gerado com sucesso!")


# Procedimento para escrever num ficheiro .tex (Latex) as colunas lidas do ficheiro de texto
# Recebe o filename do ficheiro de texto
def values_to_latex(dict1):
    f = open("file.tex", "w")

    # Inicializar lista que será usada caso o utilizador use virgulas para selecionar as colunas
    value_list = []

    # Input do utilizador
    value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                  "Caso contrário insira um token:  ").upper()

    # Caso existam virgulas no input, o input é dividido para a lista
    if "," in value:
        value_list = value.split(",")

    headers = [key for key in dict1]

    latex = '\documentclass{article}\\begin{document}\\begin{center}\\begin{tabular}{||'

    # Caso a value_list não esteja vazia (imprime colunas escolhidas pelo user)
    if value_list:

        for value_single in value_list:
            latex += 'c '
        latex += '||} \hline '

        key_indexes = []
        list_length = len(dict1[getKeyFromIndex(0, dict1)])
        i = 0
        for value_single in value_list:
            j = 0
            for key in dict1:

                if (key == value_single) & (i < len(value_list) - 1):
                    key_indexes.append(j)
                    latex += f"{key} & "
                    i += 1
                elif key == value_single:
                    key_indexes.append(j)
                    latex += f"{key} \\\\ [0.5ex] \hline \hline "
                    i += 1
                j += 1

        key_indexes_size = len(key_indexes)

        value_index = 0

        while value_index < list_length:
            key_index = 0
            while key_index < key_indexes_size - 1:
                string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                latex += f"{string_final} & "
                key_index += 1
            if key_index == key_indexes_size - 1:
                string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                latex += f"{string_final} \\\\ \hline "
            value_index += 1

    # Caso o input do user não exista nos headers (imprime todas as colunas)
    elif value not in headers:
        list_length = len(dict1[getKeyFromIndex(0, dict1)])
        for element in headers:
            latex += 'c '
        latex += '||} \hline '

        # Printar headers
        headers_length = len(headers)
        i = 0

        for key in dict1:
            if i < headers_length - 1:
                latex += f"{key} & "
            else:
                latex += f"{key} \\\\ [0.5ex] \hline \hline "
            i += 1

        # Printar linhas
        value_index = 0
        while value_index < list_length:
            key_index = 0
            while key_index < len(headers):
                if key_index < len(headers)-1:
                    string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                    latex += f"{string_final} & "
                    key_index += 1
                else:
                    string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                    latex += f"{string_final} \\\\ \hline "
                    key_index += 1
            value_index += 1

    # Caso o utilizador tenha inserido apenas o nome de uma coluna (imprime apenas uma coluna)
    else:
        latex += 'c ||} \hline '
        latex += f"{value}\\\\[0.5ex] \hline\hline "
        for x in dict1[value]:
            latex += f"{x} \\\\ \hline "

    latex += "\end{tabular}\end{center}\end{document}"
    f.write(latex)
    f.close()
    webbrowser.open_new_tab("file.tex")
    print("Documento LaTex gerado com sucesso!")