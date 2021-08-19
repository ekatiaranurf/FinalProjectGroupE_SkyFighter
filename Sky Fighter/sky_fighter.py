#Title Game : Sky Fighter
#Short Description : Attack UFOs to save the earth by pressing key left, key right, and key space for bullets!

# Accessing the Library
import pygame
from pygame import mixer
import math
import random

# Intialize the pygame
pygame.init()

# create the SCREEN
SCREEN = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/background_earth.png')

# Sound
mixer.music.load("sounds/RunningGame.mp3")
mixer.music.play(-1)

# Caption dan Icon Game
pygame.display.set_caption("Sky Figther")
icon = pygame.image.load('assets/spaceship.png')
pygame.display.set_icon(icon)

# Spaceship (Spaceship that protects the earth)
spaceshipImg = pygame.image.load('assets/spaceship.png')
spaceshipX = 370
spaceshipY = 480
spaceshipX_change = 0

# UFO (UFO that will attack the earth)
UFOImg = []
UFOX = []
UFOY = []
UFOX_change = []
UFOY_change = []
num_of_UFO = 6

for i in range(num_of_UFO):
    UFOImg.append(pygame.image.load('assets/ufoalien.png'))
    UFOX.append(random.randint(0, 736))
    UFOY.append(random.randint(50, 150))
    UFOX_change.append(4)
    UFOY_change.append(40)

# Bullet (Bullets from Spaceship to attack UFO)
# Ready - You can't see the bullet on the SCREEN
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('assets/spaceship_bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    SCREEN.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    SCREEN.blit(over_text, (200, 250))


def spaceship(x, y):
    SCREEN.blit(spaceshipImg, (x, y))


def UFO(x, y, i):
    SCREEN.blit(UFOImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    SCREEN.blit(bulletImg, (x + 16, y + 10))


def isCollision(UFOX, UFOY, bulletX, bulletY):
    distance = math.sqrt(math.pow(UFOX - bulletX, 2) + (math.pow(UFOY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    SCREEN.fill((0, 0, 0))
    # Background Image
    SCREEN.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceshipX_change = -5
            if event.key == pygame.K_RIGHT:
                spaceshipX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("sounds/laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = spaceshipX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceshipX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    spaceshipX += spaceshipX_change
    if spaceshipX <= 0:
        spaceshipX = 0
    elif spaceshipX >= 736:
        spaceshipX = 736

    # UFO Movement
    for i in range(num_of_UFO):

        # Game Over
        if UFOY[i] > 440:
            for j in range(num_of_UFO):
                UFOY[j] = 2000
            game_over_text()
            show_score(325,370)
            bulletSound = mixer.Sound("sounds/GameOver.wav")
            bulletSound.play()
            break

        UFOX[i] += UFOX_change[i]
        if UFOX[i] <= 0:
            UFOX_change[i] = 4
            UFOY[i] += UFOY_change[i]
        elif UFOX[i] >= 736:
            UFOX_change[i] = -4
            UFOY[i] += UFOY_change[i]

        # Collision
        collision = isCollision(UFOX[i], UFOY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("sounds/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            UFOX[i] = random.randint(0, 736)
            UFOY[i] = random.randint(50, 150)

        UFO(UFOX[i], UFOY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    spaceship(spaceshipX, spaceshipY)
    show_score(textX, testY)
    pygame.display.update()
