import pygame
            
def pegar_sprite(local_arquivo, x, y, width, height, scale=1):
    """Corta um único elemento de uma spritesheet BMP e remove o fundo."""
    
    # 1. Carrega o BMP e usa .convert() (sem alpha) para otimizar a velocidade
    sheet = pygame.image.load(local_arquivo).convert()

    # 2. Cria uma superfície padrão para o recorte (não precisa de SRCALPHA aqui)
    image = pygame.Surface((width, height))
    
    # 3. Copia o pedaço da folha BMP para a nossa nova imagem
    image.blit(sheet, (0, 0), (x, y, width, height))
    
    # 4. CONFIGURAÇÃO DA TRANSPARÊNCIA (O segredo para o BMP)
    # Pegamos a cor do pixel no canto superior esquerdo (0,0) do recorte, 
    # assumindo que o fundo do seu sprite começa ali.
    cor_do_fundo = image.get_at((0, 0))
    
    # Dizemos ao Pygame para ignorar essa cor específica na hora de desenhar
    image.set_colorkey(cor_do_fundo)
    
    # 5. Aplica o redimensionamento, se houver
    if scale != 1:
        novo_largura = int(width * scale)
        novo_altura = int(height * scale)
        image = pygame.transform.scale(image, (novo_largura, novo_altura))
        
    return image

nivel_iniciante = []

for i in range(40):          
    linha = []

    for j in range(42):      

        if i == 0 or i == 39 or j == 0 or j == 41:
            linha.append(1)

        elif i == 5 and 5 < j < 20:
            linha.append(1)

        elif i == 10 and 10 < j < 30:
            linha.append(1)

        elif j == 15 and 10 < i < 25:
            linha.append(1)

        elif j == 30 and 15 < i < 35:
            linha.append(1)

        else:
            linha.append(0)

    nivel_iniciante.append(linha)




nivel_iniciante[1][1] = 2      
nivel_iniciante[38][40] = 3    



for linha in nivel_iniciante:
    for bloco in linha:

        if bloco == 1:
            print("█", end="")   

        elif bloco == 2:
            print("☺", end="")  
        elif bloco == 3:
            print("★", end="")  

        else:
            print(" ", end="")  
    print()

    nivel_intermediario = []


for i in range(40):          
    linha = []

    for j in range(42):      

        if i == 0 or i == 39 or j == 0 or j == 41:
            linha.append(1)

        elif i == 4 and 3 < j < 18:
            linha.append(1)

        elif j == 8 and 4 < i < 20:
            linha.append(1)

        elif i == 12 and 8 < j < 30:
            linha.append(1)

        elif j == 25 and 12 < i < 30:
            linha.append(1)

        elif i == 25 and 10 < j < 35:
            linha.append(1)

        elif j == 34 and 18 < i < 35:
            linha.append(1)


        elif i == 8 and 25 < j < 35:
            linha.append(1)

        elif i == 18 and 5 < j < 15:
            linha.append(1)

        elif i == 32 and 15 < j < 28:
            linha.append(1)

        else:
            linha.append(0)

    nivel_intermediario.append(linha)




nivel_intermediario[1][1] = 2       # jogador
nivel_intermediario[38][40] = 3     # saída




for linha in nivel_intermediario:

    for bloco in linha:

        if bloco == 1:
            print("█", end="")

        elif bloco == 2:
            print("☺", end="")

        elif bloco == 3:
            print("★", end="")

        else:
            print(" ", end="")

    print()


    nivel_final = []


for i in range(40):
    linha = []

    for j in range(42):

        if i == 0 or i == 39 or j == 0 or j == 41:
            linha.append(1)



        elif i == 4 and 3 < j < 35:
            linha.append(1)

        elif i == 8 and 8 < j < 38:
            linha.append(1)

        elif i == 14 and 3 < j < 28:
            linha.append(1)

        elif i == 20 and 12 < j < 38:
            linha.append(1)

        elif i == 27 and 4 < j < 32:
            linha.append(1)

        elif i == 34 and 10 < j < 38:
            linha.append(1)




        elif j == 6 and 4 < i < 15:
            linha.append(1)

        elif j == 12 and 14 < i < 28:
            linha.append(1)

        elif j == 20 and 8 < i < 21:
            linha.append(1)

        elif j == 28 and 20 < i < 35:
            linha.append(1)

        elif j == 35 and 5 < i < 20:
            linha.append(1)




        elif i == 11 and 20 < j < 35:
            linha.append(1)

        elif i == 24 and 5 < j < 18:
            linha.append(1)

        elif i == 31 and 20 < j < 30:
            linha.append(1)



        else:
            linha.append(0)


    nivel_final.append(linha)




nivel_final[1][1] = 2       
nivel_final[38][40] = 3      



for linha in nivel_final:

    for bloco in linha:

        if bloco == 1:
            print("█", end="")

        elif bloco == 2:
            print("☺", end="")

        elif bloco == 3:
            print("★", end="")

        else:
            print(" ", end="")

    print()
