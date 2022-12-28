def transform(matrix, xpansion_distance = 3, high_rank_value = 4):                         # se asume aqui que la matriz es de 3x3
    maxi = 0
    mini = 10000000
    positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
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
    print(final_matrix)
    for i, j in positions:
        for o, p in positions:
            if o == i and j == p: continue
            for elem in matrix[o][p]:
                _distance = distance(i, j, o, p)
                if _distance <= xpansion_distance and elem - _distance > 0:
                    final_matrix[i][j] += elem - _distance

    return final_matrix