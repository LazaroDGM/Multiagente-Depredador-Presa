from simulators.simulator_03.environment import Environment03, Plant, Obstacle
from simulators.simulator_03.simulator import Simulator02
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

sim = Simulator02(Environment03)
sim.StartSimulation(
    tick= 0.05,
    stop_steps=1000,
    map= map,
    food_generation_period=40,
    plant_radius= 3,
    food_ratio= 0.1,
    initial_count_prey=0,
    initial_count_predator=0,
    params_prey=[],
    params_predator=[]
)
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