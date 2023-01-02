def HillClimbing(initil_vector, function, generate_neighbours, fitness_eval, max_count_solution, minimize):
    '''
    Metaheuristica HillClimbing para hallar maximos locales de funciones.

    `initil_vector`: Vector inicial del Dominio
    `function`: Funcion de caja negra que se quiere optimizar
    `generate_neighbours`: Funcion generadora de vecinos validos en el
    dominio de `function`
    `fitness_eval`: Funcion heuristica evaluadora de vectores solucion
    `max_count_solution`: Cantidad maxima de escalada que se desea hacer
    `minimize`: `True` si desea minimizar `function`. Por defecto `False`, para maximizar

    IMPORTANTE: Tenga en cuenta que la complejidad temporal de este algoritmo sera:

    `|neighbours| * max_count_solution * O(function)`

    por lo que se aconseja mantener un equilibrio entre la cantidad de escaladas con
    la cantidad de vecinos generados
    '''

    if minimize:
        fitness_eval = lambda x : - fitness_eval(x)

    actual_vector = initil_vector    
    actual_fitness = fitness_eval(function(actual_vector))
    count = 0

    global_fitness = {}
    global_fitness[actual_vector] = actual_fitness

    while count < max_count_solution:
        neighbours = generate_neighbours(actual_vector)
        
        max_fitness = actual_fitness
        max_neighbour = None
        for neig in neighbours:
            fitness = global_fitness.get(neig, None)
            if fitness is None:
                result = function(neig)
                fitness = fitness_eval(result)
                global_fitness[neig] = fitness
                if fitness > max_fitness:
                    max_fitness = fitness
                    max_neighbour = neig
        if max_fitness < actual_fitness:
            break
        actual_fitness = max_fitness
        actual_vector = max_neighbour
    
    return actual_vector, actual_fitness, count

