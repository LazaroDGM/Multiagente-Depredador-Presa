from operator import index
from Algorithms.AStar import AStar
from Algorithms.transform import transform
from simulator.agent import Agent, BrooksAgent
import random
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
        return (0,0), False

    #### Regla 2 ####
    def __condition_eat(self, P):
        vision = P[0]
        obj = vision[P[1][0], P[1][1]]
        return obj is Food
    def __eat(self, P):
        self.eating = self.prop.digestion_time        
        return (0,0), True
    
    #### Regla 3 ####
    def __condition_mov(self, P):
        return True
    def __mov(self, P):
        self.energy -= 1

        food_found = lambda ent: ent == Food()
        obstacle_found = lambda ent : ent in [type(Agent)]                                                     # modificar lista para agragar obstaculos
        x, y = P[1]

        matrix = AStar(P[0], x, y, len(P[0]), food_found, obstacle_found)
        abundance_matrix = transform(matrix)
        
        maxs = [(i, max(array)) for i, array in  enumerate(abundance_matrix)]
        maxx = 0
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        sameImportance = []
        for i, (j, temp_max) in enumerate(maxs):
            if temp_max > maxx:
                maaxx = temp_max
                sameImportance.clear()
                sameImportance.append((i, j))
            elif temp_max == maxx:
                sameImportance.append((i, j))
        
        return (sameImportance[random.randint(0, 7)], False)


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

    

