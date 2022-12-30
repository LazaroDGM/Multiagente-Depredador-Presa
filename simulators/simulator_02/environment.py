from simulator.environment import EnvironmentFood, EnvironmentManyAgents
from simulator.entities import Food
from simulator.agent import Agent
from simulators.simulator_02.agent import PreyAgent, PredatorAgent
import random
import numpy as np

PREDATOR = 0
PREY = 1

class Environment02(EnvironmentManyAgents):

    def __init__(self, map, initial_count_animals, breeding_period, breeding_ratio, digestion_time, vision_radius, max_energy, food_generation_period, food_ratio, energy_ratio, special_parameters) -> None:
        super().__init__(map, initial_count_animals, breeding_period, breeding_ratio, digestion_time, vision_radius, max_energy, food_generation_period, food_ratio, energy_ratio, special_parameters, [PredatorAgent, PreyAgent])

    def outputs(self):
        return len(self.agents_groups[1]), self.count_foods
    
    def transform(self, actions):
        food = self.food       

        ### Movimiento de los agentes ###
        new_positions = {}
        for type_agent, agent, action in actions:
            position, eat_food = action
            if position[0] < 0 or position[1] < 0:
                raise Exception()                    
            
            if eat_food == True:
                sett = self._map[position[0], position[1]]
                sett.remove(food)
                self.count_foods -= 1
                new_positions[position] = (type_agent, agent)
            else:
                mov_posible = True
                for item in self._map[position[0]][position[1]]:
                    if item is agent:
                        new_positions[position] = (type_agent, agent)
                        mov_posible = False
                        break
                    if isinstance(item, (Agent, type(self.obstacle))):
                        mov_posible = False
                        break
                if not mov_posible:
                    continue
                elif new_positions.get(position, None) is None:
                    new_positions[position] = (type_agent, agent)
                elif position == self.agents_groups[type_agent][agent]:
                    new_positions[position] = (type_agent, agent)

        for position, (type_agent, agent) in new_positions.items():
            old_position = self.agents_groups[type_agent][agent]
            if old_position != position:
                self._map[old_position[0]][old_position[1]].remove(agent)
                self._map[position[0]][position[1]].add(agent)
                self.agents_groups[type_agent][agent] = position
