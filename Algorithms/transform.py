from random import randint

positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

def transform(matrix, xpansion_distance = 3, high_rank_value = 4):                         # se asume aqui que la matriz es de 3x3
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

    for i, j in positions:
        for k in range(len(matrix[i][j])):
            # test_elem = f'M[{i}][{j}][{k}]:   {matrix[i][j][k]}   ->    {int((maxi + mini - matrix[i][j][k]) * (high_rank_value / maxi))}'
            elem = matrix[i][j][k] = int((maxi + mini - matrix[i][j][k]) * (high_rank_value / maxi))
            final_matrix[i][j] += elem
    for i, j in positions:
        for o, p in positions:
            if o == i and j == p: continue
            for elem in matrix[o][p]:
                _distance = distance(i, j, o, p)
                if _distance <= xpansion_distance and elem - _distance > 0:
                    final_matrix[i][j] += elem - _distance

    return final_matrix

def transform_again(vision_abundance_matrix, xpansion_distance = 3, high_rank_value = 4):
    final_matrix = [[[], [], []],
                            [[], [], []],
                            [[], [], []]]
    for i, j in positions:
        final_matrix[i][j].append(vision_abundance_matrix[i][j])
    return transform(final_matrix, xpansion_distance, high_rank_value)

def betterMove(vision_abundance_matrix, rnd = True):
    maxs = [(i, max(array)) for i, array in  enumerate(vision_abundance_matrix)]
    maxx = 0
    positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    sameImportance = []
    for i, (j, temp_max) in enumerate(maxs):
        if temp_max > maxx:
            maaxx = temp_max
            sameImportance.clear()
            sameImportance.append((i, j))
        elif temp_max == maxx:
            sameImportance.append((i, j))
    
    if rnd:                                             return sameImportance[randint(0, len(sameImportance))]  
    elif len(sameImportance) ==1:       return sameImportance[0] 
    else:                                               return betterMove(transform_again(vision_abundance_matrix))
