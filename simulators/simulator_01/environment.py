from simulator.environment import Environment
from simulators.simulator_01.agent import AnimalAgent
from simulators.simulator_01.entities import Food
import random
import numpy as np

class EnvironmentSimulator01(Environment):

    def __init__(self,
                 shape_map,
                 initial_count_animals,
                 breeding_period,
                 breeding_ratio,
                 vision_radius,
                 food_generation_period,
                 food_ratio,
                 energy_ratio,
                 digestion_time,
                 max_energy,
                ) -> None:
        super().__init__()
        self.shape_map = shape_map
        self.initial_count_animals = initial_count_animals
        self.breeding_period = breeding_period
        self.breeding_ratio = breeding_ratio
        self.vision_radius = vision_radius
        self.food_generation_period = food_generation_period
        self.food_ratio = food_ratio
        self.energy_ratio = energy_ratio
        self.digestion_time = digestion_time
        self.max_energy = max_energy

        self._see_functions[type(AnimalAgent)] = EnvironmentSimulator01.seeAgent
        self._rand = random.Random()
        self.obstacles = [AnimalAgent, type(AnimalAgent)]

        def isObstacle(s):
            for item in s:
                if type(item) in self.obstacles:
                    return True
            return False
        self.isObstacle = isObstacle

        ### Variables Observables ###
        self.count_agents = 0
        self.count_foods = 0
        self.agents = {}
        
        f = Food(energy_ratio)
        self._init_map()
        self._gen_food()
        

    def seeAgent(agent: AnimalAgent):
        raise NotImplementedError()

    def _init_map(self):
        fil, col =  self.shape_map
        self._map = np.array([set() for i in range(0, fil*col)])
        self._map.resize((fil, col))
        self._map[0][0].add(AnimalAgent(self.digestion_time, self.max_energy))
    
    def _gen_food(self):
        '''
        Genera aleatoriamente uniforme, en lugares sin obstaculos, comida.
        La cantidad de comida generada es en proporcion al mapa.
        '''
        reshaped = self._map.reshape(self._map.size)
        emptys = np.array(list(filter(lambda s: not self.isObstacle(s), reshaped)))
        emptys.resize(emptys.size)
        selection = self._rand.choices(emptys,k = min(int(self.food_ratio * self.shape_map[0]*self.shape_map[1]), emptys.size))
        food = Food(self.energy_ratio)
        for s in selection:
            s.add(food)
        self.count_foods += len(selection)

    def _remove_food(self):
        '''
        Elimina toda la comida del mapa
        '''
        food = Food()        
        for row_array in self._map:
            for _set in row_array:
                if food in _set:
                    _set.remove(food)
        self.count_foods = 0

    def _gen_animals(self):
        '''
        Genera nuevos agentes animales en posiciones libres de obstaculos,
        aleatoriamente de forma uniforme
        '''        
        emptys = []
        for i in range(self._map.shape[0]):
            for j in range(self._map.shape[1]):
                if not self.isObstacle(self._map[i][j]):
                    emptys.append((i,j))
        emptys = np.array(emptys)
        emptys.resize(emptys.size)
        selection = self._rand.choices(emptys,k = min(int(self.breeding_ratio * self.count_agents), emptys.size))
        for r, c in selection:
            a = AnimalAgent(self.digestion_time, self.max_energy)
            self._map[r][c].add(a)
            self.agents[a] = (r, c)
        self.count_agents += len(selection)

    def _removes_agent(self):

        for agent, (r,c) in self.agents.items():
            if agent.energy <= 0:
                self._map[r][c].remove(agent)
                self.agents.pop(agent)
                self.count_agents -=1
    


