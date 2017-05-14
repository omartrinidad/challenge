import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pandas.stats.api import ols
from sql import *
from scipy.spatial import distance_matrix

sample = pd.read_csv('data/train_sample_0.csv')
sample = sample[['media_id', 'album_id', 'genre_id', 'artist_id', 'media_duration']]


def scatter2D(axis_x, axis_y):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(sample[axis_x][:100], sample[axis_y][:100], 'bo')
    ax.set_xlabel(axis_x, labelpad=20)
    ax.set_ylabel(axis_y, labelpad=20)
    plt.show()


def scatter3D(axis_x, axis_y, axis_z):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(sample[axis_x][:1000], sample[axis_y][:1000], sample[axis_z][:1000], 'bo')

    ax.set_xlabel(axis_x, labelpad=20)
    ax.set_ylabel(axis_y, labelpad=20)
    ax.set_zlabel(axis_z, labelpad=20)

    plt.show()


#data = count_users("media_id")
#data = count_users("genre_id")
#data = count_users("artist_id")
#data = count_users("genre_id")

arreglo = data['count_users']
conteo = np.reshape(arreglo, (-1, len(arreglo)))
conteo = conteo.T
distances = distance_matrix(conteo, conteo)

# Plot the data
fig, ax = plt.subplots()
heatmap = ax.pcolor(distances, cmap=plt.cm.Blues, alpha=0.8)

fig = plt.gcf()
fig.set_size_inches(8,11)
plt.show()


#scatter2D('media_id', 'album_id')
#scatter2D('genre_id', 'artist_id')
