import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from pandas.stats.api import ols

sample = pd.read_csv('data/train_sample_0.csv')
sample = sample[['media_id', 'album_id', 'genre_id', 'artist_id', 'media_duration']]

def scatterplot():
    plt.plot(sample['artist_id'], sample['media_duration'], 'bo')
    plt.show()
