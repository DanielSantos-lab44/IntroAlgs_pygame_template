# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

> Labirinto do Tempo

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Daniel Carneiro (Interface e Integração)
- Andre Luiz Pinheiro (Design de Fases e Colisão)
- Gabriel Pandino (Áudio e Estruturas)
- Enzo Carneiro (Testes e Documentação)

## 3. Tipo de jogo

Indique o tipo de jogo que será desenvolvido.

> Labirinto com coleta de itens, sistema de pontuação e fuga de inimigos.

## 4. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará.

> O jogo apresenta um mapa de labirinto em 2D visto de cima. O jogador controla um guerreiro e precisa explorar o mapa para encontrar e coletar os "Cristais do Tempo". Durante a exploração, inimigos (morcegos) patrulham os corredores e devem ser evitados. Ao coletar o cristal, um portal mágico é ativado, permitindo que o jogador avance para a próxima fase.

## 5. Objetivo do jogador

Explique qual é o objetivo principal do jogador.

> Coletar os cristais para acumular pontos e alcançar o portal de saída para escapar das 3 fases do labirinto com vida.

## 6. Regras principais

Liste as principais regras do jogo.

- **Regra 1:** O jogador começa a partida com 3 vidas.
- **Regra 2:** Cada cristal coletado vale 10 pontos e muda de lugar no mapa de forma acessível.
- **Regra 3:** Tocar em um inimigo desconta 1 vida e concede uma breve janela de invencibilidade.
- **Regra 4:** O portal de avanço de fase só é ativado após uma coleta bem-sucedida.
- **Regra 5:** O recorde de pontuação máxima (High Score) é salvo automaticamente no computador.

## 7. Condição de vitória

Explique como o jogador vence ou conclui o jogo.

> O jogador vence ao sobreviver e atravessar o portal de saída na terceira e última fase do labirinto, acionando a tela de "VOCÊ ESCAPOU!".

## 8. Condição de derrota ou encerramento

Explique como o jogador perde ou quando a partida termina.

> O jogador perde e a partida é encerrada (Game Over) se o seu número de vidas chegar a zero por conta de colisões sucessivas com os inimigos.

## 9. Elementos previstos no jogo

Descreva os principais elementos que farão parte do jogo.

**Jogador ou elemento principal**
> Um personagem (guerreiro/aventureiro) renderizado a partir de uma spritesheet, controlado pelas setas direcionais do teclado.

**Obstáculos, inimigos ou desafios**
> Paredes de pedra que bloqueiam a passagem (física de grade) e morcegos inimigos que causam dano ao toque e perseguem o jogador pelo labirinto.

**Itens, alvos ou objetos de interação**
> Cristais brilhantes (gemas) que aumentam a pontuação e um portal roxo que transporta o jogador entre os níveis.

**Pontuação, vidas, tempo ou progresso**
> Sistema de pontuação contínua (+10 por cristal), sistema de persistência (lê e grava o recorde em um arquivo `.txt`), e HUD na tela exibindo os Pontos, Recorde e as 3 Vidas restantes.

## 10. Controles previstos

Informe os comandos que serão utilizados pelo jogador.

- **Setas direcionais (Cima/Baixo/Esquerda/Direita):** Movimentar o jogador pelo mapa.
- **ESPAÇO:** Iniciar o jogo a partir da tela de Menu.
- **R:** Reiniciar a partida nas telas de Game Over ou Vitória.
- **ESC:** Sair e fechar o jogo a qualquer momento.

## 11. Organização inicial do código

Explique como o grupo pretende organizar o código.

- `main.py`: inicia a aplicação e chama o módulo do jogo.
- `src/jogo.py`: contém o loop principal, a renderização e a máquina de estados (telas).
- `src/config.py`: guarda configurações globais, dimensões da tela, cores e caminhos de arquivos.
- `src/funcoes.py`: contém funções puras para lógica matemática, física e colisões.
- `src/sprites.py`: gerencia o recorte das imagens (spritesheet) e as matrizes das 3 fases.
- `src/dados.py`: funções para gravação e leitura do arquivo de recorde (`recorde.txt`).
- `src/audio.py`: classe para gerenciamento de músicas e efeitos sonoros.
- `tests/test_funcoes.py`: scripts de testes automatizados usando `pytest`.

## 12. Recursos externos previstos

Informe se o grupo pretende utilizar imagens, sons, fontes, tutoriais ou códigos externos.

> Pretendemos utilizar *spritesheets* gratuitas e livres de direitos autorais para os personagens e chão, bem como arquivos de áudio `.wav` baixados de bancos gratuitos para os efeitos de coleta e dano. Utilizaremos as bibliotecas externas Pygame (motor do jogo) e Pytest (para garantia de qualidade).

## 13. Principais dificuldades esperadas

Liste as dificuldades que o grupo acredita que poderá enfrentar.

- **Dificuldade 1:** Implementar a matemática de colisão de forma perfeita para que o jogador não atravesse as paredes do labirinto.
- **Dificuldade 2:** Integração limpa do código de quatro integrantes sem gerar conflitos críticos (*merge conflicts*).
- **Dificuldade 3:** Criar uma inteligência artificial funcional de perseguição para o inimigo seguir o jogador pelo labirinto.

## 14. Escopo mínimo para a entrega final

Descreva qual será a versão mínima aceitável do jogo.

> A versão mínima terá um personagem capaz de andar livremente pela tela através das teclas, um item coletável que aumenta a pontuação na interface, um inimigo estático ou de movimento simples que retira vidas ao ser tocado, além das telas básicas de Menu Inicial e Fim de Jogo.

## 15. Possíveis melhorias, caso haja tempo

Liste funcionalidades extras que o grupo poderá implementar se conseguir concluir o escopo mínimo.

- **Melhoria 1:** Múltiplas fases com designs de mapas diferentes.
- **Melhoria 2:** Inteligência artificial de perseguição (*pathfinding*) para o inimigo.
- **Melhoria 3:** Sistema de persistência de dados (salvar o High Score localmente) e testes automatizados.