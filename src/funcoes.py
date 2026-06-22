import pygame

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

def processar_movimento(teclas, jogador, velocidade, largura_tela, altura_tela):
    if teclas[pygame.K_LEFT]:
        jogador["rect"].x -= velocidade
    if teclas[pygame.K_RIGHT]:
        jogador["rect"].x += velocidade
    if teclas[pygame.K_UP]:
        jogador["rect"].y -= velocidade
    if teclas[pygame.K_DOWN]:
        jogador["rect"].y += velocidade

    # Mantém o jogador dentro da tela
    jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, largura_tela - jogador["rect"].width)
    jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, altura_tela - jogador["rect"].height)


def coletar_cristal(jogador, cristal, pontos, largura_tela, altura_tela):
    if verificar_colisao(jogador["rect"], cristal["rect"]):
        pontos = calcular_pontos(pontos, 10)
        
        cristal["rect"].x += 80
        cristal["rect"].y += 50
        
        if cristal["rect"].x > largura_tela - cristal["rect"].width:
            cristal["rect"].x = 50
        if cristal["rect"].y > altura_tela - cristal["rect"].height:
            cristal["rect"].y = 50
            
    return pontos


def interagir_inimigo(jogador, inimigo, vidas, largura_tela, altura_tela):
    if verificar_colisao(jogador["rect"], inimigo["rect"]):
        vidas = tomar_dano(vidas, 1)
        
        inimigo["rect"].x += 80
        inimigo["rect"].y += 50
        
        if inimigo["rect"].x > largura_tela - inimigo["rect"].width:
            inimigo["rect"].x = 50
        if inimigo["rect"].y > altura_tela - inimigo["rect"].height:
            inimigo["rect"].y = 50
            
    return vidas

def desenhar_texto(tela, texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont(None, tamanho)
    imagem_texto = fonte.render(texto, True, cor)

    retangulo = imagem_texto.get_rect()
    retangulo.center = (x, y)

    tela.blit(imagem_texto, retangulo)