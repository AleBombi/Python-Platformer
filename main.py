import os 
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 8000
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites] #indicano come flippare l'immagine

def load_sprite_sheets(dir1, dir2, width, height, direction=False): #in questo modo direction è di default settato a False
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))] #carica ogni file presente il path se path è valido
    # os.path.isfile() method in Python is used to check whether the specified path is an existing regular file or not

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() #convert alpha permette di avere lo sfondo trasparente

        sprites = []
        for i in range(sprite_sheet.get_width()//width): # width larghezza dell'intera immagine
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) #stiamo creando la superficie di un'immagine singola
            rect = pygame.Rect(i*width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect) 
            sprites.append(pygame.transform.scale2x(surface))

        if direction: # siccome le immagini hanno come direzione destra, in una animazione multidirezionale dobbiamo flippare quelle immagini per avere la direzione a sinistra
            all_sprites[image.replace(".png", "")+"_right"] = sprites
            all_sprites[image.replace(".png", "")+"_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    
    return all_sprites

class Player(pygame.sprite.Sprite): # modo per eridare le proprietà di Sprite
    COLOR=(255, 0, 0)
    GRAVITY = 1


    def __init__(self, x, y, width, height):
        self.rect=pygame.Rect(x,y, width, height) # self rappresenta l'instanza della classe, permette di accedere agli attributi e metodi della classe
        self.x_vel=0
        self.y_vel=0
        self.mask=None
        self.direction="left" 
        self.animation_count=0
        self.fall_count=0
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel # velocità negativa perchè dobbiamo sottrarre alle ascisse
        if self.direction != "left":
            self.direction = "left"
            self.animation_count= 0

    def move_right(self, vel):
        self.x_vel = vel   
        if self.direction != "right":
            self.direction = "right"
            self.animation_count= 0

    def loop(self, fps):
        self.y_vel+= min(1, (self.fall_count/fps)*self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1


    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT// height + 1):
            pos = (i*width, j*height) # tupla che contiene le posizioni
            tiles.append(pos)

    return tiles, image



def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)
    
    player.draw(window)
   
    pygame.display.update()


def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel=0 #necessario affinche il personaggio si fermi quando smettiamo di premere un tasto
    if keys[pygame.K_LEFT]: # per utilizzare il tasto a per andare a sinistra si deve sostituire K_LEFT con K_a
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Gray.png")

    player = Player(100,100,50,50)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player)
        draw(window, background, bg_image, player)

    pygame.quit()
    quit()
    
   



if __name__ == "__main__":
    main(window)

