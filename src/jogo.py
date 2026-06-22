import pygame

from src.audio import Audio
from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    AZUL,
    CINZA,
    PRETO,
    BRANCO,
    VERMELHO,
    AMARELO,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
    CAMINHO_CHAO,
    TAMANHO_BLOCO
)
from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    processar_movimento,
    coletar_cristal,
    interagir_inimigo,
    resolver_colisao_parede,
    desenhar_texto,
    verificar_acessibilidade  # Importado para validar o spawn da gema
)
from src.sprites import (
    nivel_iniciante,
    nivel_intermediario,
    nivel_final,
    pegar_sprite
)
from src.dados import (
    salvar_recorde,
    carregar_recorde
)

SCALE_JOGADOR = 0.1   
SCALE_INIMIGO = 0.08   # Reduzido de 0.060 para 0.045 para evitar colisões fantasmas nas quinas
SCALE_CRISTAL = 0.1   

VELOCIDADE_JOGADOR = 2   
VELOCIDADE_INIMIGO_POR_FASE = {1: 1, 2: 2, 3: 3}   
DELAY_INIMIGO_POR_FASE = {1: 4, 2: 3, 3: 2}      


def _celula_livre_longe(nivel, jogador_rect, tamanho_bloco, distancia_min=15):
    import random
    linhas = len(nivel)
    colunas = len(nivel[0])
    jl = jogador_rect.centery // tamanho_bloco
    jc = jogador_rect.centerx // tamanho_bloco
    for _ in range(500):
        ni = random.randint(1, linhas - 2)
        nj = random.randint(1, colunas - 2)
        if nivel[ni][nj] == 0 and verificar_acessibilidade(nivel, ni, nj) and abs(ni - jl) + abs(nj - jc) >= distancia_min:
            return (nj * tamanho_bloco, ni * tamanho_bloco)
    return (tamanho_bloco * 2, tamanho_bloco * 2)  


def desenhar_nivel(tela, nivel, portal_ativo, tamanho_bloco, offset_x, offset_y):
    for linha, blocos in enumerate(nivel):
        for coluna, bloco in enumerate(blocos):
            x = offset_x + coluna * tamanho_bloco
            y = offset_y + linha * tamanho_bloco

            if bloco == 1:
                pygame.draw.rect(tela, (50, 50, 50),
                                 (x, y, tamanho_bloco, tamanho_bloco))
            elif bloco == 3 and portal_ativo:
                pygame.draw.rect(tela, (138, 43, 226),
                                 (x, y, tamanho_bloco * 3, tamanho_bloco * 3))


def executar_jogo():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    chao = pygame.image.load(CAMINHO_CHAO).convert()
    chao = pygame.transform.scale(chao, (LARGURA_TELA, ALTURA_TELA))

    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    audio = Audio()
    audio.tocar_musica_fundo()

    player_image = pegar_sprite(CAMINHO_SPRITES, x=110, y=120,
                                width=190, height=190, scale=SCALE_JOGADOR)
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=900, y=690,
                                width=200, height=200, scale=SCALE_CRISTAL)
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=905, y=1060,
                                width=200, height=130, scale=SCALE_INIMIGO)

    nivel_largura_px = 42 * TAMANHO_BLOCO   
    nivel_altura_px  = 40 * TAMANHO_BLOCO   
    offset_x = (LARGURA_TELA - nivel_largura_px) // 2   
    offset_y = (ALTURA_TELA  - nivel_altura_px)  // 2   

    def nova_pos(col_bloco, lin_bloco):
        return (offset_x + col_bloco * TAMANHO_BLOCO,
                offset_y + lin_bloco * TAMANHO_BLOCO)

    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=nova_pos(2, 2))
    }
    cristal = {
        "imagem": gem_image,
        "rect": gem_image.get_rect(topleft=nova_pos(20, 20))
    }
    inimigo = {
        "imagem": bat_image,
        "rect": bat_image.get_rect(topleft=nova_pos(30, 30))
    }

    pontos      = 0
    vidas       = 3
    recorde     = carregar_recorde(CAMINHO_RECORDE)
    fase_atual  = 1
    portal_ativo = False
    estado      = "MENU"

    contador_inimigo = 0
    invencivel_timer = 0
    INVENCIVEL_FRAMES = 60

    def reiniciar():
        nonlocal pontos, vidas, fase_atual, portal_ativo, estado
        nonlocal contador_inimigo, invencivel_timer
        pontos = 0
        vidas  = 3
        fase_atual = 1
        portal_ativo = False
        contador_inimigo = 0
        invencivel_timer = 0
        estado = "JOGANDO"
        jogador["rect"].topleft = nova_pos(2, 2)
        cristal["rect"].topleft = nova_pos(20, 20)
        inimigo["rect"].topleft = nova_pos(30, 30)

    def avancar_fase():
        nonlocal fase_atual, portal_ativo, contador_inimigo
        fase_atual  += 1
        portal_ativo = False
        contador_inimigo = 0
        jogador["rect"].topleft = nova_pos(2, 2)
        px, py = _celula_livre_longe(nivel_atual, jogador["rect"], TAMANHO_BLOCO)
        inimigo["rect"].topleft = (offset_x + px, offset_y + py)

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                if estado == "MENU" and evento.key == pygame.K_SPACE:
                    estado = "JOGANDO"
                elif estado in ("GAMEOVER", "VITORIA") and evento.key == pygame.K_r:
                    reiniciar()

        if fase_atual == 1:
            nivel_atual = nivel_iniciante
        elif fase_atual == 2:
            nivel_atual = nivel_intermediario
        else:
            nivel_atual = nivel_final

        if estado == "MENU":
            tela.fill(PRETO)
            desenhar_texto(tela, "LABIRINTO DO TEMPO", 60, BRANCO,
                           LARGURA_TELA // 2, ALTURA_TELA // 2 - 50)
            desenhar_texto(tela, "Pressione ESPAÇO para Iniciar", 30, AMARELO,
                           LARGURA_TELA // 2, ALTURA_TELA // 2 + 50)

        elif estado == "JOGANDO":
            teclas = pygame.key.get_pressed()

            processar_movimento(teclas, jogador, VELOCIDADE_JOGADOR,
                                nivel_atual, TAMANHO_BLOCO, offset_x, offset_y)

            delay = DELAY_INIMIGO_POR_FASE.get(fase_atual, 3)
            contador_inimigo += 1
            if contador_inimigo >= delay:
                contador_inimigo = 0
                jog_local = jogador["rect"].move(-offset_x, -offset_y)
                ini_local = inimigo["rect"].move(-offset_x, -offset_y)

                from src.funcoes import bfs_proximo_passo
                dx, dy = bfs_proximo_passo(nivel_atual, ini_local, jog_local,
                                           TAMANHO_BLOCO)
                vel = VELOCIDADE_INIMIGO_POR_FASE.get(fase_atual, 1)
                
                # ── Mecanismo Anti-Stuck (Alinhamento de Quinas) ─────────────────
                # Se movendo na horizontal, puxa sutilmente o Y para o centro do trilho
                if dx != 0:
                    centro_y = (ini_local.centery // TAMANHO_BLOCO) * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
                    if ini_local.centery < centro_y:
                        inimigo["rect"].y += 1
                    elif ini_local.centery > centro_y:
                        inimigo["rect"].y -= 1
                        
                # Se movendo na vertical, puxa sutilmente o X para o centro do trilho
                if dy != 0:
                    centro_x = (ini_local.centerx // TAMANHO_BLOCO) * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
                    if ini_local.centerx < centro_x:
                        inimigo["rect"].x += 1
                    elif ini_local.centerx > centro_x:
                        inimigo["rect"].x -= 1

                inimigo["rect"].x += dx * vel
                inimigo["rect"].y += dy * vel

                ini_local2 = inimigo["rect"].move(-offset_x, -offset_y)
                resolver_colisao_parede(ini_local2, nivel_atual, TAMANHO_BLOCO)
                inimigo["rect"].topleft = (ini_local2.x + offset_x,
                                           ini_local2.y + offset_y)

            if verificar_colisao(jogador["rect"], cristal["rect"]):
                pontos = calcular_pontos(pontos, 10)
                portal_ativo = True
                audio.tocar_cristal()
                import random
                linhas_n = len(nivel_atual)
                colunas_n = len(nivel_atual[0])
                for _ in range(500):
                    ni = random.randint(1, linhas_n - 2)
                    nj = random.randint(1, colunas_n - 2)
                    # Adicionada verificação de acessibilidade antes de posicionar a gema
                    if nivel_atual[ni][nj] == 0 and verificar_acessibilidade(nivel_atual, ni, nj):
                        cristal["rect"].topleft = (offset_x + nj * TAMANHO_BLOCO,
                                                   offset_y + ni * TAMANHO_BLOCO)
                        break

            if invencivel_timer > 0:
                invencivel_timer -= 1
            elif verificar_colisao(jogador["rect"], inimigo["rect"]):
                vidas -= 1
                invencivel_timer = INVENCIVEL_FRAMES
                audio.tocar_dano()
                ini_local_tmp = jogador["rect"].move(-offset_x, -offset_y)
                px, py = _celula_livre_longe(nivel_atual, ini_local_tmp,
                                             TAMANHO_BLOCO)
                inimigo["rect"].topleft = (offset_x + px, offset_y + py)

            if jogador_perdeu(vidas):
                estado = "GAMEOVER"

            if portal_ativo:
                for static_l, blocos in enumerate(nivel_atual):
                    for static_c, bloco in enumerate(blocos):
                        if bloco == 3:
                            px_portal = offset_x + static_c * TAMANHO_BLOCO
                            py_portal = offset_y + static_l  * TAMANHO_BLOCO
                            portal_rect = pygame.Rect(px_portal, py_portal,
                                                      TAMANHO_BLOCO * 3,
                                                      TAMANHO_BLOCO * 3)
                            if verificar_colisao(jogador["rect"], portal_rect):
                                audio.tocar_portal()
                                if fase_atual >= 3:
                                    estado = "VITORIA"
                                else:
                                    avancar_fase()

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            pygame.display.set_caption(
                f"{TITULO_JOGO} | Pts: {pontos} | Rec: {recorde} | Vidas: {vidas}"
            )

            tela.blit(chao, (0, 0))
            desenhar_nivel(tela, nivel_atual, portal_ativo,
                           TAMANHO_BLOCO, offset_x, offset_y)

            tela.blit(cristal["imagem"], cristal["rect"])
            tela.blit(inimigo["imagem"],  inimigo["rect"])

            if invencivel_timer == 0 or (invencivel_timer // 5) % 2 == 0:
                tela.blit(jogador["imagem"], jogador["rect"])

            desenhar_texto(tela,
                           f"Pontos: {pontos}  |  Vidas: {vidas}  |  Fase: {fase_atual}",
                           24, PRETO, LARGURA_TELA // 2, 12)

        elif estado == "GAMEOVER":
            tela.fill(PRETO)
            desenhar_texto(tela, "FIM DE JOGO", 70, VERMELHO,
                           LARGURA_TELA // 2, ALTURA_TELA // 2 - 60)
            desenhar_texto(tela, f"Sua pontuação: {pontos}", 40, BRANCO,
                           LARGURA_TELA // 2, ALTURA_TELA // 2)
            desenhar_texto(tela,
                           "Pressione 'R' para recomeçar ou 'ESC' para sair",
                           25, AMARELO, LARGURA_TELA // 2, ALTURA_TELA // 2 + 80)

        elif estado == "VITORIA":
            tela.fill(PRETO)
            desenhar_texto(tela, "VOCÊ ESCAPOU!", 70, AMARELO,
                           LARGURA_TELA // 2, ALTURA_TELA // 2 - 60)
            desenhar_texto(tela, f"Pontuação Final: {pontos}", 40, BRANCO,
                           LARGURA_TELA // 2, ALTURA_TELA // 2)
            desenhar_texto(tela, "Pressione 'R' para jogar novamente", 25, BRANCO,
                           LARGURA_TELA // 2, ALTURA_TELA // 2 + 80)

        pygame.display.flip()

    pygame.quit()