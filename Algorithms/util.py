import numpy as np
import random

def adjacent_box(matrix, new_position, isValid):
    new_r, new_c =  new_position
    adjacents = []
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            if isValid(matrix[r][c]):
                if abs(new_r - r) <= 1 and abs(new_c - c):
                    adjacents.append((r,c))
    return adjacents

def extract_radius_matrix(matrix, position, radius):
    r, c = position
    min_r = max(0, r-radius)
    min_c = max(0, c-radius)
    max_r = min(matrix.shape[0], r+radius+1)
    max_c = min(matrix.shape[1], c+radius+1)
    extract = matrix[min_r:max_r, min_c:max_c]
    print(position)
    print(extract)
    return extract
