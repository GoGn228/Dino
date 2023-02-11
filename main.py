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
font = pygame.font.SysFont("arial", 40)
score = 0
time = 10

from load import *

def startMenu():
    global lvl
    lvl = "menu"
    sc.blit(menu_image, (0, 0))
    sc.blit(space_image, (370, 600))
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        lvl = "Game"
    pygame.display.update()

def game_lvl():
    global records_list, score
    sc.fill((128, 128, 128))
    sc.blit(earth_image, (0, HEIGHT - 100))
    sc.blit(cloud_image, (200, 70))
    sc.blit(cloud_image, (800, 50))
    player_group.update()
    player_group.draw(sc)
    earth_group.update()
    earth_group.draw(sc)
    kaktys_group.update()
    kaktys_group.draw(sc)
    sword_group.update()
    sword_group.draw(sc)
    with open("score.txt", "r", encoding="utf-8") as file:
        records_list = []
        for i in range(5):
            records_list.append(file.readline().replace("\n", ""))
    text_font = font.render(records_list[0], True, "black")
    sc.blit(text_font, (1000, 50))
    with open("score.txt", "w", encoding="utf-8") as file:
        file.write(str(score) + "\n")
    pygame.display.update()


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = HEIGHT - 40
        self.jump = False
        self.jump_step = -22
        self.timer_spawn_kaktus = 0
        self.timer_spawn_kaktus2 = 0
        self.timer_spawn_sword = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        self.frame = 0
        self.timer_anime = 0
        self.anime = True
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
        if key[pygame.K_DOWN]:
            self.image = player_sit_image
        self.timer_spawn_kaktus += 1
        self.timer_spawn_kaktus2 += 1
        self.timer_spawn_sword += 1
        if self.timer_spawn_kaktus / FPS > time:
            kaktys = Kaktys(kaktys_image)
            kaktys_group.add(kaktys)
            self.timer_spawn_kaktus = 0
        if self.timer_spawn_kaktus2 / FPS > time - 2:
            kaktys2 = Kaktys(kaktys2_image)
            kaktys_group.add(kaktys2)
            self.timer_spawn_kaktus2 = 0
        if self.timer_spawn_sword / FPS > time + 15:
            sword = Sword(sword_image)
            sword_group.add(sword)
            self.timer_spawn_sword = 0
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "red", (x, y), 3)
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player_image) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0
        self.image = player_image[self.frame]


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
        global FPS, sword
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
        self.rect.bottom = HEIGHT - 250
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
            self.kill()



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
    score += 1
    time -= 0.001
    clock.tick(FPS)