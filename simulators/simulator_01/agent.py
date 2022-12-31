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
        food_found = lambda ent: ent == Food()
        obstacle_found = lambda ent : ent in []                                                     # modificar lista para agragar obstaculos
        x, y = P[1]

        matrix = AStar(P[0], x, y, len(P[0]), food_found, obstacle_found)
        abundance_matrix = transform(matrix)
        dx, dy = betterMove(abundance_matrix, rnd=False)
        new_x, new_y = x + dx -1, y + dy -1
        if new_x < 0 or new_y < 0:
            raise Exception()
        if new_x != x or new_y != y:
             self.energy -= 1
        return (new_x,new_y), False
        
        


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
        elif self.eating <= 0:
            self.energy -= 1
        return
    
    def __repr__(self) -> str:
        return 'a'

    

