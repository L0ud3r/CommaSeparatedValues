# my_utils.py

# "Utilitários" - funções que são úteis para a execução do nosso código residem neste documento
# são repetidas diversas vezes e, por isso, são definidas aqui e chamadas onde for necessário.


#Função slurp serve para abrir um ficheiro e ler os seus conteúdos
#Retorna os conteúdos lidos
def slurp(filename):
    with open(filename, "rt") as fh:
        contents = fh.read()
    return contents


# Função replace_multiple serve para dar replace a múltiplos caracteres ou sub-strings dentro de uma string
# Text = string onde vai ser feito o tal replace
# Dic = dicionário com os items a substituir {item_a_substituir: substituição, item_a_substituir2: substituição}
# Retorna o texto com os replaces aplicados
def replace_multiple(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


# Obtem a chave de uma dictionary a partir do index
def getKeyFromIndex(index, dict_received):
    i = 0
    for key in dict_received:
        if i == index:
            return key
        i += 1
