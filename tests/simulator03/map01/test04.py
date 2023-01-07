from simulators.simulator_03.environment import Environment03, Plant, Obstacle
from simulators.simulator_03.simulator import Simulator03_2D
from simulators.simulator_03.agent_predator import ParamsPredator
from simulators.simulator_03.agent_prey import ParamsPrey
from simulators.simulator_03.simulator import Simulator03
import numpy as np
import matplotlib.pyplot as plt
import stats.stats as st
import statistics
import seaborn as sb

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
            [N,N,N,O,B,B,B,B,B,N,N,N,N,N,O,N,N,N,N,N,N,N,O,O,N,N,N,N],
            [N,N,N,O,B,B,B,B,B,N,N,N,N,N,O,N,N,N,N,N,N,N,O,N,N,N,N,N],
            [N,N,N,N,N,O,O,O,O,N,N,N,N,N,O,N,N,O,O,O,N,N,N,N,N,N,N,N],
            [N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,O,N,O,O,N,N,N,P,N,N,N],
            [N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,N,N,N,N,N,O,O,N,N,N,N,N,N],
            [N,N,N,N,N,N,N,N,N,N,O,O,O,N,N,N,N,N,N,N,N,O,N,N,N,N,N,N],
            [N,N,N,N,N,N,N,N,N,O,O,N,N,N,N,P,N,N,N,O,O,O,N,N,N,N,N,N],
            [N,N,P,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,N,N,N,N],
            [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,O,O,O,B,B,O,N,N],
            [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,B,B,B,B,B,B,B,O,N,N],
            [N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,O,O,B,B,B,B,B,O,N,N],
        ]
    )

    sim = Simulator03()
    simulations= sim.StartManySimulationsThreading(        
        stop_steps=30000,
        map= map,
        food_generation_period=70,
        plant_radius= 3,
        food_ratio= 0.175,
        initial_count_prey=3,
        initial_count_predator=1,
        params_prey= ParamsPrey(
            digestion_time=3,
            max_energy= 150,
            velocity= 1,
            vision_radius= 3,
            lost_energy_wait=0.5,
            lost_energy_wait_burrow=0.2,
            lost_energy_walk=1,
            lost_energy_walk_burrow=0.4,
            memory_predator_wait_time=50,
            memory_prey_wait_time=150,
            breeding_point=100,
            food_energy_ratio=0.3,
            forget_tick= 30,
            weight_memory_food= 20,
            gestate_again_time= 0,
            gestate_time= 10,        
            reproduction_ratio=2,
            gamma=0.0,
            bold=0.8,
            lamb= 2,
            beta=6,
            sigma=4
        ),
        params_predator= ParamsPredator(
            digestion_time=5,
            max_energy= 300,
            velocity= 0,
            vision_radius= 5,
            lost_energy_wait=0.5,
            lost_energy_walk=1,
            memory_predator_wait_time=300,
            memory_prey_wait_time=100,
            breeding_point=250,
            food_energy_ratio=0.8,
            forget_tick= 30,
            weight_memory_food= 20,
            gestate_again_time= 100,
            gestate_time= 10,
            reproduction_ratio=1,
            bold=0.8,
            beta=9,
            sigma=2
        )
    )

    counts = [np.array(simulation[0]).T for simulation in simulations]
    counts_preys = [count[0] for count in counts]
    counts_predators = [count[1] for count in counts]
    counts_food = [count[2] for count in counts]

    mean_life_preys = [np.mean(simulation[1]) for simulation in simulations]
    mean_life_predators = [np.mean(simulation[2]) for simulation in simulations]

    median_life_preys = [np.median(simulation[1]) for simulation in simulations]
    median_life_predators = [np.median(simulation[2]) for simulation in simulations]

    mode_life_preys = [statistics.mode(simulation[1]) if len(simulation[1]) > 0 else np.nan for simulation in simulations]
    mode_life_predators = [statistics.mode(simulation[2]) if len(simulation[2]) > 0 else np.nan for simulation in simulations]    

    heatmap_preys = np.array([simulation[3] for simulation in simulations])
    heatmap_predators = np.array([simulation[4] for simulation in simulations])
    
    with open('results/simulator03/map01/04.npz', 'wb') as ft:
        np.savez(ft,
            counts_preys= counts_preys,
            counts_predators = counts_predators,
            counts_food = counts_food,
            mean_life_preys= mean_life_preys,
            mean_life_predators = mean_life_predators,
            median_life_preys = median_life_preys,
            median_life_predators= median_life_predators,
            mode_life_preys= mode_life_preys,
            mode_life_predators= mode_life_predators,
            heatmap_preys = heatmap_preys,
            heatmap_predators = heatmap_predators
        )

def view_results():
    with open('results/simulator03/map01/04.npz', 'rb') as ft:
        obj = np.load(ft)
        
        #print(results.shape)
        for result in obj['counts_food']:
            plt.plot(range(result.shape[0]), result, linewidth=0.8)        
        mean = obj['counts_food'].mean(axis=0)
        std = obj['counts_food'].std(axis=0)
        plt.plot(range(len(mean)), mean, '-.', color= 'black', linewidth= 4)
        plt.plot(range(len(mean)), mean + std, '--', color= 'black', linewidth= 2)
        plt.plot(range(len(mean)), mean - std, '--', color= 'black', linewidth= 2)
        plt.show()

        for result in obj['counts_preys']:
            plt.plot(range(result.shape[0]), result, linewidth=0.8)        
        mean = obj['counts_preys'].mean(axis=0)
        std = obj['counts_preys'].std(axis=0)
        plt.plot(range(len(mean)), mean, '-.', color= 'black', linewidth= 4)
        plt.plot(range(len(mean)), mean + std, '--', color= 'black', linewidth= 2)
        plt.plot(range(len(mean)), mean - std, '--', color= 'black', linewidth= 2)
        plt.show()

        for result in obj['counts_predators']:
            plt.plot(range(result.shape[0]), result, linewidth=0.8)        
        mean = obj['counts_predators'].mean(axis=0)
        std = obj['counts_predators'].std(axis=0)
        plt.plot(range(len(mean)), mean, '-.', color= 'black', linewidth= 4)
        plt.plot(range(len(mean)), mean + std, '--', color= 'black', linewidth= 2)
        plt.plot(range(len(mean)), mean - std, '--', color= 'black', linewidth= 2)
        plt.show()        
        
        sb.heatmap(np.mean(obj['heatmap_preys'], axis=0))
        plt.show()  
        sb.heatmap(np.mean(obj['heatmap_predators'], axis=0))
        plt.show()         

        
