import random
import numpy as np
from heapq import heapify, heappop, heappush

class FoodMemory:
    def __init__(self, weight = 20, forget_tick = 10):
        self.slots = [[], [], [], []]
        self.weights = [int(weight * 0.3),
                                int(weight * 0.3),
                                int(weight * 0.2),
                                int(weight * 0.1)]
        self.len = sum(self.weights)
        self.memories_location = lambda ratio: 0 if ratio >0.25 else 1 if ratio > 0.2 else 2 if ratio > 0.1 else 3
        self.forget_tick = forget_tick
        self.current_tick = 0
        self.rnd = random.Random()

        self.max_abundance = 4 * self.weights[0] + 3 * self.weights[1] + 2* self.weights[2] + self.weights[3]

    def Tick(self):
        self.current_tick += 1
        if self.current_tick % (self.forget_tick *8) == 0:
            self.current_tick = 0
            self.Forget(3)
        elif self.current_tick % (self.forget_tick *4) == 0:
            self.Forget(2)
        elif self.current_tick % (self.forget_tick *4) == 0:
            self.Forget(1)
        else: 
            self.Forget(0)
        return
            

    def Remember(self, pos, food_ratio):
        if food_ratio == 0.0:
            return
        location = self.memories_location(food_ratio)
        current_slot = self.slots[location]

        try:
            ind = current_slot.index(pos)
            current_slot.pop(ind)
            current_slot.append(pos)
        except:
            if len(current_slot) < self.weights[location]: 
                current_slot.append(pos)
                return
            choix = abs(int(self.rnd.normalvariate(0, 4.5)))
            for i in range(len(current_slot)):
                manhathan_distance = max(abs(current_slot[i][0] - pos[0]), abs(current_slot[i][1] - pos[1]))
                if manhathan_distance <= choix:
                    # current_slot[i: len(current_slot) - 1] = current_slot[i: len(current_slot)]                                                       # estas dos lineas pueden ahorrar la re-copia del array
                    # current_slot[-1] = pos                                                                                                                                  # al hacerle pop()
                    current_slot.pop(i)
                    current_slot.append(pos)
                    return
            current_slot.append(pos)
            self.slots[location].pop(0)
            
        
        
        
    def Forget(self, slot_to_forget):
        if len(self.slots[slot_to_forget]) <= 0:
            return
        self.slots[slot_to_forget].pop(0)


    def PrintMemo(self):
        for i in range(4):
            for item in self.slots[i]:
                print(item)
            print()

    def __len__(self):
        return self.len
    def count(self):
        return sum(len(slot) for slot in self.slots)

    def gen_abundance(self):
        abundance = 4 * len(self.slots[0]) + 3 * len(self.slots[1]) +  2 * len(self.slots[2]) + len(self.slots[3])
        return abundance/self.max_abundance

    def suggestion(self, extra_positions=[], remove_position = None):
        l = [] + extra_positions
        l = l + (self.slots[0] * 8)
        l = l + (self.slots[1] * 5)
        l = l + (self.slots[2] * 3)
        l = l + (self.slots[3] * 2)

        if remove_position is not None:
            exist = True
            while exist:
                try:
                    l.remove(remove_position)
                except:
                    exist = False        
        return random.choice(l)

# memo = FoodMemory()

## test 1
# for i in range(10):
#     item = memo.rnd.random()
#     memo.Remember((1, 1), item)

## test 2    
# memo.Remember((0, 0), 0.96)
# memo.Remember((0, 1), 0.76)
# memo.Remember((0, 2), 0.76)
# memo.Remember((1, 0), 0.76)
# memo.Remember((1, 1), 0.76)
# memo.Remember((1, 2), 0.76)
# memo.Remember((2, 0), 0.76)
# memo.Remember((2, 1), 0.76)

# memo.PrintMemo()

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
        while len(self.times) > 0 and self.times[0] == self.time:
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
        while len(self.times) > 0 and self.times[0] == self.time:
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