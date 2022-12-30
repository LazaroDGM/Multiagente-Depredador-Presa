from simulator.environment import EnvironmentManyAgents, EnvironmentSimulatorPreyPredator
from simulator.entities import Food
from simulator.agent import Agent
from simulators.simulator_02.agent import PreyAgent, PredatorAgent
import random
import numpy as np

PREDATOR = 0
PREY = 1

class SpecialParametersPrey():
    def __init__(self, alpha, beta) -> None:
        self.alpha = alpha
        self.beta = beta

class Environment02(EnvironmentSimulatorPreyPredator):

    def __init__(self, map, initial_count_animals, breeding_period, breeding_ratio, digestion_time, vision_radius, max_energy, food_generation_period, food_ratio, energy_ratio, special_parameters) -> None:
        super().__init__(map, initial_count_animals, breeding_period, breeding_ratio, digestion_time, vision_radius, max_energy, food_generation_period, food_ratio, energy_ratio, special_parameters, [PredatorAgent, PreyAgent])
    

