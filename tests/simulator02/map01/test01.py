from simulators.simulator_02.environment import Environment02
from simulator.entities import Obstacle
from simulator.simulator import Simulator
from simulators.simulator_02.simulator import Simulator02
import numpy as np
import matplotlib.pyplot as plt

def generate_result():
    o = set([Obstacle()])
    v = set()
    map = np.array(
        [
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            [v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v],#v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
            #[v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v],
        ]
    )


    sim = Simulator(Environment02)

    _, simulation = sim.StartManySimulations(
        count_simulations=2,
        stop_steps=2000,
        map= map,
        initial_count_animals= [2,5],
        breeding_period= [200,50],
        breeding_ratio= [0.3, 0.2],
        breeding_population= [0.75,0.7],
        vision_radius= [7,3],
        food_generation_period= 50,
        food_ratio= 0.1,
        energy_ratio= 1,
        digestion_time= [5,2],
        max_energy= [200, 100],
        special_parameters=[[0.3,0.4,1],[0.3,0.4,2]],
    )

    results = np.array(simulation)
    with open('results/simulator02/map01/01.npz', 'wb') as ft:
        np.savez(ft, results= results)

def view_results():
    with open('results/simulator02/map01/01.npz', 'rb') as ft:
        obj = np.load(ft)
        results = obj['results'].T

        plt.plot(range(results.shape[1]), results[0])
        plt.plot(range(results.shape[1]), results[1])
        plt.plot(range(results.shape[1]), results[2])
        plt.show()
