import pygame
import random
import os
import math

score = 0
time = 0
enemy_count = 0
num_of_enemies = 6
health = 3

# Intialize the pygame
pygame.init()

# Centreing the screen
screenx = 230
screeny = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screenx,screeny)

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

#Caption and Icon
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    randnumber = random.randint(1, 6)
    enemyImg.append(pygame.image.load('enemy' + str(randnumber) + '.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet Image

# ready state - bullet isnt on screen

# fire state - bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 6
bullet_state = "ready"

# Function to draw player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to draw Enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Function to draw bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

# Enemy-Bullet Collision Calculations
def ifCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Player-Enemy Collision Calculations
def ifEnemyPlayerCollision(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt((math.pow(playerX-enemyX, 2)) + (math.pow(playerY-enemyY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # Screen Colour - R, G, B
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # Closing the window
        if event.type == pygame.QUIT:
            running = False

        # If Keystroke is pressed check if its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_RIGHT:
                playerX_change = 3                
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Keystroke Released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Movement and Boundries (PLAYER)
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Movement and Boundries (ENEMY)
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)

    # Collision
        collision = ifCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(f"score = {score}")
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enPlayCollision = ifEnemyPlayerCollision(playerX, playerY, enemyX[i], enemyY[i])
        if enPlayCollision:
            health -= 1            
            enemyX[i] = (random.randint(0, 735))
            enemyY[i] = (random.randint(50, 150))
            enemyX_change[i] = (2)
            enemyY_change[i] = (40)
            print(f"health = {health}")

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Drawing Player
    player(playerX, playerY)

    # Updating Screen
    pygame.display.update()
