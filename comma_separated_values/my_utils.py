# my_utils.py

def slurp(filename):
    with open(filename, "rt") as fh:
        contents = fh.read()
    return contents


def replace_multiple(text, dic):
    for i,j in dic.items():
        text = text.replace(i, j)
    return text
