import pygame
import os
import sys
import random

pygame.init()
current_path=os.path.dirname(__file__)
os.chdir(current_path)
WIDTH=1200
HEIGHT=800
FPS=60
#pygame.mixer.music.load('sound/mario.mp3')
#pygame.mixer.music.play(-1)
lvl="menu"
sc=pygame.display.set_mode((WIDTH, HEIGHT))
clock=pygame.time.Clock()

from load import *

def startMenu():
    global lvl
    lvl = "menu"
    sc.blit(menu_image, (0, 0))
    sc.blit(space_image, (370, 600))
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        lvl = "Game"
    #sc.blit(start_image, (100, 200))
    #sc.blit(records_image, (100, 300))
    #sc.blit(exit_image, (100, 400))
    #pos_mouse=pygame.mouse.get_pos()
    pygame.display.update()

def game_lvl():
    sc.fill((128, 128, 128))
    sc.blit(earth_image, (0, HEIGHT - 100))
    player_group.update()
    player_group.draw(sc)
    earth_group.update()
    earth_group.draw(sc)
    kaktys_group.update()
    kaktys_group.draw(sc)
    sword_group.update()
    sword_group.draw(sc)
    pygame.display.update()


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = HEIGHT - 40
        self.jump = False
        self.jump_step = -22
        self.timer_spawn = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
    def update(self):
        global FPS
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.jump = True
        if self.jump:
            if self.jump_step <= 22:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -22
        self.timer_spawn += 1
        self.timer_spawn += 1
        if self.timer_spawn / FPS > random.randint(3, 6):
            kaktys = Kaktys(kaktys_image)
            kaktys_group.add(kaktys)
            self.timer_spawn = 0
        if self.timer_spawn / FPS > 4:
            sword = Sword(sword_image)
            sword_group.add(sword)
            self.timer_spawn = 0
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "red", (x, y), 3)


class Kaktys(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 500)
        self.rect.bottom = HEIGHT - 40
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
    def update(self):
        global FPS
        self.rect.x -= self.speed
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "blue", (x, y), 3)
        if len(set(self.mask_list) & set(player.mask_list)) > 0:
            sys.exit()

class Sword(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 500)
        self.rect.bottom = HEIGHT - 40
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
    def update(self):
        global FPS
        self.rect.x -= self.speed
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "blue", (x, y), 3)


def restart():
    global player_group, earth_group, kaktys_group, sword_group, player
    earth_group = pygame.sprite.Group()
    kaktys_group = pygame.sprite.Group()
    sword_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = Player(player_image, (0, 0))
    player_group.add(player)


restart()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if lvl == "Game":
        game_lvl()
    elif lvl == "menu":
        startMenu()
    clock.tick(FPS)