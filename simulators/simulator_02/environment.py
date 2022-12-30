from simulator.environment import EnvironmentTwoAgents
from simulator.entities import Food
from simulators.simulator_02.agent import PreyAgent, PredatorAgent
from simulator.agent import Agent
import random
import numpy as np

PREDATOR = 0
PREY = 1

class SpecialParametersPrey():
    def __init__(self, alpha, beta) -> None:
        self.alpha = alpha
        self.beta = beta

class EnvironmentSimulator02(EnvironmentTwoAgents):

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
                 special_parameters,
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

        self.special_parameters = [
            None,
            SpecialParametersPrey(special_parameters[PREY])
        ]

        self._see_functions = {
            PreyAgent: self.seePrey(PREY),
            PredatorAgent: self.seePrey(PREDATOR)
        }

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

    