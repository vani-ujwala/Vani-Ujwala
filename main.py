import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((900, 700))

# Background
background = pygame.image.load('background.jpg')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("CHICK INVADERS")
icon = pygame.image.load('fox.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('man.png')
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('fox.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Balloon

# Ready - You can't see the balloon on the screen
# Fire - The balloon is currently moving

balloonImg = pygame.image.load('balloon.png')
balloonX = 0
balloonY = 480
balloonX_change = 0
balloonY_change = 10
balloon_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_balloon(x, y):
    global balloon_state
    balloon_state = "fire"
    screen.blit(balloonImg, (x + 26, y + 10))


def isCollision(enemyX, enemyY, balloonX, balloonY):
    distance = math.sqrt(math.pow(enemyX - balloonX, 2) + (math.pow(enemyY - balloonY, 2)))
    if distance <30:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    #RGB = Red, Green, Blue
    screen.fill((0,0,0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if balloon_state is "ready":
                    balloonSound = mixer.Sound("104772701.mp3")
                    balloonSound.play()
                    # Get the current x cordinate of the spaceship
                    balloonX = playerX
                    fire_balloon (balloonX, balloonY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], balloonX, balloonY)
        if collision:
            explosionSound = mixer.Sound("Balloon popping _ burst _ blast (248BDBD-MSB).mp3")
            explosionSound.play()
            balloonY = 480
            balloon_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Balloon Movement
    if balloonY <= 0:
        balloonY = 480
        balloon_state = "ready"

    if balloon_state is "fire":
        fire_balloon(balloonX, balloonY)
        balloonY -= balloonY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
