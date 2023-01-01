from email.policy import default
from simulator.agent import Agent, BrooksAgent
from simulator.entities import Food, Obstacle
from Algorithms.AStar import AStar
from Algorithms.transform import betterMove, transform
import random
from math import inf

from simulators.simulator_02.entities import HidePlace


directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

class PredatorAgentPropierties:
    def __new__(cls, digestion_time, max_energy, alpha = 1, beta = 1):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PredatorAgentPropierties, cls).__new__(cls)
            cls.digestion_time = digestion_time
            cls.max_energy = max_energy
            cls.alpha = alpha
            cls.beta = beta
            cls._behaviors = [
                (cls.__condicion_para_permanecer, cls.__accion_de_permanecer),
                (cls.__condicion_para_comer, cls.__accion_de_comer),
                (cls.__condicion_para_cazar, cls.__accion_de_cazar),
                (cls.__condicion_para_caminar, cls.__accion_de_caminar),
            ]
            cls.rand = random.Random()
        return cls.instance


    def manhathan_distance(i, j, o, p): return max(abs(i - o), abs(j - p))
    def __proximo_presa(self, P):
        (x, y) = P[1]
        min_distance = len(P[0]) + 1
        for i in range(len(P[0])):
            for j in range(len(P[0][i])):
                elem = P[0][i][j]
                distance_m = PredatorAgentPropierties.manhathan_distance(x, y, i, j)
                if type(scaredPreyAgent) in elem and min_distance > distance_m:
                    return True
        return False
    def __en_rango_presa(self, P):
        matriz = P[0]
        (x, y) = P[1]
        (real_x, real_y) = P[2]
        if Food() in matriz[x][y]  :
            self.future_position = (real_x, real_y)
            return True
        return False
        
        
    #### Regla 1 ####
    def __condicion_para_permanecer(self, P):
        return self.eating > 0 or ((self.prop.max_energy * self.prop.beta) > self.energy and self.rand()) or (self.prop.__proximo_depredador(P) and self.hidden)
    def __accion_de_permanecer(self, P):
        return P[2], False

    #### Regla 2 ####
    def __condicion_para_comer(self, P):
        return self.prop.__en_rango_presa(P) and (self.prop.max_energy * self.prop.alpha) > self.energy
    def __accion_de_comer(self, P):
        self.eating = self.prop.digestion_time
        return P[2], True

    #### Regla 3 ####
    def __condicion_para_cazar(self, P):
        return self.prop.__proximo_presa(P) and (self.prop.max_energy * self.prop.beta) > self.energy
    def __accion_de_cazar(self, P):
        prey_found = lambda ent: ent == type(scaredPreyAgent)
        obstacle_found = lambda ent: ent in [Obstacle()]                                                     # modificar lista para agragar obstaculos
        (x, y) = P[1]
        (real_x, real_y) = P[2]
        
        matrix = AStar(P[0], x, y, len(P[0]), prey_found, obstacle_found)
        abundance_matrix = transform(matrix)
        (dx, dy) = betterMove(abundance_matrix)

        (new_x, new_y) = x + dx -1, y + dy -1
        (new_real_x, new_real_y) = real_x + dx - 1, real_y + dy - 1

        if new_x < 0 or new_y < 0:
            raise Exception()
        if new_x != x or new_y != y:
             self.energy -= 1
        return (new_real_x, new_real_y), False

    #### Regla 4 ####
    def __condicion_para_caminar(self, P):
        return True
    def __accion_de_caminar(self, P):
        matrix = P[0]
        (x, y) = P[1]
        (real_x, real_y) = P[2]
        
        default_pos = positions_to_move = []
        for i, j in directions:
            if (x + i) in range(0, len(matrix)) and (y + j) in range(0, len(matrix[x + i])) and matrix[x + i][y + j] not in [Obstacle()]:                          # modificar para agregar obstaculos
                default_pos.append((real_x + i, real_y + j))
        if len(default_pos) == 0: return (x, y), False
        return (default_pos[random.randint(0, len(default_pos) - 1)], False)

        
        

        

class PredatorAgent(BrooksAgent):
    def __init__(self, digestion_time, max_energy, alpha, beta) -> None:
        self.prop = PredatorAgentPropierties(digestion_time, max_energy)
        self.eating = 0
        self.behaviors = self.prop._behaviors
        self.energy = max_energy

    def next(self, P):
        if self.eating == 1:
            self.energy = max(self.energy + Food().energy_ratio * self.prop.max_energy,
                                self.prop.max_energy)
        elif self.eating <= 0:
            self.energy -= 1
        
        return













class scaredPreyAgentPropierties:
    def __new__(cls, digestion_time, max_energy, alpha, beta):
        if not hasattr(cls, 'instance'):
            cls.instance = super(scaredPreyAgentPropierties, cls).__new__(cls)
            cls.digestion_time = digestion_time
            cls.max_energy = max_energy
            cls.alpha = alpha
            cls.beta = beta
            cls._behaviors = [
                #(cls.__condicion_para_esconderse, cls.__accion_de_esconderse),
                #(cls.__condicion_para_buscar_escondite, cls.__accion_de_buscar_escondite),
                (cls.__condicion_para_huir, cls.__accion_de_huir),
                (cls.__condicion_para_permanecer, cls.__accion_de_permanecer),
                (cls.__condicion_para_comer, cls.__accion_de_comer),
                (cls.__condicion_para_buscar_comida, cls.__accion_de_buscar_comida),
                (cls.__condicion_para_caminar, cls.__accion_de_caminar),
                
            ]
            cls.rand = random.Random()
        return cls.instance

    def manhathan_distance(i, j, o, p): return max(abs(i - o), abs(j - p))
    
    def __proximo_escondite(self, P):                                                           # P = matriz, pos
        (x, y) = P[1]
        min_distance = len(P[0]) + 1
        for i in range(len(P[0])):
            for j in range(len(P[0][i])):
                elem = P[0][i][j]
                distance_m =scaredPreyAgentPropierties.manhathan_distance(x, y, i, j)
                if elem == HidePlace() and min_distance > distance_m:
                    return True
        return False
    def __en_rango_escondite(self, P):
        matriz = P[0]
        escondites = []
        (x, y) = P[1]
        (real_x, real_y) = P[2]
        # for i, j in directions:
        #     if matriz[x + i][y + j] == HidePlace():
        #         escondites.append((real_x + i, real_y + j))
        # # return escondites[random.randint(0, len(escondites) - 1)]
        # if len(escondites) > 0:
        #     self.future_position = escondites[random.randint(0, len(escondites) - 1)]
        # return len(escondites) != 0
        if HidePlace() in matriz[x][y]  :
            self.future_position = (real_x, real_y)
            return True
        return False
                

    def __proximo_depredador(self, P):
        (x, y) = P[1]
        closer_predator = (-1, -1)
        min_distance = len(P[0]) + 1
        for i in range(len(P[0])):
            for j in range(len(P[0][i])):
                elem = P[0][i][j]
                distance_m =scaredPreyAgentPropierties.manhathan_distance(x, y, i, j)
                if PredatorAgent in elem and min_distance > distance_m:
                    return True
        # if closer_predator == (-1, -1): return -1
        # return closer_predator
        return False
    def __proximo_comida(self, P):
        (x, y) = P[1]
        closer_food = (-1, -1)
        min_distance = len(P[0]) + 1
        for i in range(len(P[0])):
            for j in range(len(P[0][i])):
                elem = P[0][i][j]
                distance_m =scaredPreyAgentPropierties.manhathan_distance(x, y, i, j)
                if Food() in elem and min_distance > distance_m:
                    return True
        # if closer_food == (-1, -1): return -1
        # return closer_food
        return False
    def __en_rango_comida(self, P):
        matriz = P[0]
        foods = []
        (x, y) = P[1]
        (real_x, real_y) = P[2]
        # for i, j in directions:
        #     if (x + i) not in range(0, len(matriz)) or (y + j) not in range(0, len(matriz[x + i])) or matriz[x + i][y + j] in [Obstacle()]: continue            # modificar para agregar tipos de obstaculos
        #     if matriz[x + i][y + j] == Food():
        #         foods.append((real_x + i, real_y + j))
        # if len(foods) > 0:
        #     self.future_position = foods[random.randint(0, len(foods) - 1)]
        # return len(foods) != 0
        if Food() in matriz[x][y]  :
            self.future_position = (real_x, real_y)
            return True
        return False

        
    #### Regla 1 ####
    def __condicion_para_esconderse(self, P):
        return self.prop.__en_rango_escondite(P) and self.prop.__proximo_depredador(P) and not self.hidden
    def __accion_de_esconderse(self, P):
        self.hidden = True
        return self.future_position, False
    #### Regla 2 ####
    def __condicion_para_buscar_escondite(self, P):
        return self.prop.__proximo_escondite(P) and self.prop.__proximo_depredador(P) and not self.hidden
    def __accion_de_buscar_escondite(self, P):
        hideplace_found = lambda ent: ent == HidePlace()
        predator_found = lambda ent: ent == type(PredatorAgent)
        obstacle_found = lambda ent : ent in [Obstacle()]                                                     # modificar lista para agragar obstaculos
        (x, y) = P[1]
        (real_x, real_y) = P[2]

        hideplaces_matrix = AStar(P[0], x, y, len(P[0]), hideplace_found, obstacle_found)
        hideplaces_abundance_matrix = transform(hideplaces_matrix, xpansion_distance= 1)

        predators_matrix = AStar(P[0], x, y, len(P[0]), predator_found, obstacle_found)
        predators_abundance_matrix = transform(predators_matrix, xpansion_distance= 1)

        pounded_matrix = [[0, 0, 0], 
                                        [0, 0, 0], 
                                        [0, 0, 0]] 
        maxi = 0
        for i, j in positions:
            maxi = max(maxi, max(hideplaces_abundance_matrix[i][j], predators_abundance_matrix[i][j]))
        for i, j in positions:
            pounded_matrix[i][j] = hideplaces_matrix[i][j] if hideplaces_matrix[i][j] <= 0 else maxi + hideplaces_abundance_matrix[i][j] - predators_abundance_matrix[i][j]

        dx, dy = betterMove(pounded_matrix, rnd=True)
        (new_x, new_y) = x + dx -1, y + dy -1
        (new_real_x, new_real_y) = real_x + dx -1, real_y + dy -1
        if new_x < 0 or new_y < 0:
            raise Exception()
        if new_x != x or new_y != y:
            self.energy -= 1
        return (new_real_x, new_real_y), False
        
        

    #### Regla 3 ####
    def __condicion_para_huir(self, P):
        # print(self.prop.__proximo_depredador(P))
        return self.prop.__proximo_depredador(P) and not self.hidden
    def __accion_de_huir(self, P):
        #print('HUIRRRRRRRRR')
        predator_found = lambda ent: ent in [PredatorAgent]
        obstacle_found = lambda ent : ent in [Obstacle()]                                                     # modificar lista para agragar obstaculos
        (x, y) = P[1]
        (real_x, real_y) = P[2]

        predators_matrix = AStar(P[0], x, y, len(P[0]), predator_found, obstacle_found)
        predators_abundance_matrix = transform(predators_matrix, xpansion_distance= 1)

        pounded_matrix = [[0, 0, 0], 
                                        [0, 0, 0], 
                                        [0, 0, 0]] 
        # maxi = max([max(array) for array in predators_abundance_matrix])
        
        maxi = max(max([array for array in predators_abundance_matrix]))
        
        for i, j in positions:
            pounded_matrix[i][j] = maxi - predators_abundance_matrix[i][j] if predators_abundance_matrix[i][j] >= 0 else -1
                

        dx, dy = betterMove(pounded_matrix, rnd=True)
        print('HUIR', dx-1, dy-1)
        print(predators_matrix)
        new_x, new_y = x + dx -1, y + dy -1
        (new_real_x, new_real_y) = real_x + dx -1, real_y + dy -1
        if new_x < 0 or new_y < 0:
            raise Exception()
        if new_x != x or new_y != y:
            self.energy -= 1

        return (new_real_x, new_real_y), False

    #### Regla 4 ####
    def __condicion_para_permanecer(self, P):
        return self.eating > 0 or ((self.prop.max_energy * self.prop.beta) > self.energy and self.rand()) or (self.prop.__proximo_depredador(P) and self.hidden)
    def __accion_de_permanecer(self, P):
        return P[2], False

    #### Regla 5 ####
    def __condicion_para_comer(self, P):
        return self.prop.__en_rango_comida(P) and (self.prop.max_energy * self.prop.alpha) > self.energy
    def __accion_de_comer(self, P):
        self.eating = self.prop.digestion_time
        return P[2], True

    #### Regla 6 ####
    def __condicion_para_buscar_comida(self, P):
        return self.prop.__proximo_comida(P) and (self.prop.max_energy * self.prop.beta) > self.energy
    def __accion_de_buscar_comida(self, P):
        food_found = lambda ent: ent == Food()
        obstacle_foun = lambda ent: ent in [Obstacle()]                                                     # modificar lista para agragar obstaculos
        (x, y) = P[1]
        (real_x, real_y) = P[2]
        
        matrix = AStar(P[0], x, y, len(P[0]), food_found, obstacle_foun)
        abundance_matrix = transform(matrix)
        (dx, dy) = betterMove(abundance_matrix)

        (new_x, new_y) = x + dx -1, y + dy -1
        (new_real_x, new_real_y) = real_x + dx - 1, real_y + dy - 1

        if new_x < 0 or new_y < 0:
            raise Exception()
        if new_x != x or new_y != y:
             self.energy -= 1
        return (new_real_x, new_real_y), False

    #### Regla 7 ####
    def __condicion_para_caminar(self, P):
        return True
    def __accion_de_caminar(self, P):
        matrix = P[0]
        (x, y) = P[1]
        (real_x, real_y) = P[2]
        
        default_pos = positions_to_move = []
        for i, j in directions:
            if (x + i) in range(0, len(matrix)) and (y + j) in range(0, len(matrix[x + i])) and matrix[x + i][y + j] not in [Obstacle()]:                          # modificar para agregar obstaculos
                default_pos.append((real_x + i, real_y + j))
        if len(default_pos) == 0: return (x, y), False
        return (default_pos[random.randint(0, len(default_pos) - 1)], False)

        
        
        
        
        
        
        
        
        


class scaredPreyAgent(BrooksAgent):
    
    def __init__(self, digestion_time, max_energy, alpha, beta) -> None:
        self.prop = scaredPreyAgentPropierties(digestion_time, max_energy, alpha, beta)
        self.behaviors = self.prop._behaviors
        self.eating = 0
        self.energy = max_energy
        self.hidden = False
        self.rand = lambda: random.randint(0, 100) > 70
        self.future_position = (-1, -1)
    
    def next(self, P):
        if self.eating > 1:
            self.eating -= 1
        if self.eating == 1:
            self.energy = min(self.energy + Food().energy_ratio * self.prop.max_energy,
                                self.prop.max_energy)
            self.eating -= 1
        elif self.eating <= 0:
            self.energy -= 1
        self.next_predators.clear()
        return
    
    def __repr__(self) -> str:
        return 'a'


