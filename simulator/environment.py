import simulator.entities as ents
import numpy as np
import random
from simulator.agent import Agent

class Environment():
    '''
    Clase abstracta para modelar los Medios Ambientes.
    Un medio ambiente necesita una funcion de transformacion (`transform`) del Medio, y 
    las funciones perceptuales (`see`) segun los tipos de agentes que pueden convivir en el
    '''

    def __init__(self) -> None:
        self._see_functions = {}

    def see(self, agent):
        '''
        Evaluacion de la funcion perceptual para un agente especifico. Dado el agente (`agent`),
        y el tipo de agente (`type(agent)`), genera el conjunto de percepciones que
        ese agente capatar'a, segun la funcion perceptual de su tipo.

        `agent`: Instancia del agente

        `return`: Conjunto de percepciones captadas
        '''
        f =self._see_functions[type(agent)]
        return f(self, agent)

    def get_see_function(self, type_agent):
        '''
        Funcion perceptual para un agente especifico dado el tipo del agente (`type_agent`)

        `type_agent`: Tipo de agente

        `return`: Funcion perceptual
        '''
        return self._see_functions[type_agent]

    def transform(self, actions):
        '''
        Funcion de transformacion del Medio, que dado un conjunto de acciones, 
        cambia el estado del sistema
        '''
        raise NotImplementedError()

    def next_step(self):
        '''
        Ejecuta un paso de la simulacion dentro del Medio
        '''
        raise NotImplementedError()

    def outputs(self):
        '''
        Devuelve las observaciones realizadas hasta el momento de las variables observables.
        '''
        raise NotImplementedError()

class EnvironmentTwoAgents(Environment):

    def __init__(self,
                 map,          
                 food_generation_period,
                 food_ratio,
                 energy_ratio,
                 initial_count_animals,
                 breeding_period,
                 breeding_ratio,
                 digestion_time,
                 vision_radius,
                 max_energy,              
                ) -> None:
        super().__init__()
        self.shape_map = map.shape       
        self.food_generation_period = food_generation_period
        self.food_ratio = food_ratio
        self.energy_ratio = energy_ratio

        self.initial_count_animals = initial_count_animals
        self.breeding_period = breeding_period
        self.breeding_ratio = breeding_ratio
        self.digestion_time = digestion_time
        self.vision_radius = vision_radius
        self.max_energy = max_energy    
        
        self._rand = random.Random()

        ### Estados internos del Medio ###
        self.cicle = 0
        self.cicle_food = int(self._rand.expovariate(1/self.food_generation_period)) + 1        

        ### Variables Observables ###        
        self.count_foods = 0        
        
        self.food = ents.Food(energy_ratio)
        self.obstacle = ents.Obstacle()
        self.agents_groups = []
        self._init_map()
        self._gen_food(int(self.food_ratio * self.shape_map[0]*self.shape_map[1]))     
        
    def _init_map(self, map):
        row, col =  map.shape
        self._map = np.array([set() for i in range(0, row*col)])
        self._map.resize((row, col))
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                self._map[i][j].add(self.obstacle)

    def _gen_food(self, count):
        '''
        Genera aleatoriamente uniforme, en lugares sin obstaculos, comida.
        La cantidad de comida generada es en proporcion al mapa.
        '''
        reshaped = self._map.reshape(self._map.size)
        food = ents.Food(self.energy_ratio)

        emptys = np.array(list(filter(self.free_for_food, reshaped)))
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
        for row_array in self._map:
            for _set in row_array:
                if self.food in _set:
                    _set.remove(self.food)
        self.count_foods = 0

    def gen_food(self):
        # Generacion de Comida
        if self.cicle == self.cicle_food:
            self._remove_food()
            self._gen_food(int(self.food_ratio * self.shape_map[0]*self.shape_map[1]))
            self.cicle_food = int(self._rand.expovariate(1/self.food_generation_period)) + self.cicle + 1
            print('Nueva produccion de comida en: ', self.cicle_food)

    def next_step(self):        

        self.pre_transform()

        actions = []
        for agents in self.agents_groups:
            for agent in agents.keys():
                P = self.see(agent)
                agent.next(P)
                Ac = agent.action(P)
                actions.append((agent, Ac))

        self.transform(actions)
        self.cicle += 1
    
    def pre_transform(self):
        raise NotImplementedError()

class EnvironmentSimulatorPreyPredator(EnvironmentTwoAgents):

    def __init__(self,
                 map,
                 initial_count_animals,
                 breeding_period,
                 breeding_ratio,
                 digestion_time,
                 vision_radius,
                 max_energy,
                 food_generation_period,
                 food_ratio,
                 energy_ratio,                 
                ) -> None:
        super().__init__(
            map = map,
            initial_count_animals =initial_count_animals,
            breeding_period = breeding_period,
            breeding_ratio = breeding_ratio,
            digestion_time = digestion_time,
            vision_radius = vision_radius,
            max_energy = max_energy,
            food_generation_period = food_generation_period,
            food_ratio = food_ratio,
            energy_ratio = energy_ratio,
        )

        ### Estados internos del Medio ###
        self.cicle_breeding = [int(self._rand.expovariate(1/period)) + 1 for period in self.breeding_period]
        
        ### Variables Observables ###
        self.agents_groups = [{} for i in range(len(initial_count_animals))]
        self.count_foods = 0        
                
        self._init_map()        
        self._gen_food(int(self.food_ratio * self.shape_map[0]*self.shape_map[1]))
        

    def seePrey(self, agent_type):
        def seeAgent(self, agent):
            r, c = self.agents[agent]
            min_r = max(0, r-self.vision_radius[agent_type])
            min_c = max(0, c-self.vision_radius[agent_type])
            max_r = min(self._map.shape[0], r+self.vision_radius[agent_type]+1)
            max_c = min(self._map.shape[1], c+self.vision_radius[agent_type]+1)
            extract = self._map[min_r:max_r, min_c:max_c]

            vision = np.array([set() for _ in range(0, extract.size)])
            vision.resize(extract.shape)
            for i in range(extract.shape[0]):
                for j in range(extract.shape[1]):
                    for ent in extract[i][j]:
                        if ent.isinstance(Agent) :
                            vision[i][j].add(type(ent))
                        else:
                            vision[i][j].add(ent)
            row_position_vision = min(self.vision_radius[agent_type], r)
            col_position_vision = min(self.vision_radius[agent_type], c)
            if row_position_vision < 0 or col_position_vision < 0:
                raise Exception()
            return vision, (row_position_vision, col_position_vision), (r,c)
        return seeAgent

    