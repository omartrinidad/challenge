# https://github.com/letiantian/kmedoids/

import pandas as pd
import numpy as np
import pickle
from kmedoids import *
from sql import *
from sklearn.metrics import silhouette_score, silhouette_samples

import matplotlib.pyplot as plt
import matplotlib.cm as cm


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


def silhouette_vizualization(matrix, n_clusters, cluster_labels, M):
    """
    """
            
    sample_silhouette_values = silhouette_samples(matrix, cluster_labels,
            metric="precomputed")

    # Create a subplot with 1 row and 2 columns
    fig, (ax1) = plt.subplots(1)
    fig.set_size_inches(18, 40)
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 0.3])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(matrix) + (n_clusters + 1) * 10])

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.01, y_lower + 0.5 * size_cluster_i, str(M[i]))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.3])

    # 2nd Plot showing the actual clusters formed
    colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    plt.show()


def cross_validation_kmedoids(matrix, elements):
    """Get the best kmedoids clusters evaluated with  """

    best_results = {}

    # for n_clusters in np.linspace(15, 45, 7):
    for n_clusters in range(16, 81):

        best_score = 0
        best_centers = None

        #print("------------->", n_clusters)

        for i in range(100):
            M, C = kMedoids(matrix, n_clusters, tmax=20)
            cluster_labels = np.zeros(len(elements))
            for c in C:
                cluster_labels[C[c]] = c

            # ToDo: Analize clustering with Silhouhette
            silhouette_avg = silhouette_score(matrix, cluster_labels, metric="precomputed")
            # print("------------->", silhouette_avg)
            if silhouette_avg > best_score:
                best_centers = M
                best_score = silhouette_avg

        best_centers.sort()
        best_results[n_clusters] = best_score, best_centers

    return best_results



# load (or generate) distance matrix
"""
generate_distance_matrix("genre")
generate_distance_matrix("media")
generate_distance_matrix("album")
generate_distance_matrix("artist")
"""

# Get the best possible kmedoids clutering according to Silhuotte
matrix, elements = load_distance_matrix("genre")
best_results_genre = cross_validation_kmedoids(matrix, elements)

matrix, elements = load_distance_matrix("media")
best_results_media = cross_validation_kmedoids(matrix, elements)

matrix, elements = load_distance_matrix("album")
best_results_album = cross_validation_kmedoids(matrix, elements)

matrix, elements = load_distance_matrix("artist")
best_results_artist = cross_validation_kmedoids(matrix, elements)
