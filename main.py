#Creditos ao canal buildwithpython que me ensinou como fazer este jogo.
#O tema foi apenas uma brincadeira, humorismo do bom
import pygame
import random
import math
from pygame import mixer

#inicia o pygame
pygame.init()
#criar a tela
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('space.png')

#Som do Background
mixer.music.load('background.mp3')
mixer.music.play(-1)

#Titulo e icone da janela
pygame.display.set_caption("Goiaba Invaders")
icone = pygame.image.load('goiaba_icone.png')
pygame.display.set_icon(icone)

#Jogador
playerImg = pygame.image.load('goiabajog.png')
playerX = 370
playerY = 480
playerX_change = 0

#Inimigo
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('bolsoini.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#Bala
#Ready state significa que você não ira ver a bala
#Fira a bala estara em movimento
bulletImg = pygame.image.load('bala.png')
bulletX = 0
bulletY = 480 #A bala tem que ficar na mesma altura da nave
bulletX_change = 0
bulletY_change = 10 #Velocidade da bala
bullet_state = 'ready'

#pontuacao
score_value = 0
font = pygame.font.Font('minecraft.ttf', 30)

textX = 10
textY = 10

#Texto Game Over
over_font = pygame.font.Font('minecraft.ttf', 64)


#Funcao Game Over
def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

#Funcao placar
def show_score(x,y):
    score = font.render('Goiabadas: ' + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

#funcao Jogador
def player(x, y):
    screen.blit(playerImg, (x, y))

#funcao Inimigo
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#Funcao Bala.
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

#funcao colissao
def isCollision(enemyX, enemyY, bulletX, bulletY):
    #Esta é a formula para a distancia entre duas coordenadas (X,Y) e encontrar o centro delas
    # D = Raiz((X2 - X1)² + (Y2 - Y1)²) (,2 abaixo indica que é elevando ao quadrado
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Game loop mantem a tela aberta e fecha quando clicar no X de fechar
running = True
while running:

    # RGB -  Red - Green - Blue
    # A tela tem que vir antes de tudo. Se colocar depois ela fica sobreposta.
    screen.fill((0, 0, 0))
    #Backgroung
    screen.blit(background, (0, 0))
    #Se digitar "playerX += 0.1" #playerX += move para a direita  -  playerX -= move para a esquerda
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Os eventos abaixo são para identificar quando uma tecla é pressionada (KEYDOWN)
        # e quando uma tecla é solta (KEYUP) e se é para direita ou esquerda
        #Este processo deve estar dentro do "for event", no loop
        if event.type == pygame.KEYDOWN:
            #print('Uma tecla foi pressionada')
            if event.key == pygame.K_LEFT:#print('Seta da esquerda pressionada')
                playerX_change = -5 #Este é o incremento para a esquerda
            if event.key == pygame.K_RIGHT:#print('Seta da direita pressionada')
                playerX_change = 5 #Este é o incremento para a direita
            if event.key == pygame.K_SPACE:# Quando pressionar espaço, a bala aparece
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('jogando.wav')
                    bullet_Sound.play()
                    bulletX = playerX #aqui a bala sai da posição atual da nave. Sem essa funcao, a bala acompanha a nave
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                #print('A tecla foi solta')

    playerX += playerX_change #Precisa estar dentro do loop

    #Definindo limites dentro da tela
    #A imagem tem 64 pixels, 800 - 64 = 736
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736



    #Movimento do inimigo
    for i in range(num_of_enemy):

        #Game over
        if enemyY[i] > 420: #limite para dar a mensagem de game over
            for j in range(num_of_enemy):
                enemyY[j] = 2000 #Joga para a posicao Y=2000 para sumir tudo da tela
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]  # Precisa estar dentro do loop
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        # Colissao
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('canalhas.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1  # toda vez que tem a colissao, a pontuacao soma em + 1 (score = score + 1)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)  # Precisa estar dentro do loop e do for

    #Movimento da bala
    if bulletY <= 0: #repete quando aperta espaco essa é a bala na posicao final
        bulletY = 480 #aqui é a bala na posicao inicial (na "goiaba")
        bullet_state = 'ready'

    if bullet_state is 'fire': #movimento
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY) #Precisa estar dentro do loop
    show_score(textX, textY)
    pygame.display.update() #Atualiza a tela de acordo com a configuração dentro do while running: