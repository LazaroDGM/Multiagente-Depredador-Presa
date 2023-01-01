from simulator.agent import BrooksAgent
import numpy as np
import random

VOID = 0
FOOD = 1
OBSTACLE = -1
HIDING_PLACE = -2


class PreyAgent(BrooksAgent):
    def __init__(self, digestion_time, max_energy, velocity) -> None:
        super().__init__()
        self.prop = PreyAgentPropierties(
            digestion_time= digestion_time,
            max_energy= max_energy,
            velocity= velocity
        )
        self.energy = max_energy
        self.eating = 0
    
    def set_global_map(self, map):
        self._map = np.copy(map)

    def next(self, P):
        return super().next(P)


class PreyAgentPropierties:
    def __new__(cls, digestion_time, max_energy, velocity):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PreyAgentPropierties, cls).__new__(cls)
            cls.digestion_time = digestion_time
            cls.max_energy = max_energy
            cls.velocity = velocity
            cls._behaviors = [
                
            ]
            cls.rand = random.Random()
        return cls.instance