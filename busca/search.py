from queue import PriorityQueue
import pygame
from time import sleep
from settings import PASSOS



def get_time_from_terrain(terreno:str):
    return {
        ".":1,
        "R":5,
        "V":10,
        "M":200,
        "P":-1,
        "#":-1
    }.get(terreno)


def h(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(grid, start, end, screen):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # heap
    came_from = {}

    g_score = {spot.get_pos(): float("inf") for row in grid for spot in row}
    g_score[start.get_pos()] = 0 

    f_score = {spot.get_pos(): float("inf") for row in grid for spot in row}
    f_score[start.get_pos()] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start.get_pos()}

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]

        open_set_hash.remove(current.get_pos())
        

        if current == end:
            # make path
            return came_from

        for neighbor in current.neighbors:


            pygame.draw.rect(
                    screen, 
                    (255, 0, 0), 
                    pygame.Rect(
                        neighbor.x, 
                        neighbor.y, 
                        neighbor.square_width, 
                        neighbor.square_height
                    )
            )
            
            

            pygame.display.update()

            temp = 0
            
            if neighbor.state not in PASSOS:
                temp = get_time_from_terrain(neighbor.state)
            else:
                temp = 1

            temp_g_score = g_score[current.get_pos()] +  temp # alterar aqui
            
            temp_f_score = temp_g_score + h(current.get_pos(), end.get_pos())
            
            if temp_f_score < f_score[neighbor.get_pos()]:

                came_from[neighbor.get_pos()] = current
                g_score[neighbor.get_pos()] = temp_g_score
                f_score[neighbor.get_pos()] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor.get_pos() not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor.get_pos()], count, neighbor)) 
                    open_set_hash.add(neighbor.get_pos())
                    neighbor.make_open()
        
        if current != start:
            current.make_close()

    return False




def pegaMenor(lista):
    menor = lista[0]
    for i in lista[1:]:
        if menor.f > i.f:
            menor = i
    return menor


#

'''
def astar2(GameMap,etapa, node, ScreenBoard):
    aberta=[]
    fechada=[]  
    aberta.append(node)
    current=node
    cor = (randint(0,255),randint(0,255),randint(0,255))
    while aberta:
        current = pegaMenor(aberta)
        #print(current.x,current.y)
        if (current.x == etapa.GoalX and current.y == etapa.GoalY):
            pathList = current.getPath()
            return pathList
        aberta.remove(current)
        fechada.append(current)
        vizinhos=current.getVizinhos(GameMap, etapa)
        for nextNode in vizinhos:
            inFechada=False
            inAberta=False
            for i in fechada:
                if(nextNode.x==i.x and nextNode.y==i.y):
                   ScreenBoard.draw_path(nextNode.x,nextNode.y,GameMap,cor)
                   inFechada=True
            if(not(inFechada)):   
                for i in aberta: 
                    if(nextNode.x==i.x and nextNode.y==i.y):
                        inAberta=True
                        if (nextNode.f<i.f):
                            i.f=nextNode.f
                            nextNode.partner=current
                if(inAberta==False):
                   aberta.append(nextNode)
                   nextNode.partner=current
    print("Caminho não encontrado")
    return None
'''