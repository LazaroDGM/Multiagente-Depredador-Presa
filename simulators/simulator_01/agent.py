from operator import index
from Algorithms.AStar import AStar
from Algorithms.transform import betterMove, transform
from simulator.agent import Agent, BrooksAgent
import random
from math import inf
from simulators.simulator_01.entities import Food

class AnimalAgentPropierties:
    def __new__(cls, digestion_time, max_energy):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AnimalAgentPropierties, cls).__new__(cls)
            cls.digestion_time = digestion_time
            cls.max_energy = max_energy
            cls._behaviors = [
                (cls.__condition_keep_eating, cls.__keep_eating),
                (cls.__condition_eat, cls.__eat),
                (cls.__condition_mov, cls.__mov)
            ]
            cls.rand = random.Random()
        return cls.instance
    
    #### Regla 1 ####
    def __condition_keep_eating(self, P):
        return self.eating > 0
    def __keep_eating(self, P):
        self.eating -= 1
        return (P[2][0], P[2][1]), False

    #### Regla 2 ####
    def __condition_eat(self, P):
        vision = P[0]
        set_obj = vision[P[1][0], P[1][1]]
        for obj in set_obj:
            if type(obj) is Food:
                return True
        return False
    def __eat(self, P):
        self.eating = self.prop.digestion_time        
        return (P[2][0], P[2][1]), True
    
    #### Regla 3 ####
    def __condition_mov(self, P):
        return True
    def __mov(self, P):
        
        r,c = P[1]
        min_r = max(0, r-1)
        min_c = max(0, c-1)
        max_r = min(P[0].shape[0], r+1+1)
        max_c = min(P[0].shape[1], c+1+1)
        extract = P[0][min_r:max_r, min_c:max_c]
        r = min(1,r)
        c = min(1,c)
        positions = []
        for i in range(extract.shape[0]):
            for j in range(extract.shape[1]):
                positions.append((i,j))
        indx = random.randint(0, len(positions)-1)
        mov = positions[indx]
        if mov != (r,c):
            self.energy -= 1
        self.energy -= 1
        new_position = (P[2][0] + mov[0] - r, P[2][1] + mov[1] - c)
        if new_position[0] < 0 or new_position[1] < 0:
            raise Exception()
        return (new_position, False)
        
        


class AnimalAgent(BrooksAgent):

    def __init__(self, digestion_time, max_energy) -> None:
        self.prop = AnimalAgentPropierties(digestion_time, max_energy)
        self.eating = 0
        self.behaviors = self.prop._behaviors
        self.energy = max_energy
    
    def next(self, P):
        if self.eating == 1:
            self.energy = max(self.energy + Food().energy_ratio * self.prop.max_energy,
                                self.prop.max_energy)
        elif self.eating == 0:
            self.energy -= 1
        return
    
    def __repr__(self) -> str:
        return 'a'

    

