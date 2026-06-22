import pygame
from src.config import MUSICA_FUNDO, SOM_CRISTAL, SOM_DANO, SOM_PORTAL

class Audio:
    def __init__(self):
        pygame.mixer.init()

        self.som_cristal = pygame.mixer.Sound(SOM_CRISTAL)
        self.som_dano = pygame.mixer.Sound(SOM_DANO)
        self.som_portal = pygame.mixer.Sound(SOM_PORTAL)

        self.som_cristal.set_volume(0.6)
        self.som_dano.set_volume(0.7)
        self.som_portal.set_volume(0.8)
    
    def tocar_musica_fundo(self):
        pygame.mixer.music.load(MUSICA_FUNDO)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    
    def tocar_cristal(self):
        self.som_cristal.play()
        
    def tocar_dano(self):
        self.som_dano.play()
        
    def tocar_portal(self):
        self.som_portal.play()