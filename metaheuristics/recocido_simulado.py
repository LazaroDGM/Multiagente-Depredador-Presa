import random

def generate_population(weight = 30, vector_length = 4):
    rnd = random.Random()
    for i in range(weight):
        solution = []
        for j in range(vector_length):
            solution.append(1 - rnd.uniform(0, 1))
        yield solution
    return

def recocido_simulado_eval(parameters_number: int, fitness_function, function, simulation_times :int = 30, temperature:int = 25):
    generate_population(vector_length=parameters_number)
    
    