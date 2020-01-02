# Pygame template

import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shmup!')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speedx

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, 40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.left > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, 40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

mobs = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

bullets = pygame.sprite.Group()

running = True

while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    # Events
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    # Update
    all_sprites.update()

    # Check if bullet hit mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # check to see if a mob hit the player

    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False




    # Draw / Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
