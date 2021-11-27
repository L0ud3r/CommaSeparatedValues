# Author: Duarte Melo / Pedro Simões
# Contact: a21149@alunos.ipca.pt / a21140@alunos.ipca.pt
# Program: Comma Separated Values
# Objective: Programa capaz de ler um ficheiro CSV e, dependendo do input do user, reproduzir
# uma tabela csv, html ou mesmo resutados em consola dos dados pedidos

from reader import Reader
from my_utils import printCountryShowStuff



# Construção do objeto Reader
leitura = Reader.builder("list1.csv")

menu = """Bem-vindo
1 - Print
2 - HTML
3 - Latex
OUTROS:
4 - Verificar se um país existe, se sim, mostrar as suas informações"""

print(menu)



#input from menu


myDict = leitura.read()


#ver se um country existe, se existe, printar infos (para usar no Menu!)
printCountryShowStuff("Portugal", myDict)


# Mostrar resultados em consola
leitura.print(myDict)
# Mostrar resultados em uma tabela HTML
leitura.html(myDict)
# Mostrar resultados em uma tabela LaTex
leitura.latex(myDict)
