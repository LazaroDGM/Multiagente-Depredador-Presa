from simulators.simulator_03.environment import Environment03, Plant, Obstacle
from simulators.simulator_03.simulator import Simulator03
from simulators.simulator_03.agent_predator import ParamsPredator
from simulators.simulator_03.agent_prey import ParamsPrey
from simulator.simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt
import stats.stats as st

def generate_result():

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

    sim = Simulator(Environment03)
    simulation= sim.StartManySimulationsThreading(
        #count_simulations=32,
        stop_steps=30000,
        map= map,
        food_generation_period=100,
        plant_radius= 3,
        food_ratio= 0.1,
        initial_count_prey=3,
        initial_count_predator=0,
        params_prey= ParamsPrey(
            digestion_time=3,
            max_energy= 100,
            velocity= 2,
            vision_radius= 3,
            lost_energy_wait=0.5,
            lost_energy_wait_burrow=0.2,
            lost_energy_walk=1,
            lost_energy_walk_burrow=0.4,
            memory_predator_wait_time=50,
            memory_prey_wait_time=100,
            breeding_point=75,
            food_energy_ratio=0.5,
            forget_tick= 30,
            weight_memory_food= 20,
            gestate_again_time= 0,
            gestate_time= 10,
            max_life= 30000,
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
    #results = np.array(results).T

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

    results = np.array(simulation)
    with open('results/simulator03/map01/03.npz', 'wb') as ft:
        np.savez(ft, results= results)

def view_results():
    with open('results/simulator03/map01/03.npz', 'rb') as ft:
        obj = np.load(ft)
        results = obj['results']
        #print(results.shape)

        for result in results:
            plt.plot(range(result.shape[0]), results.T[0], linewidth=0.8)
        m = st.select_from_results(results, 0)
        mean = m.mean(axis=0)
        std = m.std(axis=0)
        plt.plot(range(result.shape[0]), mean, '-.', color= 'black', linewidth= 4)
        plt.plot(range(result.shape[0]), mean + std, '--', color= 'black', linewidth= 2)
        plt.plot(range(result.shape[0]), mean - std, '--', color= 'black', linewidth= 2)
        plt.show()

        for result in results:
            plt.plot(range(result.shape[0]), results.T[1], linewidth=0.8)
        m = st.select_from_results(results, 1)
        mean = m.mean(axis=0)
        std = m.std(axis=0)
        plt.plot(range(result.shape[0]), mean, '-.', color= 'black', linewidth= 4)
        plt.plot(range(result.shape[0]), mean + std, '--', color= 'black', linewidth= 2)
        plt.plot(range(result.shape[0]), mean - std, '--', color= 'black', linewidth= 2)
        plt.show()
        
        print(m.shape)
