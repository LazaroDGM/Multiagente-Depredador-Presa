import numpy as np


def select_from_results(results, i):
    result = [r.T[i] for r in results]
    return np.array(result)

