################################################################################
# Exploratory Data Analysis
# columns list(sample)
# sample.drop('is_listened', 1)
# yes = sample.loc[sample['is_listened'] == 1]
# no = sample.loc[sample['is_listened'] == 0]
################################################################################

import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
plt.style.use('seaborn-deep')

# read the serialized sample
sample = pd.read_pickle('data/first_p.dsg')


def age_skip_song():
    # relationship between age and skip song
    age_listen = sample[['user_age', 'is_listened']]
    ages = age_listen['user_age'].unique()
    ages.sort_values()
    table = age_listen.groupby(['user_age', 'is_listened']).size()
    table = table.sort_index(level='is_listened')
    result = table.as_matrix()

    plt.bar(ages, result[13:], width=0.5, color='g', align='center')
    plt.bar(ages+0.5, result[:13], width=0.5, color='r', align='center')
    plt.legend(('Is Listened', 'Not Listened'), loc='upper right')
    plt.show()


def times():
    # At which time the people hear the songs
    hour = sample[['hour']]
    hours = hour['hour'].unique()
    hours.sort()
    table = hour.groupby(['hour']).size()
    table = table.sort_index(level='hour')
    result = table.as_matrix()

    plt.bar(hours, result, width=0.5, color='g', align='center')
    plt.legend("People hearing music", loc='upper right')
    plt.xlim(0, 24)
    plt.show()


def histogram(sample, column_name):
    """Create a histogram"""
    column = sample[[column_name]]
    values = column[column_name].unique()
    values.sort()
    #print(values)
    table = column.groupby([column_name]).size()
    table = table.sort_index(level=column_name)
    #print(table)
    result = table.as_matrix()

    plt.bar(values, result, width=0.5, color='g', align='center')
    plt.legend("Title", loc='upper right')
    # plt.xlim(values[0], values[-1])
    plt.show()
    

# histogram(sample, 'release_year')
# times()
# age_skip_song()
