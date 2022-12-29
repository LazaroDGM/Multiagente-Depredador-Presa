from random import randint
from Algorithms.AStar import AStar

positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

def transform(matrix, xpansion_distance = 2, re_transforming = False, high_rank_value = 4):                         # se asume aqui que la matriz es de 3x3
    maxi = 0
    mini = 10000000
    final_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    temp_matrix = [[[], [], []], [[], [], []], [[], [], []]]
    def distance(x, y, i, j): 
        factor = (2 if (x == i == 1  or y == j == 1) else 0)
        return abs(x - i) + abs(y - j)  +  factor
    for i, j in positions:
        temp_max = maxi
        temp_min = mini
        obstacle_found = False
        for elem in matrix[i][j]:
            if elem == -1: 
                temp_matrix[i][j].append(-1)
                final_matrix[i][j] = -1
                obstacle_found = True
                break
            temp_max = max(temp_max, elem)
            temp_min = min(temp_min, elem)
        if not obstacle_found:
            maxi = max(maxi, temp_max)
            mini = min(mini, temp_min)
    if maxi == 0: return final_matrix
    for i, j in positions:
        if final_matrix[i][j] == -1: continue
        for k in range(len(matrix[i][j])):
            test_elem = f'M[{i}][{j}][{k}]:   {matrix[i][j][k]}   ->    {int((maxi + mini - matrix[i][j][k]) * (high_rank_value / maxi))}'
            elem = matrix[i][j][k] if re_transforming else int((maxi + mini - matrix[i][j][k]) * (high_rank_value / maxi))
            temp_matrix[i][j].append(elem)
            final_matrix[i][j] = elem
    print("matriz con pesos reales: ")
    PrintMatrix(temp_matrix)

    for i, j in positions:
        if final_matrix[i][j] == -1: continue
        for o, p in positions:
            if final_matrix[o][p] == -1: continue
            if o == i and j == p: continue
            for elem in temp_matrix[o][p]:
                _distance = distance(i, j, o, p)
                if _distance <= xpansion_distance and elem - _distance > 0:
                    final_matrix[i][j] += elem - _distance
    return final_matrix

def transform_again(abundance_matrix, xpansion_distance = 2, high_rank_value = 4):
    final_matrix = [[[], [], []],
                            [[], [], []],
                            [[], [], []]]
    for i, j in positions:
        final_matrix[i][j].append(abundance_matrix[i][j])
    return transform(final_matrix, xpansion_distance, re_transforming=True, high_rank_value=high_rank_value)

def betterMove(abundance_matrix, xpansion_distance = 2, high_rank_value = 4, rnd = True):
    maxx = 0
    sameImportance = []
    for i, j in positions:
        if abundance_matrix[i][j] > maxx:
            maxx = abundance_matrix[i][j]
            sameImportance.clear()
            sameImportance.append((i, j))
        elif abundance_matrix[i][j] == maxx:
            sameImportance.append((i, j))


    if rnd:                                             return sameImportance[randint(0, len(sameImportance) - 1)]  
    elif len(sameImportance) ==1:       return sameImportance[0] 
    else:                                               return betterMove(transform_again(abundance_matrix, xpansion_distance, high_rank_value))

def PrintMatrix(matrix)        :
    for array in matrix:
        print("[ ", end="")
        for item in array: 
            print(item, end="")
        print(' ]')



matrix = [[[0], [-1], [0], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [1]],
                [[0], [0], [0], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [0]],
                [[0], [0], [1], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [0]]]
P = (matrix, (0, 0))
food_found = lambda ent: ent == 1
obstacle_found = lambda ent : ent == -1                                                     # modificar lista para agragar obstaculos
x, y = P[1]

matrix2 = AStar(P[0], x, y, len(P[0]), food_found, obstacle_found)
print('AStar: ')
PrintMatrix(matrix2)

abundance_matrix = transform(matrix2)
print('after transform: ')
PrintMatrix(abundance_matrix)

print('better move:  ')
print(betterMove(abundance_matrix, rnd=False))
