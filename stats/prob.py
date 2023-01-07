import random
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg

def den_D1(l, alpha, sigma, gamma):
    if l >= alpha:
        raise Exception('"l" debe ser menor que "alpha"')
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

def generator_D1(l, alpha, sigma, gamma, rand_var=None):
    if l >= alpha:
        raise Exception('"l" debe ser menor que "alpha"')
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

    if rand_var is None:
        rand_var = random.Random()
    def generator():        
        y = rand_var.uniform(l, L)
        x = rand_var.uniform(0,1)
        while x >= f(y) / (c * g):
            x = rand_var.uniform(0,1)
            y = rand_var.uniform(l, L)            
        return y
    return generator

#rand = random.Random()
#gen = generator_D1(l=1, alpha= 6, sigma=2, gamma= 0)
#d = den_D1(l=1, alpha= 6, sigma=2, gamma= 0)
##l = [gen() for i in range(0, 1000)]
##plt.hist(l,30)
#plt.plot(np.arange(0,9,0.01), [d(i) for i in np.arange(0,9,0.01)])
#plt.show()
#exit()