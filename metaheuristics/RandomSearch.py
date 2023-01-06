from math import inf
import heapq

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)


def RandomSearch(function, random_generation, fitness_eval, max_count_solution, minimize=False):
    '''
    Metaheuristica RandomSearch para optimizacion de funciones. Se generan varios
    vectores del dominio y se comprueba cual es el mejor

    `function`: Funcion que se desea optimizar
    `random_generation`: Funcion que genera vectores aleatorios
    `fitness_eval`: Funcion heuristica que calcula cuan bueno es un vector solucion
    `max_count_solution`: Cantidad maxima de vectores aleatorios del Dominio generados.
    `minimize`: `True` si desea minimizar `function`. Por defecto `False`, para maximizar
    '''

    if minimize:
        fitness_eval = lambda x : - fitness_eval(x)

    best_solutions = [PrioritizedItem(-inf, None)] * 25
    
    for _ in range(max_count_solution):
        rand_vector = random_generation()
        result = function(rand_vector)
        fitness = fitness_eval(*result)
        heapq.heappushpop(best_solutions,PrioritizedItem(fitness, rand_vector))
        print(fitness, rand_vector)
    
    return heapq.nlargest(25,best_solutions)
