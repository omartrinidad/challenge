# https://github.com/letiantian/kmedoids/

import pandas as pd
import numpy as np
import pickle
from kmedoids import *
from sql import *
from sklearn.metrics import silhouette_score


def generate_distance_matrix(column):
    """
    Generate distance matrix for specific column and save them in a serialized
    file.
    """
    matrix, elements = count_users(column)
    with open(column + ".dsg", "wb") as f:
        pickle.dump((matrix, elements), f)


def load_distance_matrix(column):
    """
    Load previously generated distance matrix for specific column and save them
    in a serialized file.
    """
    with open(column + ".dsg", "rb") as f:
        matrix = pickle.load(f)
    return matrix


# load (or generate) distance matrix
"""
generate_distance_matrix("genre")
generate_distance_matrix("media")
generate_distance_matrix("album")
generate_distance_matrix("artist")
"""

#matrix_genre, elements = load_distance_matrix("genre")
#load_distance_matrix("media")
#load_distance_matrix("album")
#load_distance_matrix("artist")

#M, C = kMedoids(matrix_genre, 8, tmax=2000)
#labels = np.array(map(str, M))

# ToDo: Analize clustering with Silhouhette
# silhouette_score(matrix_genre, metric="precomputed")
