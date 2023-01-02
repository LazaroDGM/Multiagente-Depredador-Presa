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
        self.memories_location = lambda ratio: 0 if ratio >0.6 else 1 if ratio > 0.4 else 2 if ratio > 0.2 else 3
        self.forget_tick = forget_tick
        self.current_tick = 0
        self.rnd = random.Random()

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
        location = self.memories_location(food_ratio)
        current_slot = self.slots[location]
        if len(current_slot) < self.weights[location]: 
            current_slot.append(pos)
            return

        try:
            ind = current_slot.index(pos)
            current_slot.pop(ind)
            current_slot.append(pos)
        except:
            choix = abs(int(self.rnd.normalvariate(0, 2.5)))
            for i in range(len(current_slot)):
                manhathan_distance = max(abs(current_slot[i][0] - pos[0]), abs(current_slot[i][1] - pos[1]))
                if choix < manhathan_distance:
                    # current_slot[i: len(current_slot) - 1] = current_slot[i: len(current_slot)]                                                       # estas dos lineas pueden ahorrar la re-copia del array
                    # current_slot[-1] = pos                                                                                                                                  # al hacerle pop()
                    current_slot.pop(i)
                    current_slot.append(pos)
                    return
            current_slot.append(pos)
            self.slots[location].pop(0)
            
        
        
        
    def Forget(self, slot_to_forget):
        self.slots[slot_to_forget].pop(0)


    def PrintMemo(self):
        for i in range(4):
            for item in self.slots[i]:
                print(item)
            print()

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
