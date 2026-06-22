import pygame
from collections import deque

def limitar_valor(valor, minimo, maximo):
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor

def verificar_colisao(retangulo_1, retangulo_2):
    return retangulo_1.colliderect(retangulo_2)

def calcular_pontos(pontos_atual, pontos_ganhos):
    return pontos_atual + pontos_ganhos

def tomar_dano(vida_atual, dano):
    return vida_atual - dano

def jogador_perdeu(vidas):
    return vidas <= 0

def _construir_grafo_paredes(nivel, tamanho_bloco):
    paredes = set()
    for i, linha in enumerate(nivel):
        for j, bloco in enumerate(linha):
            if bloco == 1:
                paredes.add((i, j))
    return paredes

def _rect_para_celula(rect, tamanho_bloco):
    cx = rect.centerx // tamanho_bloco
    cy = rect.centery // tamanho_bloco
    return (cy, cx)

def _celula_para_pixel(linha, coluna, tamanho_bloco):
    return (coluna * tamanho_bloco, linha * tamanho_bloco)

def verificar_acessibilidade(nivel, linha_dest, coluna_dest):
    """Garante através de um Flood Fill se o destino é alcançável a partir do início (2,2)"""
    origem = (2, 2)
    if origem == (linha_dest, coluna_dest):
        return True
    
    linhas = len(nivel)
    colunas = len(nivel[0])
    fila = deque([origem])
    visitados = {origem}
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while fila:
        atual = fila.popleft()
        if atual == (linha_dest, coluna_dest):
            return True
        for dl, dc in direcoes:
            vizinho = (atual[0] + dl, atual[1] + dc)
            if 0 <= vizinho[0] < linhas and 0 <= vizinho[1] < colunas:
                if vizinho not in visitados and nivel[vizinho[0]][vizinho[1]] != 1:
                    visitados.add(vizinho)
                    fila.append(vizinho)
    return False

def bfs_proximo_passo(nivel, origem_rect, destino_rect, tamanho_bloco):
    linhas = len(nivel)
    colunas = len(nivel[0]) if linhas > 0 else 0

    paredes = _construir_grafo_paredes(nivel, tamanho_bloco)

    origem = _rect_para_celula(origem_rect, tamanho_bloco)
    destino = _rect_para_celula(destino_rect, tamanho_bloco)

    if origem == destino:
        return (0, 0)

    fila = deque()
    fila.append((origem, [origem]))
    visitados = {origem}

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while fila:
        atual, caminho = fila.popleft()

        for dl, dc in direcoes:
            vizinho = (atual[0] + dl, atual[1] + dc)
            if vizinho[0] < 0 or vizinho[0] >= linhas:
                continue
            if vizinho[1] < 0 or vizinho[1] >= colunas:
                continue
            if vizinho in visitados:
                continue
            if vizinho in paredes:
                continue

            novo_caminho = caminho + [vizinho]

            if vizinho == destino:
                proximo = novo_caminho[1]
                dl_final = proximo[0] - origem[0]
                dc_final = proximo[1] - origem[1]
                return (dc_final, dl_final)

            visitados.add(vizinho)
            fila.append((vizinho, novo_caminho))

    return (0, 0)

def resolver_colisao_parede(rect, nivel, tamanho_bloco):
    linhas = len(nivel)
    colunas = len(nivel[0]) if linhas > 0 else 0

    esq = rect.left // tamanho_bloco
    dir_ = (rect.right - 1) // tamanho_bloco
    top = rect.top // tamanho_bloco
    bot = (rect.bottom - 1) // tamanho_bloco

    for i in range(max(0, top), min(linhas, bot + 1)):
        for j in range(max(0, esq), min(colunas, dir_ + 1)):
            if nivel[i][j] == 1:
                parede = pygame.Rect(
                    j * tamanho_bloco, i * tamanho_bloco,
                    tamanho_bloco, tamanho_bloco
                )
                if rect.colliderect(parede):
                    over_left  = parede.right - rect.left
                    over_right = rect.right - parede.left
                    over_top   = parede.bottom - rect.top
                    over_bot   = rect.bottom - parede.top

                    min_over = min(over_left, over_right, over_top, over_bot)
                    if min_over == over_left:
                        rect.left = parede.right
                    elif min_over == over_right:
                        rect.right = parede.left
                    elif min_over == over_top:
                        rect.top = parede.bottom
                    else:
                        rect.bottom = parede.top

def processar_movimento(teclas, jogador, velocidade, nivel, tamanho_bloco, offset_x, offset_y):
    if teclas[pygame.K_LEFT]:
        jogador["rect"].x -= velocidade
    if teclas[pygame.K_RIGHT]:
        jogador["rect"].x += velocidade
    if teclas[pygame.K_UP]:
        jogador["rect"].y -= velocidade
    if teclas[pygame.K_DOWN]:
        jogador["rect"].y += velocidade

    jog_local = jogador["rect"].move(-offset_x, -offset_y)

    linhas = len(nivel)
    colunas = len(nivel[0]) if linhas > 0 else 0
    largura_mapa = colunas * tamanho_bloco
    altura_mapa = linhas * tamanho_bloco

    jog_local.x = limitar_valor(jog_local.x, 0, largura_mapa - jog_local.width)
    jog_local.y = limitar_valor(jog_local.y, 0, altura_mapa - jog_local.height)

    resolver_colisao_parede(jog_local, nivel, tamanho_bloco)
    jogador["rect"].topleft = (jog_local.x + offset_x, jog_local.y + offset_y)

def coletar_cristal(jogador, cristal, pontos, largura_tela, altura_tela, nivel, tamanho_bloco):
    if verificar_colisao(jogador["rect"], cristal["rect"]):
        pontos = calcular_pontos(pontos, 10)
        import random
        linhas = len(nivel)
        colunas = len(nivel[0])
        tentativas = 0
        while tentativas < 500:
            ni = random.randint(1, linhas - 2)
            nj = random.randint(1, colunas - 2)
            if nivel[ni][nj] == 0 and verificar_acessibilidade(nivel, ni, nj):
                cristal["rect"].topleft = (nj * tamanho_bloco, ni * tamanho_bloco)
                break
            tentativas += 1
    return pontos

def interagir_inimigo(jogador, inimigo, vidas, largura_tela, altura_tela, nivel, tamanho_bloco):
    if verificar_colisao(jogador["rect"], inimigo["rect"]):
        vidas = tomar_dano(vidas, 1)
        import random
        linhas = len(nivel)
        colunas = len(nivel[0])
        tentativas = 0
        while tentativas < 500:
            ni = random.randint(1, linhas - 2)
            nj = random.randint(1, colunas - 2)
            dist = abs(ni - jogador["rect"].centery // tamanho_bloco) + \
                   abs(nj - jogador["rect"].centerx // tamanho_bloco)
            if nivel[ni][nj] == 0 and dist > 10 and verificar_acessibilidade(nivel, ni, nj):
                inimigo["rect"].topleft = (nj * tamanho_bloco, ni * tamanho_bloco)
                break
            tentativas += 1
    return vidas

def desenhar_texto(tela, texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont(None, tamanho)
    imagem_texto = fonte.render(texto, True, cor)
    retangulo = imagem_texto.get_rect()
    retangulo.center = (x, y)
    tela.blit(imagem_texto, retangulo)