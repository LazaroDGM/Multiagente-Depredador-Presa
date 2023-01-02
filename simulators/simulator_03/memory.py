import random
import numpy as np
import heapq

class FoodMemory:
    def __init__(self, weight = 10):
        self.slots = [[], [], [], []]
    def Tick(self):
        raise NotImplementedError()
    def Remember(self):
        raise NotImplementedError()
