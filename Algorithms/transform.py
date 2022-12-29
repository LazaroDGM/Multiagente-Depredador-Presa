from random import randint
from AStar import AStar

positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

def transform(matrix, xpansion_distance = 3, re_transforming = False, high_rank_value = 4):                         # se asume aqui que la matriz es de 3x3
    maxi = 0
    mini = 10000000
    final_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    def distance(x, y, i, j): 
        factor = (2 if (x == i == 1  or y == j == 1) else 0)
        return abs(x - i) + abs(y - j)  +  factor
    for i, j in positions:
        for elem in matrix[i][j]:
            maxi = max(maxi, elem)
            mini = min(mini, elem)

    if maxi == 0: return final_matrix
    for i, j in positions:
        for k in range(len(matrix[i][j])):
            # test_elem = f'M[{i}][{j}][{k}]:   {matrix[i][j][k]}   ->    {int((maxi + mini - matrix[i][j][k]) * (high_rank_value / maxi))}'
            elem = matrix[i][j][k] if re_transforming else int((maxi + mini - matrix[i][j][k]) * (high_rank_value / maxi))
            final_matrix[i][j] += elem
    for i, j in positions:
        for o, p in positions:
            if o == i and j == p: continue
            for elem in matrix[o][p]:
                _distance = distance(i, j, o, p)
                if _distance <= xpansion_distance and elem - _distance > 0:
                    final_matrix[i][j] += elem - _distance

    return final_matrix

def transform_again(abundance_matrix, xpansion_distance = 3, high_rank_value = 4):
    final_matrix = [[[], [], []],
                            [[], [], []],
                            [[], [], []]]
    for i, j in positions:
        final_matrix[i][j].append(abundance_matrix[i][j])
    return transform(final_matrix, xpansion_distance, high_rank_value)

def betterMove(abundance_matrix, xpansion_distance = 3, high_rank_value = 4, rnd = True):
    maxs = []
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



# def PrintMatrix(matrix)        :
#     for array in matrix:
#         print("[ ", end="")
#         for item in array: 
#             print(item, end="")
#         print(' ]')



# matrix = [[[0], [0], [0], [0], [0], [0], [0]],
#                 [[0], [0], [0], [0], [1], [0], [0]],
#                 [[0], [0], [0], [0], [0], [0], [0]],
#                 [[0], [0], [0], [0], [0], [0], [0]],
#                 [[0], [0], [1], [0], [0], [0], [0]],
#                 [[0], [0], [0], [0], [0], [0], [0]],
#                 [[0], [0], [0], [0], [0], [0], [0]]]
# P = (matrix, (0, 0))
# food_found = lambda ent: ent == 1
# obstacle_found = lambda ent : ent == -1                                                     # modificar lista para agragar obstaculos
# x, y = P[1]

# matrix2 = AStar(P[0], x, y, len(P[0]), food_found, obstacle_found)
# print(f'AStar: {PrintMatrix(matrix2)}')
# abundance_matrix = transform(matrix2)
# print(f'after transform: {PrintMatrix(abundance_matrix)}')
# print(betterMove(abundance_matrix, rnd=False))