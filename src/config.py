import os

LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
TAMANHO_BLOCO = 10
TITULO_JOGO = "Projeto Final - Pygame"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CAMINHO_RECORDE = os.path.join(BASE_DIR, "data", "recorde.txt")

CAMINHO_SPRITES = os.path.join(BASE_DIR, "assets", "imagens", "spritesheet.bmp")

CAMINHO_CHAO = os.path.join(BASE_DIR, "assets", "imagens", "chao.png")

MUSICA_FUNDO = os.path.join(BASE_DIR, "assets", "sons", "musica_fundo.wav")
SOM_CRISTAL = os.path.join(BASE_DIR, "assets", "sons", "cristal.wav")
SOM_DANO = os.path.join(BASE_DIR, "assets", "sons", "dano.wav")
SOM_PORTAL = os.path.join(BASE_DIR, "assets", "sons", "portal.wav")