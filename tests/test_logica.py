import pygame
from src.funcoes import (
    verificar_colisao,
    limitar_valor,
    calcular_pontos,
    tomar_dano,
    jogador_perdeu
)

def test_verificar_colisao_com_sucesso():
    """Testa se a função de colisão detecta quando dois retângulos se sobrepõem."""
    rect1 = pygame.Rect(100, 100, 50, 50)
    rect2 = pygame.Rect(100, 100, 50, 50)
    assert verificar_colisao(rect1, rect2) == True

def test_verificar_colisao_sem_sucesso():
    """Testa se a função de colisão funciona quando os retângulos estão distantes."""
    rect1 = pygame.Rect(10, 10, 50, 50)
    rect2 = pygame.Rect(500, 500, 50, 50)
    assert verificar_colisao(rect1, rect2) == False

def test_limitar_valor():
    """Testa se o valor não ultrapassa os limites da tela (usado no movimento)."""
    assert limitar_valor(5, 0, 10) == 5    # Dentro do limite
    assert limitar_valor(-5, 0, 10) == 0   # Passou do limite mínimo
    assert limitar_valor(15, 0, 10) == 10  # Passou do limite máximo

def test_calcular_pontos():
    """Testa o acréscimo de pontuação ao pegar cristais."""
    assert calcular_pontos(100, 10) == 110
    assert calcular_pontos(0, 50) == 50

def test_tomar_dano():
    """Testa a redução de vidas quando toca no inimigo."""
    assert tomar_dano(3, 1) == 2
    assert tomar_dano(1, 1) == 0

def test_jogador_perdeu():
    """Testa a condição de Game Over (vida zero ou menor)."""
    assert jogador_perdeu(0) is True
    assert jogador_perdeu(-1) is True
    assert jogador_perdeu(1) is False