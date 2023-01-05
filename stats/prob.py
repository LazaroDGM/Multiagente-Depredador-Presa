import random
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg

def den_D1(l, alpha, sigma, gamma):
    if sigma > alpha:
        raise Exception('"sigma" debe ser menor que "l"')
    if not (l <= alpha <= alpha + l):
        raise Exception('"alpha" debe ser un valor entre "l" y "sigma + l"')
    if gamma > 1 or gamma < 0:
        raise Exception('"gamma" debe ser un valor en el intervalo [0,1]')
    
    L = alpha + sigma
    A = np.array(
        [
            [alpha - l, L- alpha, alpha**2 + (l**2 + L**2)/2],
            [-1, 1, -2*alpha],
            [1-gamma, 0, l-gamma*alpha]
        ]
    )
    b = np.array(
        [
            1,
            0,
            0
        ]
    )
    sol = linalg.solve(A, b)

    def f(x):
        if x < l:
            return 0
        if l <= x <= alpha:
            return x * sol[2] + sol[0]
        if alpha < x <= L:
            return - x * sol[2] + sol[1]
        return 0
    
    return f

def generator_D1(l, alpha, sigma, gamma):
    if sigma > alpha:
        raise Exception('"sigma" debe ser menor que "l"')
    if gamma > 1 or gamma < 0:
        raise Exception('"gamma" debe ser un valor en el intervalo [0,1]')
    
    L = alpha + sigma
    A = np.array(
        [
            [alpha - l, L- alpha, alpha**2 + (l**2 + L**2)/2],
            [-1, 1, -2*alpha],
            [1-gamma, 0, l-gamma*alpha]
        ]
    )
    b = np.array(
        [
            1,
            0,
            0
        ]
    )
    sol = linalg.solve(A, b)

    def f(x):
        if x < l:
            return 0
        if l <= x <= alpha:
            return x * sol[2] + sol[0]
        if alpha < x <= L:
            return - x * sol[2] + sol[1]
        return 0

    g = 1/(L - l)
    c = (L-l)* (sol[2]*alpha + sol[0])

    rand = random.Random()
    def generator():        
        y = rand.uniform(l, L)
        x = rand.uniform(0,1)
        while x >= f(y) / (c * g):
            x = rand.uniform(0,1)
            y = rand.uniform(l, L)
            print('iter')    
        return y
    return generator