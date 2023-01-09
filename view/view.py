import pygame
from pygame.locals import *
import os
from settings import PASSOS
from time import sleep


COLORS = {
    ".": (114, 219, 142),
    "R": (120, 90, 42),
    "V": (5, 117, 33),
    "M": (41, 36, 30),
    "P": (0, 0, 0),
    "#": (58, 71, 222),
    "checkpoint": (232, 224, 0)
}

sysfont = pygame.font.get_default_font()

cor_do_caminho = (200, 109, 252)



def draw_map(screen, grid):
    

    screen.fill((255, 255, 255))

    for row in grid:
        for spot in row:
            pygame.draw.rect(
                screen, 
                spot.color, 
                pygame.Rect(
                    spot.x, 
                    spot.y, 
                    spot.square_width, 
                    spot.square_height
                )
            )
    

    eye = pygame.image.load(os.path.join(os.path.dirname(__file__), '../img/eye.png')).convert_alpha()
    eye = pygame.transform.scale(eye, (60, 60))
    screen.blit(eye, (730, 270))

    


def draw_path(path, grid, end):
    cont = 0
    start = path.get(end.get_pos())
    # print("drawpath", end, start)
    while start is not None:
        cont += 1
        if start.state not in PASSOS:
            grid[start.row][start.col].color = cor_do_caminho
        start = path.get(start.get_pos())
    pygame.display.update()

def draw_hobbits(screen, etapa, hobbits_por_etapa):
    x = 80
    offset = 120
    hobbits = hobbits_por_etapa.get(etapa)
    print(hobbits)
    for i in range(len(hobbits)):
        hobbit_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '../img/{}.png'.format(hobbits[i]))).convert_alpha()
        #hobbit_img = pygame.transform.scale(hobbit_img, (80 + i * offset, 80))
        screen.blit(hobbit_img, (10 + i * offset, 350))
    pygame.display.update()
    return

