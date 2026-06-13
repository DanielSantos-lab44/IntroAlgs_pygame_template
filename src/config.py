LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Projeto Final - Pygame"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212,212,212)
AZUL = (0, 0, 255)

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MUSICA_FUNDO = os.path.join(BASE_DIR, "assets", "sons", "musica_fundo.wav")
SOM_CRISTAL = os.path.join(BASE_DIR, "assets", "sons", "cristal.wav")
SOM_DANO = os.path.join(BASE_DIR, "assets", "sons", "dano.wav")
SOM_PORTAL = os.path.join(BASE_DIR, "assets", "sons", "portal.wav")