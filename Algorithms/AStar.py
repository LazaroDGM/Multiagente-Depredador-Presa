from heapq import heapify, heappop, heappush

# def AStar(numpy_array, x, y, vision, found, obstacle):
#     len_x = len(numpy_array)
#     len_y = len(numpy_array[0])
#     matrix = [[ [], [], [] ], 
#                     [ [], [], [] ],
#                     [ [], [], [] ]]
#     heap = []
#     heapify(heap)
#     visited_cells = set()
    
#     heappush(heap, (0, (0, (0, ([], (x, y))))))                       # 1- costo, 2- direccion de partida del camino, 3- dist. manhathan, 4- trace o camino hasta el momento 5- posicion correspondiente
#     visited_cells.add((x, y))

    
#     while len(heap) != 0:
#         min_tuple = heappop(heap)
#         current_cost = min_tuple[0] - min_tuple[1][1][0]
#         current_direction = min_tuple[1][0]
#         for j in range(-1, 2):
#             pass
#             _x_pos = min_tuple[1][1][1][1][0] + j
#             if _x_pos < 0 or _x_pos >= len_x or abs(_x_pos - x) > vision: continue                                                  # out of range test
#             for k in range(-1, 2):
#                 _y_pos = min_tuple[1][1][1][1][1] + k
#                 if _y_pos < 0 or _y_pos >= len_y  or  (j == 0 and k == 0)  or  abs(_x_pos - x) > vision: continue       # out of range test
#                 cell = _x_pos, _y_pos
#                 if cell in visited_cells: continue                                                                                                             # cell already visited
#                 visited_cells.add((_x_pos, _y_pos))
#                 manhathan_distance = max(abs(_x_pos - x), abs(_y_pos - y))
                
#                 for agent in numpy_array[_x_pos][_y_pos]:
#                     if found(agent):
#                         print(f'camino a {cell}: {min_tuple[1][1][1][0]}')
#                         if current_direction == 0:
#                             matrix[j + 1][k + 1].append(1)
#                         else: 
#                             matrix[int((current_direction - 1) / 3)][(current_direction - 1) % 3].append(current_cost + 1)

#                 next_direction = (j+1)*3 + k+2       if          current_direction == 0        else            current_direction
#                 heappush(heap, (manhathan_distance + current_cost + 1, (next_direction, (manhathan_distance,(min_tuple[1][1][1][0] + [cell], (_x_pos, _y_pos))))))
#     return matrix
                


positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

def AStar(numpy_array, x, y, vision, found, obstacle):
    len_x = len(numpy_array)
    len_y = len(numpy_array[0])
    matrix = [[ [], [], [] ], 
                    [ [], [], [] ],
                    [ [], [], [] ]]
    heap = []
    heapify(heap)
    visited_cells = set()
    
    heappush(heap, (0, (0, (0, (x, y)))))                       # 1- costo, 2- direccion de partida del camino, 3- dist. manhathan, 4- posicion correspondiente
    visited_cells.add((x, y))
    
    while len(heap) != 0:
        min_tuple = heappop(heap)
        current_cost = min_tuple[0] - min_tuple[1][1][0]
        current_direction = min_tuple[1][0]
        for j in range(-1, 2):
            _x_pos = min_tuple[1][1][1][0] + j
            if _x_pos < 0 or _x_pos >= len_x or abs(_x_pos - x) > vision: continue                                                  # out of range test
            for k in range(-1, 2):
                _y_pos = min_tuple[1][1][1][1] + k
                if _y_pos < 0 or _y_pos >= len_y  or  (j == 0 and k == 0)  or  abs(_x_pos - x) > vision: continue       # out of range test
                cell = _x_pos, _y_pos
                if cell in visited_cells: continue                                                                                                             # cell already visited
                visited_cells.add((_x_pos, _y_pos))
                manhathan_distance = max(abs(_x_pos - x), abs(_y_pos - y))
                obstacle_in_cell = False
                for agent in numpy_array[_x_pos][_y_pos]:
                    if obstacle(agent): 
                        obstacle_in_cell = True
                        break
                    if found(agent):
                        if current_direction == 0:
                            matrix[j + 1][k + 1].append(1)
                        else: 
                            matrix[int((current_direction - 1) / 3)][(current_direction - 1) % 3].append(current_cost + 1)
                if obstacle_in_cell: continue
                next_direction = (j+1)*3 + k+2       if          current_direction == 0        else            current_direction
                heappush(heap, (manhathan_distance + current_cost + 1, (next_direction, (manhathan_distance, (_x_pos, _y_pos)))))
        
    # Adding obstacles
    for i, j in positions:
        if x + i - 1 not in range(0, len(numpy_array)) or y + j - 1 not in range(0, len(numpy_array[x + i - 1])): 
            matrix[i][j] = [-1]
            continue
        #print(f'position analized: {(x + i - 1, y + j - 1)}')
        for ent in numpy_array[x + i - 1][y + j - 1]:
            if obstacle(ent):
                matrix[i][j] = [-1]
    return matrix
