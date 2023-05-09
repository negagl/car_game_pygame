# Setting up our game
import random
import sys
import time
import pygame
from pygame.locals import *

# Allows us to initialize the engine
pygame.init()

# FPS
FPS = 60
clock = pygame.time.Clock()

# Speed and Score
speed = 5

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("Verdana", 60)
small_font = pygame.font.SysFont("Verdana", 60)
game_over = font.render("Game Over", True, BLACK)

# Background
background = pygame.image.load("assets/background.jpg")
x = 0
y = 0

# Screen
S_WIDTH = 400
S_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Gamecito")

# Enemy Images
images = [
    "assets/player2-1.png",
    "assets/player2-2.png",
    "assets/player2-3.png"
]

# Enemy


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(random.choice(images))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, S_WIDTH-30), 0)

    def move(self):
        self.rect.move_ip(0, speed)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, S_WIDTH-30), 0)
            self.image = pygame.image.load(random.choice(images))


# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 550)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -speed)

        if self.rect.bottom < 600:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, speed)

        if self.rect.left > 15:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-speed, 0)

        if self.rect.right < S_WIDTH-15:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(speed, 0)


# initialize classes
P1 = Player()
E1 = Enemy()

# Create sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop start, where all things happen
while True:
    for event in pygame.event.get():

        # Increment speed
        if event.type == INC_SPEED:
            speed += 1

        # Exit game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # DISPLAYSURF.blit(background, (x, y))

    # Movimiento del fondo
    y_relative = y % background.get_rect().height
    DISPLAYSURF.blit(background, (x, y_relative -
                     background.get_rect().height))
    if y_relative < S_HEIGHT:
        DISPLAYSURF.blit(background, (0, y_relative))
    y += 5

    # Redraw all charcters
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)  # Draw
        entity.move()  # Move

    # If there's a collision
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(FPS)
