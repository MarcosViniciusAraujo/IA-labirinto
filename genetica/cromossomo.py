
from random import *
from settings import *


def gera_populacao(num_ger_max, qto_populacao):
    num_geracoes = 0

    crom = [Cromossomo() for _ in range(qto_populacao)]
    validacao = True

    while True:
        print('Geração {}.'.format(num_geracoes + 1))


        crom.sort(key=lambda x: x.tempo)
        
        if num_geracoes == num_ger_max:
            break

        prox_cromo = []


        '''
            manter os 10% melhores 
            cross over dos melhores para preencher 40%
            resto é random
        '''

        melhoresNum = qto_populacao // 10


        melhores = crom[:melhoresNum]
        prox_cromo += melhores
        to_crossover = crom[melhoresNum: melhoresNum * 5]

        
        # crossover : melhores x não melhores
        for cromo in to_crossover:

            filho = -1

            while True:
                filho = Cromossomo.crossover(cromo, choice(melhores))

                if filho is not None:
                    prox_cromo.append(filho)
                    break

        # crossover : melhores x melhores
        
        for i, cromo in enumerate(melhores):

            options = [j for j in range(len(melhores)) if i != j]

            filho1 = -1
            filho2 = -1

            
            while True:
                
                escolhido = choice(options)
                filho1 = Cromossomo.crossover(cromo, melhores[escolhido])

                if filho1 is not None:
                    prox_cromo.append(filho1)
                    options.remove(escolhido)
                    break


            while True:
    
                escolhido = choice(options)
                filho2 = Cromossomo.crossover(cromo, melhores[escolhido])

                if filho2 is not None:
                    prox_cromo.append(filho2)
                    options.remove(escolhido)
                    break
            
        
        
        qto_random = qto_populacao  - 5 * melhoresNum

        for i in range(qto_random):
            prox_cromo.append(Cromossomo())

        num_geracoes += 1
        
        crom = prox_cromo


    return crom

def calcula_tempo(etapa, lista_hobbits):
    agilidade = 0

    for hobbit in lista_hobbits:

        agilidade += dict_agilidade.get(hobbit)
    return dict_etapas.get(etapa) / agilidade


def valida_lista(lista):
    soma = [0, 0, 0, 0]
    for elemento in lista:
        if elemento == [0, 0, 0, 0]:
            return False
        for i in range(4):
            soma[i] += elemento[i]

    for e in soma:
        if e > 7:
            return False

    if soma == [7, 7, 7, 7]:
        return False

    return True


class Cromossomo:

    def __init__(self, filho=False):
        self.tempo = -1
        self.lista = [-1] * 16

        if not filho:
            self.cria_aleatorio()


    def __str__(self):
        return "Fitness: {}".format(self.tempo)
    
    def __add__(self, other):
        return other.tempo + self.tempo

    def cria_aleatorio(self):
        lista = []
        energia = [7, 7, 7, 7]

        for i in range(16):
            if energia == [0, 0, 0, 0]:
                self.cria_aleatorio()
                return 
            while True:
                
                lst = [0 if energia[k] == 0 else randint(0, 1) for k in range(4)]
                if lst != [0, 0, 0, 0]:
                    break

            for j in range(4):
                energia[j] -= lst[j]

            lista.append(lst)

        if energia == [0, 0, 0, 0]:
            self.cria_aleatorio()
            return

        self.lista = lista

        self.calcula_tempo_etapas()

    def calcula_tempo_etapas(self):
        tempo = 0
        for i, num_hobbits in enumerate(self.lista):
            lista_hobbits = []
            if num_hobbits[0]:
                lista_hobbits.append("Pippin")
            if num_hobbits[1]:
                lista_hobbits.append("Merry")
            if num_hobbits[2]:
                lista_hobbits.append("Sam")
            if num_hobbits[3]:
                lista_hobbits.append("Frodo")

            tempo += calcula_tempo(PASSOS[i + 1], lista_hobbits)
        self.tempo = tempo
        return

    def mutacao_linhas(self):
        temp = self.lista.copy()
        ind_a = randint(0, 15)
        ind_b = randint(0, 15)
        while ind_a == ind_b:
            ind_b = randint(0, 15)

        temp[ind_a], temp[ind_b] = temp[ind_b], temp[ind_a]
        self.lista = temp
        return

    def mutacao_colunas(self):
        temp = self.lista.copy()
        hobbit_a = randint(0, 3)
        hobbit_b = randint(0, 3)
        while hobbit_a == hobbit_b:
            hobbit_b = randint(0, 3)

        for i in range(16):
            temp[i][hobbit_a], temp[i][hobbit_b] = temp[i][hobbit_b], temp[i][hobbit_a]
        self.lista = temp
        return

    def mutacao_random(self):
        while True:
            temp = self.lista.copy()
            rand_hobbit = randint(0, 3)
            rand_etapa = randint(0, 15)

            temp[rand_etapa][rand_hobbit] ^= 1
            if valida_lista(temp):
                self.lista = temp
                return

    @classmethod
    def crossover(cls, pai, mae):
        filho = Cromossomo(filho=True)
        herancas_pai = randint(1, 15)
        lista_indices = [i for i in range(16)]
        shuffle(lista_indices)
        for i in lista_indices:
            if herancas_pai:
                temp = pai.lista[i].copy()
                filho.lista[i] = temp
                herancas_pai -= 1
            else:
                temp = mae.lista[i].copy()
                filho.lista[i] = temp

        if filho.valida_cromo():
            mutacao = randint(0, 9)
            match mutacao:
                case 0:
                    filho.mutacao_linhas()
                case 1:
                    filho.mutacao_colunas()
                case 2:
                    filho.mutacao_random()
            
            filho.calcula_tempo_etapas()
            return filho
        return None

    def valida_cromo(self):
        return valida_lista(self.lista)
