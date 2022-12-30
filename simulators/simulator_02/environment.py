from simulator.environment import EnvironmentTwoAgents
from simulator.entities import Food
from simulator.agent import Agent
import random
import numpy as np

PREDATOR = 0
PREY = 1

class SpecialParametersPrey():
    def __init__(self, alpha, beta) -> None:
        self.alpha = alpha
        self.beta = beta

