def salvar_recorde(caminho_arquivo, pontuacao):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))

def carregar_recorde(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0

mapa_inicial = []

for i in range (30):
    linha = []
    for j in range (30):
        linha.append(j)
    mapa_inicial.append(linha)    

mapa_medial = []

for i in range (40):
    linha = []
    for j in range (40):
        linha.append(j)
    mapa_medial.append(linha)    

mapa_final = []

mapa = []

for i in range (60):
    linha = []
    for j in range (50):
        linha.append(j)
    mapa.append(linha)