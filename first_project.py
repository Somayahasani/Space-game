import pygame
import math
import random
from pygame import mixer

## Initialising this init() to active all pygame's tutorials
pygame.init()

## Create the scree (width(x),  heigth(y))
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("space.jpg")
mixer.music.load("background.mp3")
mixer.music.play(-1)
# Tite and Icon
pygame.display.set_caption("My first Pygame")
icon = pygame.image.load("planet.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0.5

## Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("invador.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(5, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


## Ready - You can't see the bullet on the screen
## Fire = The bullet is currently running
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletX_change = 2
bullet_state = "ready"
# score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

texX = 10
texY = 10

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over_text = over_font.render(
        "GAME OVER: " + str(score_value), True, (255, 255, 255)
    )
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))  ## Drawing the image in screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  ## Drawing the image in screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        (math.pow(enemyX - bulletX, 2)) + math.pow(enemyY - bulletY, 2)
    )
    if distance < 27:
        return True
    else:
        return False


## Game loop (the window is running and not hanging)
running = True
while running:
    screen.fill((0, 0, 0))  # Color of rgb (red, green, blue)
    # Background image
    screen.blit(background, (0, 0))

    for (
        event
    ) in (
        pygame.event.get()
    ):  ### This line means that all of the events that pygame has are happening in this code
        if event.type == pygame.QUIT:
            running = False
        ## If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # bullet_sound = mixer.Sound('shooting sound.mp3')
                    # bullet_sound.play()
                    bulletX = playerX
                bullet_state = "fire"

    ## Algorithms: Cecking for boundaries so it doesn't go out of the bounds.
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    ## Enemy Movement
    for i in range(num_of_enemies):
        ## Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        ## Collision
    for i in range(num_of_enemies):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explosion_sound = mixer.Sound('explode.mp3')
            # explosion_sound.play()
            bulletY = 400
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(5, 150)

        enemy(enemyX[i], enemyY[i], i)
    ## Bullet shot
    if bulletY <= 0:
        bulletY = 480
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletX_change
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

    show_score(texX, texY)
    player(playerX, playerY)
    pygame.display.update()
