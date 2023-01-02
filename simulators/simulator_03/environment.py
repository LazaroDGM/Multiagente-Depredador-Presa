from simulator.environment import Environment
from simulators.simulator_03.entities import Food, Obstacle, Plant, Burrow, Floor
import numpy as np
import random

VOID = 0
FOOD = 1
OBSTACLE = -1
HIDING_PLACE = -2

class Environment03(Environment):

    def __init__(self,
        map,
        plant_radius,
        food_ratio,
        food_generation_period,
        initial_count_prey,
        initial_count_predator,
        params_prey,
        params_predator,
    ) -> None:
        self.plant_radius = plant_radius
        self.food_ratio = food_ratio
        self.food_generation_period = food_generation_period
        self.initial_count_prey = initial_count_prey
        self.initial_count_predator = initial_count_predator

        self.food = Food()
        self.obstacle = Obstacle()
        self._rand = random.Random()

        # Diccionario de plantas-(posicion, proxima reproduccion)
        self.plants = {}

        # Diccionario de presas-posicion
        self.preys = {}

        # Diccionario de depredadores-posicion
        self.predator = {}

        # Variables contadoras
        self.cicle = 0 # Tiempo actual del Medio
        self.count_foods = 0
        
        self._init_map(map)

    
    def _init_map(self, map):
        row, col =  map.shape
        self._map = np.array([set() for i in range(0, row*col)])
        self._map.resize((row, col))
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                if isinstance(map[i,j], (Obstacle, Plant)):
                    self._map[i][j] = map[i,j]
                    if isinstance(map[i][j], Plant):
                        self.plants[(i,j)] = 1
                elif map[i][j] == 'BURROW':
                    self._map[i][j] = Burrow()
                elif map[i][j] is None or map[i][j] == 'FLOOR':
                    self._map[i][j] = Floor()
        self.shape_map = self._map.shape
    
    def free_for_food(self, s):
        '''
        Funcion para saber si una casilla esta libre para generar una comida
        '''
        if isinstance(s, Floor):
            return not s.hasFood()
        return False

    def _gen_food(self, count, matrix):
        '''
        Genera aleatoriamente uniforme, en lugares sin obstaculos, comida.
        La cantidad de comida generada es en proporcion al mapa.
        '''
        reshaped = matrix.reshape(matrix.size)
        #food = Food()

        emptys = np.array(list(filter(self.free_for_food, reshaped)))
        emptys.resize(emptys.size)
        #selection = self._rand.sample(emptys,k = min(, emptys.size))

        # int(self.food_ratio * self.shape_map[0]*self.shape_map[1])
        idx = np.random.choice(emptys.shape[0], min(count, emptys.size), replace=False)
        selection = emptys[idx]
        for s in selection:            
            s.AddFood()
        self.count_foods += len(selection)

    def gen_food(self):
        # Generacion de Comida
        for (r, c), cicle_food in self.plants.items():
            if self.cicle == cicle_food:
                #self._remove_food()                
                min_r = max(0, r-self.plant_radius)
                min_c = max(0, c-self.plant_radius)
                max_r = min(self._map.shape[0], r+self.plant_radius+1)
                max_c = min(self._map.shape[1], c+self.plant_radius+1)
                extract = self._map[min_r:max_r, min_c:max_c]

                self._gen_food(int(self.food_ratio*extract.size), extract)
                cicle_food = int(self._rand.expovariate(1/self.food_generation_period)) + self.cicle + 1
                print('Nueva produccion de comida en: ', cicle_food)
                self.plants[(r,c)] = cicle_food

    

    def next_step(self):
        self.cicle += 1
        print(self.count_foods)
        self.gen_food()

    def outputs(self):
        return None