# Author: Duarte Melo / Pedro Simões
# Contact: a21149@alunos.ipca.pt / a21140@alunos.ipca.pt
# Program: Comma Separated Values
# Objective: Programa capaz de ler um ficheiro CSV e, dependendo do input do user, reproduzir
# uma tabela csv, html ou mesmo resutados em consola dos dados pedidos

from reader import Reader

# Construção do objeto Reader
leitura = Reader.builder()
# Mostrar resultados em consola
leitura.print("list1.csv")
# Mostrar resultados em uma tabela HTML
leitura.html("list1.csv")
# Mostrar resultados em uma tabela LaTex
leitura.latex("list1.csv")
