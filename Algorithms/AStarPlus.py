from heapq import heapify, heappop, heappush
import math


positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

def AStarPlus(numpy_array, x, y, vision, found, obstacle, stop_with = 3):
    len_x = len(numpy_array)
    len_y = len(numpy_array[0])
    matrix = [[ [], [], [] ], 
                    [ [], [], [] ],
                    [ [], [], [] ]]
    heap = []
    heapify(heap)
    visited_cells = set()
    
    heappush(heap, (0, (0, (0, ([(x, y)], (x, y))))))                       # 1- costo, 2- direccion de partida del camino, 3- dist. manhathan, 4- camino o trace hsat el objetivo, 5- posicion correspondiente
    visited_cells.add((x, y))

    min_d_way = math.inf
    the_way = []
    founded = 0
    
    while len(heap) != 0:
        min_tuple = heappop(heap)
        current_cost = min_tuple[0] - min_tuple[1][1][0]
        current_direction = min_tuple[1][0]
        current_way = min_tuple[1][1][1][0]
        for j in range(-1, 2):
            _x_pos = min_tuple[1][1][1][1][0] + j
            if _x_pos < 0 or _x_pos >= len_x or abs(_x_pos - x) > vision: continue                                                  # out of range test
            for k in range(-1, 2):
                _y_pos = min_tuple[1][1][1][1][1] + k
                if _y_pos < 0 or _y_pos >= len_y  or  (j == 0 and k == 0)  or  abs(_x_pos - x) > vision: continue       # out of range test
                cell = _x_pos, _y_pos
                if cell in visited_cells: continue                                                                                                             # cell already visited
                visited_cells.add((_x_pos, _y_pos))
                manhathan_distance = max(abs(_x_pos - x), abs(_y_pos - y))
                
                if obstacle(numpy_array[_x_pos][_y_pos]): continue
                if found(_x_pos, _y_pos):
                    if current_direction == 0:
                        matrix[j + 1][k + 1].append(1)
                        founded+= 1
                        the_way = current_way + [cell]
                    else: 
                        matrix[int((current_direction - 1) / 3)][(current_direction - 1) % 3].append(current_cost + 1)
                        founded+= 1
                        if min_d_way > current_cost + 1:
                            min_d_way = current_cost + 1
                            the_way = current_way + [cell]
                next_direction = (j+1)*3 + k+2       if          current_direction == 0        else            current_direction
                heappush(heap, (manhathan_distance + current_cost + 1, (next_direction, (manhathan_distance, (current_way + [cell], cell)))))
        if founded >= stop_with:
            break

        
    # Adding obstacles
    for i, j in positions:
        if x + i - 1 not in range(0, len(numpy_array)) or y + j - 1 not in range(0, len(numpy_array[x + i - 1])): 
            matrix[i][j] = [-1]
            continue
        #print(f'position analized: {(x + i - 1, y + j - 1)}')
        if obstacle(numpy_array[x + i - 1][y + j - 1]):
            matrix[i][j] = [-1]
    return matrix, the_way
