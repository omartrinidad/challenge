import pandas as pd
import numpy as np
import pickle
from sql import *


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
#generate_distance_matrix("genre_id")
generate_distance_matrix("media_id")
#generate_distance_matrix("album_id")
#generate_distance_matrix("artist_id")
