import random
import numpy as np
import heapq

class FoodMemory:
    def __init__(self, weight = 10):
        self.slots = [[], [], [], []]
    def Tick(self):
        raise NotImplementedError()
    def Remember(self, pos, food_ratio):
        raise NotImplementedError()



################################# write below ###########################################

class PreyMemory:
    def __init__(self, wait_time) -> None:
        self.preys = []
        self.times = []
        self.time = 0
        self.wait_time = wait_time

    def __len__(self):
        return len(self.preys)
    
    def Tick(self):
        self.time += 1
        if len(self.times) > 0:
            while self.times[0] == self.time:
                self.preys.pop(0)
                self.times.pop(0)
    
    def Remember(self, prey):
        try:
            index = self.preys.index(prey)
            self.preys.pop(index)
            self.times.pop(index)
            self.preys.append(prey)
            self.times.append(self.time + self.wait_time)
        except:            
            self.preys.append(prey)
            self.times.append(self.time + self.wait_time)


class PredatorMemory:
    def __init__(self, wait_time) -> None:
        self.predators = []
        self.times = []
        self.time = 0
        self.wait_time = wait_time

    def __len__(self):
        return len(self.predators)
    
    def Tick(self):
        self.time += 1
        if len(self.times) > 0:
            while self.times[0] == self.time:
                self.predators.pop(0)
                self.times.pop(0)
    
    def Remember(self, predator):
        try:
            index = self.predators.index(predator)
            self.predators.pop(index)
            self.times.pop(index)
            self.predators.append(predator)
            self.times.append(self.time + self.wait_time)
        except:            
            self.predators.append(predator)
            self.times.append(self.time + self.wait_time)