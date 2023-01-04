from simulators.simulator_03.environment import Environment03, Plant, Obstacle
from simulators.simulator_03.simulator import Simulator03
from simulators.simulator_03.agent_predator import ParamsPredator
from simulators.simulator_03.agent_prey import ParamsPrey
import numpy as np

B = 'BURROW'
O = Obstacle()
P = Plant()
N = None

map = np.array(
    [
        [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N],
        [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N],
        [N,N,N,N,O,O,O,O,N,N,N,N,N,N,N,N,N,N,N,O,O,O,O,N,N,N,N,N],
        [N,N,N,N,O,B,B,O,O,N,N,N,N,N,N,O,O,O,P,O,N,N,N,N,N,N,N,N],
        [N,N,N,O,O,B,B,B,O,N,N,N,N,N,O,O,N,N,O,N,N,N,N,O,O,O,N,N],
        [N,N,N,O,B,B,B,B,O,N,N,N,N,N,O,N,N,N,N,N,N,N,O,O,N,N,N,N],
        [N,N,N,O,B,B,B,B,B,N,N,N,N,N,O,N,N,N,N,N,N,N,O,N,N,N,N,N],
        [N,N,N,N,O,O,O,O,O,N,N,N,N,N,O,N,N,O,O,O,N,N,N,N,N,N,N,N],
        [N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,O,N,O,O,N,N,N,P,N,N,N],
        [N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,N,N,N,N,N,O,O,N,N,N,N,N,N],
        [N,N,N,N,N,N,N,N,N,N,O,O,O,N,N,N,N,N,N,N,N,O,N,N,N,N,N,N],
        [N,N,N,N,N,N,N,N,N,O,O,N,N,N,N,P,N,N,N,O,O,O,N,N,N,N,N,N],
        [N,N,P,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,N,N,N,N],
        [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,O,O,O,B,O,N,N],
        [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,B,B,B,B,B,B,B,O,N,N],
        [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,B,B,B,B,B,O,N,N],
    ]
)

sim = Simulator03(Environment03)
_, results= sim.StartSimulation(
    tick= 0.0,
    stop_steps=10000,
    map= map,
    food_generation_period=70,
    plant_radius= 3,
    food_ratio= 0.1,
    initial_count_prey=1,
    initial_count_predator=0,
    params_prey= ParamsPrey(
        digestion_time=3,
        max_energy= 200,
        velocity= 0,
        vision_radius= 3,
        lost_energy_wait=0.5,
        lost_energy_wait_burrow=0.2,
        lost_energy_walk=1,
        lost_energy_walk_burrow=0.4,
        memory_predator_wait_time=50,
        memory_prey_wait_time=100,
        breeding_point=300,
        food_energy_ratio=0.2,
        forget_tick= 100,
        weight_memory_food= 20
    ),
    params_predator= ParamsPredator(
        digestion_time=5,
        max_energy= 200,
        velocity= 2,
        vision_radius= 6,
        lost_energy_wait=0.5,
        lost_energy_walk=1,
    )
)
results = np.array(results).T

print(results)
import matplotlib.pyplot as plt
plt.plot(range(len(results[0])), results[0])
plt.plot(range(len(results[0])), results[1])
plt.show()
#env = Environment03(
#    map= map,
#    food_generation_period=40,
#    plant_radius= 3,
#    food_ratio= 0.1,
#    initial_count_prey=0,
#    initial_count_predator=0,
#    params_prey=[],
#    params_predator=[]
#)

