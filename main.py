from view.spot import Spot
from busca.search import a_star
from view.view import draw_map, draw_path, draw_hobbits
from settings import PASSOS_if, dict_etapas, hobbits_index
import pygame
from genetica.cromossomo import *
from statistics import mean

hobbits_por_etapa = dict()

(width, height) = (1000, 500)
def make_grid():
    map_ = []
    with open('./dados/mapa.txt', 'r') as f:
        for i, linha in enumerate(f):
            map_.append([])
            for j,x in enumerate(linha):
                spot = Spot(i, j, x, width, height)
                map_[i].append(spot)

    return map_


def get_checkpoint(grid, state):

    for row in grid:
        for spot in row:
            if spot.state == state:
                return spot



def main():

    # IA
    
    genetico = gera_populacao(50, 500)

    print('Fitness medio: {}'.format(mean([c.tempo for c in genetico])))
    melhor_cromo = genetico[0]
    print('Tempo do melhor cromossomo: {}'.format(melhor_cromo.tempo))
    print('Hobbits selecionados para cada etapa:')
    nova_lista = []
    for hobbits in melhor_cromo.lista:
        novo_item = []
        for idx, elemento in enumerate(hobbits):
            if elemento == 1:
                novo_item.append(hobbits_index[idx])
        nova_lista.append(novo_item)

    print("Dicionario de etapas {}".format(dict_etapas))    
    hobbits_por_etapa['1'] = ['Frodo', 'Merry', 'Pippin', 'Sam']
    for idx, etapa in enumerate(dict_etapas.keys()):
        
        print('{nome_etapa}: {lista}'.format(nome_etapa=etapa, lista=nova_lista[idx]))
        hobbits_por_etapa[etapa] = nova_lista[idx]
        #draw_hobbits(etapa, hobbits)

    print("Lista de hobits por etapa")
    print(hobbits_por_etapa)
    # A*

    idx = 0
    
    grid = make_grid()
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
    
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))

    start = get_checkpoint(grid, PASSOS_if[idx][0]) 
    end = get_checkpoint(grid, PASSOS_if[idx][1])

    running = True
    finalizado = False
    while running:

        draw_map(screen, grid)
        draw_hobbits(screen, start.state, hobbits_por_etapa)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
    
                    
                    came_from = {}

                    if not finalizado and (start.state != '1' or (start.state == '1' and end.state == '2')):
                        draw_map(screen, grid)
                        pygame.display.update()
                        came_from = a_star(grid, start, end, screen)
                        draw_hobbits(screen, start.state, hobbits_por_etapa)

                    if idx < len(PASSOS_if) - 1:
                        idx+=1
                    else:
                        finalizado = True
                        draw_path(came_from, grid, end)
                        draw_map(screen, grid)
                        pygame.display.update()

                    if (came_from and not finalizado):
                        start = get_checkpoint(grid, PASSOS_if[idx][0])
                        end = get_checkpoint(grid, PASSOS_if[idx][1])
                        draw_path(came_from, grid, start)


if __name__ == '__main__':
    main()
