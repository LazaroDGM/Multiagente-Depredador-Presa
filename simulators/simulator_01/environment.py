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

        self._see_functions[AnimalAgent] = EnvironmentSimulator01.seeAgent
        self._rand = random.Random()
        self.obstacles = [AnimalAgent, type(AnimalAgent)]

        def isObstacle(s):
            for item in s:
                if type(item) in self.obstacles:
                    return True
            return False
        self.isObstacle = isObstacle

        ### Estados internos del Medio ###
        self.cicle = 0
        self.cicle_food = int(self._rand.expovariate(1/self.food_generation_period)) + 1
        self.cicle_breeding = int(self._rand.expovariate(1/self.breeding_period)) + 1        

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
        row_position_vision = min(self.vision_radius, r)
        col_position_vision = min(self.vision_radius, c)
        if row_position_vision < 0 or col_position_vision < 0:
            raise Exception()
        return vision, (row_position_vision, col_position_vision), (r,c)


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

        emptys = np.array(list(filter(lambda s: food not in s, reshaped)))
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
        selection = emptys[idx]
        #selection = self._rand.sample(emptys, min(count, emptys.size))
        for r, c in selection:
            if r < 0 or c < 0:
                raise Exception()
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
    

    def next_step(self):
        # Generacion de Comida
        if self.cicle == self.cicle_food:
            self._remove_food()
            self._gen_food(int(self.food_ratio * self.shape_map[0]*self.shape_map[1]))
            self.cicle_food = int(self._rand.expovariate(1/self.food_generation_period)) + self.cicle + 1
            print('Nueva produccion de comida en: ', self.cicle_food)

        # Reproduccion de la Poblacion
        if self.cicle == self.cicle_breeding:
            if self.count_agents > 0:
                self._gen_animals(int(self.breeding_ratio * self.count_agents)+1)
                self.cicle_breeding = int(self._rand.expovariate(1/self.breeding_period)) + self.cicle + 1
                print('Nueva reproduccion animal en : ', self.cicle_breeding)
            
        
        # Eliminar agentes muertos
        deleted = []
        for agent, position in self.agents.items():
            if agent.energy <= 0:
                self._map[position[0], position[1]].remove(agent)
                deleted.append(agent)
        for agent in deleted:
            self.agents.pop(agent)
        self.count_agents -= len(deleted)
                

        actions = []
        for agent in self.agents.keys():            
            P = self.see(agent)
            agent.next(P)
            Ac = agent.action(P)
            actions.append((agent, Ac))

        self.transform(actions)
        self.cicle += 1

    def transform(self, actions):
        food = Food()        

        ### Movimiento de los agentes ###
        new_positions = {}
        for agent, action in actions:
            position, eat_food = action
            if position[0] < 0 or position[1] < 0:
                raise Exception()
            
            if eat_food == True:
                sett = self._map[position[0], position[1]]
                sett.remove(food)
                self.count_foods -= 1
                new_positions[position] = agent
            else:
                mov_posible = True
                for item in self._map[position[0]][position[1]]:
                    if type(item) in [AnimalAgent]:
                        mov_posible = False
                        break
                if not mov_posible:
                    continue
                elif new_positions.get(position, None) is None:
                    new_positions[position] = agent
                elif position == self.agents[agent]:                
                    new_positions[position] = agent

        for position, agent in new_positions.items():
            old_position = self.agents[agent]
            if old_position != position:
                self._map[old_position[0]][old_position[1]].remove(agent)
                self._map[position[0]][position[1]].add(agent)
                self.agents[agent] = position
            
    def outputs(self):
        return self.count_agents, self.count_foods
