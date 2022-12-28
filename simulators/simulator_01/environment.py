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
        
        self._gen_food(int(self.food_ratio * self.shape_map[0]*self.shape_map[1]))
        

    def seeAgent(self, agent: AnimalAgent):
        r, c = self.agents[agent]
        min_r = max(0, r-self.vision_radius)
        min_c = max(0, c-self.vision_radius)
        max_r = min(self._map.shape[0], r+self.vision_radius+1)
        max_c = min(self._map.shape[1], c+self.vision_radius+1)
        extract = self._map[min_r:max_r, min_c:max_c]

        vision = np.array([set() for _ in range(0, extract.size)])
        vision.resize(extract.shape)
        for i in range(extract.shape[0]):
            for j in range(extract.shape[1]):
                for ent in extract[i][j]:
                    if type(ent) is AnimalAgent:
                        vision[i][j].add(AnimalAgent)
                    else:
                        vision[i][j].add(ent)
        return vision, (r,c)


    def _init_map(self):
        row, col =  self.shape_map
        self._map = np.array([set() for i in range(0, row*col)])
        self._map.resize((row, col))
        self._gen_animals(self.initial_count_animals)
    
    def _gen_food(self, count):
        '''
        Genera aleatoriamente uniforme, en lugares sin obstaculos, comida.
        La cantidad de comida generada es en proporcion al mapa.
        '''
        reshaped = self._map.reshape(self._map.size)
        food = Food(self.energy_ratio)

        emptys = np.array(list(filter(lambda s: not self.isObstacle(s), reshaped)))
        emptys.resize(emptys.size)
        #selection = self._rand.sample(emptys,k = min(, emptys.size))

        # int(self.food_ratio * self.shape_map[0]*self.shape_map[1])
        idx = np.random.choice(emptys.shape[0], min(count, emptys.size), replace=False)
        selection = emptys[idx]
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

    def _gen_animals(self, count):
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
        #emptys.resize(emptys.size)
        #int(self.breeding_ratio * self.count_agents),
        idx = np.random.choice(emptys.shape[0], min(count, emptys.shape[0]), replace=False)
        selection = emptys[idx,:]
        #selection = self._rand.sample(emptys, min(count, emptys.size))
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
    


