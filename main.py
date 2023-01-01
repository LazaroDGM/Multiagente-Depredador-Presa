from simulators.simulator_02.environment import Environment02
from simulator.entities import Obstacle
from simulator.simulator import Simulator
from simulators.simulator_02.simulator import Simulator02
import numpy as np
#a1 = AnimalAgent(0.9)
#a2 = AnimalAgent(0.5)
#print(a1 == a2)
#print(a1.behaviors == a2.behaviors)
#print(a1.prop.digestion_time)
#print(a2.prop.digestion_time)
#
#a1.action([])

#print(any(filter(lambda x: x>5, c)))


#AnimalAgentPropierties()

o = set([Obstacle()])
v = set()
map = np.array(
    [
        [v,v,v,v,o,v,v,v],
        [v,v,v,v,v,v,v,v],
        [v,v,v,v,o,v,v,v],
        [o,o,o,o,o,v,v,v],
        [v,v,o,v,v,o,v,v],
        [v,v,v,v,v,o,o,v],
    ]
)

sim = Simulator02(Environment02)

simulation = sim.StartSimulation(
    tick=0.1,
    stop_steps=10000,
    map= map,
    initial_count_animals= [0,3],
    breeding_period= [500,70],
    breeding_ratio= [0.3, 0.2],
    vision_radius= [5,5],
    food_generation_period= 50,
    food_ratio= 0.125,
    energy_ratio= 1,
    digestion_time= [3,3],
    max_energy= [200, 200],
    special_parameters=[[0,0],[0.7,0.7]],
)

#sim = Simulator01(EnvironmentSimulator01)
#
#simulation = sim.StartSimulation(
#    tick=0.1,
#    stop_steps=1000,
#    shape_map= (5,5),
#    initial_count_animals= 2,
#    breeding_period= 500,
#    breeding_ratio= 0.3,
#    vision_radius= 5,
#    food_generation_period= 20,
#    food_ratio= 0.125,
#    energy_ratio= 1,
#    digestion_time= 3,
#    max_energy= 200
#)
#
results = np.array(simulation[1]).T
#
print(results)
import matplotlib.pyplot as plt
#
t = range(results.shape[1])
plt.plot(t, results[0])
plt.plot(t, results[1])
plt.show()




env = Environment02(
    map= map,
    initial_count_animals= [0,3],
    breeding_period= [500,200],
    breeding_ratio= [0.3, 0.2],
    vision_radius= [5,4],
    food_generation_period= 20,
    food_ratio= 0.125,
    energy_ratio= 1,
    digestion_time= [3,6],
    max_energy= [200, 500],
    special_parameters=[[0,0],[1,1]],
)

print(env.agents_groups)
print(env.breeding_period)
print(env.breeding_ratio)
print(env.cicle)
print(env.cicle_breeding)
print(env.cicle_food)
print(env.count_foods)
print(env.digestion_time)
print(env.energy_ratio)
print(env.food_generation_period)
print(env.food_ratio)
print(env.initial_count_animals)
print(env.max_energy)
print(env._see_functions)

print(env._map)
env.next_step()
print(env._map)
env.next_step()
print(env._map)
env.next_step()
print(env._map)

env.next_step()
print(env._map)
env.next_step()
print(env._map)
env.next_step()
print(env._map)

#print(e.seeAgent(list(e.agents.keys())[0]))