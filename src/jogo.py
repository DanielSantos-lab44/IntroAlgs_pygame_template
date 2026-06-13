import pygame

from src.audio import Audio

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    AZUL,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    processar_movimento, 
    coletar_cristal,     
    interagir_inimigo    
)

from src.sprites import pegar_sprite
from src.dados import salvar_recorde, carregar_recorde

def executar_jogo():
    pygame.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    audio = Audio()
    audio.tocar_musica_fundo()    

    player_image = pegar_sprite(CAMINHO_SPRITES, x=110, y=120, width=190, height=190, scale=0.5)
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=900, y=690, width=200, height=200, scale=0.5)
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=905, y=1060, width=200, height=130, scale=0.5)
    
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(100, 100))
    }

    cristal = {
        "imagem": gem_image,
        "rect": gem_image.get_rect(topleft=(500, 300))
    }
    
    inimigo = {
        "imagem": bat_image,
        "rect": bat_image.get_rect(topleft=(200, 500))
    }

    velocidade = 5
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        teclas = pygame.key.get_pressed()

        processar_movimento(teclas, jogador, velocidade, LARGURA_TELA, ALTURA_TELA)

        pontos_antes = pontos
        pontos = coletar_cristal(jogador, cristal, pontos, LARGURA_TELA, ALTURA_TELA)
        if pontos > pontos_antes:
            audio.tocar_cristal()

        vidas_antes = vidas
        vidas = interagir_inimigo(jogador, inimigo, vidas, LARGURA_TELA, ALTURA_TELA)
        if vidas < vidas_antes:
            audio.tocar_dano

        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
        )

        tela.fill(CINZA)
        tela.blit(cristal["imagem"], cristal["rect"]) # Atualizado para cristal
        tela.blit(inimigo["imagem"], inimigo["rect"])
        tela.blit(jogador["imagem"], jogador["rect"])
        
        pygame.display.flip()

    pygame.quit()