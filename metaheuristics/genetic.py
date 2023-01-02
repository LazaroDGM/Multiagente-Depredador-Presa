import random
from heapq import heapify, heappop, heappush

neighboor_distance = 0.02

def generate_neightboors(point, index = 0):
    if index == len(point) - 1: 
        x = point[index] - neighboor_distance
        if x >= 0 and x <= 1: yield [x]
        yield [point[index]]
        z = point[index] + neighboor_distance
        if z >= 0 and z <= 1: yield [z]
        return
    for lista in generate_neightboors(point, index+1):
        x = point[index] - neighboor_distance
        if x >= 0 and x <= 1: yield [x] + lista
        yield [point[index]] + lista
        z = point[index] + neighboor_distance
        if z >= 0 and z <= 1: yield [z] + lista
        
            

def generate_population(weight = 30, vector_length = 4):
    rnd = random.Random()
    for i in range(weight):
        solution = []
        for j in range(vector_length):
            solution.append(1 - rnd.uniform(0, 1))
        yield solution
    return

def merch(vectors):
    middle = int(len(vectors)/2)
    sing_middle = (len(vectors[0]) / 2)
    
    new_solutions = []
    for i in range(middle):
        for j in range(middle, len(vectors)):
            vector1 = vectors[i]
            vector2 = vectors[j]
            
            merch = [vector1[k] if k < sing_middle else vector2[k] for k in range(len(vector1))]
            new_solutions.append(merch)
    return new_solutions

def geneticeval(parameters_number: int, fitness_function, function, simulation_times :int = 30):
    heapp = []
    for sol in generate_population(vector_length=parameters_number):
        heappush(heapp, (-fitness_function(function(sol)), sol))
    better_solutions = []
    for i in range(simulation_times):
        for a in range(10):
            better_solutions.append(heappop(heapp))
        heapp.clear()
        heapp += [(-fitness_function(solution), solution) for solution in merch([sol[1] for sol in better_solutions])]
        heapify(heapp)
    return [item[1] for item in heapp][:10]
        

        

    
# count = 0
# for solution in generate_neightboors([0.4, 0.23, 0.1, 0, 0]):
#     print(solution)
#     count+= 1
# print(f'count: {count}')


# def vector_sum(vector):
#     sum = 0
#     for item in vector:
#         sum += item
#     return sum
# arrai = geneticeval(parameters_number=4, fitness_function=lambda vector: vector_sum(vector))
# print(len(arrai))
# print(sum(arrai[0]))
# print(max(map(lambda array: sum(array), arrai)))

