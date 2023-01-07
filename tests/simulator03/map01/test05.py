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
from metaheuristics.RandomSearch import RandomSearch
import random

rand = random.Random()
def random_generation():
    alpha = round(rand.uniform(2,7),2)
    gamma = round(rand.uniform(0,1),2)
    lamb = round(rand.uniform(0,2),2)
    beta_prey = round(rand.uniform(1,20),1)
    beta_predator = round(rand.uniform(1,20),2)
    sigma_prey = round(rand.uniform(1,10),2)
    sigma_predator = round(rand.uniform(1,10),2)
    bold_prey = round(rand.uniform(0,1),2)
    bold_predator = round(rand.uniform(0,1),2)

    return (alpha, gamma, lamb, beta_prey, beta_predator, sigma_prey, sigma_predator, bold_prey, bold_predator)

def function(vector):

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

    sim = Simulator03()
    simulations= sim.StartManySimulationsThreading(        
        stop_steps=30000,
        map= map,
        food_generation_period=70,
        plant_radius= 3,
        food_ratio= 0.125,
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
            reproduction_ratio=vector[0],
            gamma=vector[1],
            bold=vector[7],
            lamb= vector[2],
            beta=vector[3],
            sigma=vector[5]
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
            bold=vector[8],
            beta=vector[4],
            sigma=vector[6]
        )
    )

    counts = [np.array(simulation[0]).T for simulation in simulations]
    counts_preys = np.array([count[0] for count in counts])
    counts_predators = np.array([count[1] for count in counts])
    #counts_food = [count[2] for count in counts]

    mean_life_preys = [np.mean(simulation[1]) for simulation in simulations]
    mean_life_predators = [np.mean(simulation[2]) for simulation in simulations]

    #median_life_preys = [np.median(simulation[1]) for simulation in simulations]
    #median_life_predators = [np.median(simulation[2]) for simulation in simulations]

    #mode_life_preys = [statistics.mode(simulation[1]) if len(simulation[1]) > 0 else np.nan for simulation in simulations]
    #mode_life_predators = [statistics.mode(simulation[2]) if len(simulation[2]) > 0 else np.nan for simulation in simulations]    

    #heatmap_preys = np.array([simulation[3] for simulation in simulations])
    #heatmap_predators = np.array([simulation[4] for simulation in simulations])
    
    #with open('results/simulator03/map01/04.npz', 'wb') as ft:
    #    np.savez(ft,
    #        counts_preys= counts_preys,
    #        counts_predators = counts_predators,
    #        counts_food = counts_food,
    #        mean_life_preys= mean_life_preys,
    #        mean_life_predators = mean_life_predators,
    #        median_life_preys = median_life_preys,
    #        median_life_predators= median_life_predators,
    #        mode_life_preys= mode_life_preys,
    #        mode_life_predators= mode_life_predators,
    #        heatmap_preys = heatmap_preys,
    #        heatmap_predators = heatmap_predators
    #    )

    return counts_preys, counts_predators, mean_life_preys, mean_life_predators

def fitness_eval(counts_preys, counts_predators, mean_life_preys, mean_life_predators):
    max_time = np.full(shape=counts_preys.shape[0], fill_value=-1)
    for i in range(counts_preys.shape[0]):
        for t in range(counts_preys[i].shape[0]):
            if counts_preys[i][t] == 0 or counts_predators[i][t] == 0:
                max_time[i] = t
                break
        if max_time[i] == -1:
            max_time[i] = counts_preys[i].shape[0]
    return max_time.mean()


def search():
    res = RandomSearch(
        function=function,
        random_generation=random_generation,
        fitness_eval=fitness_eval,
        max_count_solution=100,
        minimize=False
    )
    for r in res:
        print(r)