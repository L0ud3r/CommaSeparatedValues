def menu():
    print("""Bem-vindo
1 - Print
2 - HTML
3 - Latex
4 - Verificar se um país existe, se sim, mostrar as suas informações""")

    option = int(input(">> "))

    while option > 4 or option < 1:
        print("""Bem-vindo
        1 - Print
        2 - HTML
        3 - Latex
        4 - Verificar se um país existe, se sim, mostrar as suas informações""")

        option = int(input(">> "))

    return option


def get_country():
    string = input("Nome do pais: ")
    return string
