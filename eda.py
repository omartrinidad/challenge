import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
plt.style.use('seaborn-deep')


################################################################################
# Exploratory Data Analysis
# columns list(small)
# sample.drop('is_listened', 1)
################################################################################

# read the serialized sample
sample = pd.read_pickle('data/second.dsg')

# relationship between age and skip song
sample = sample[['user_age', 'is_listened']]
ages = sample['user_age'].unique()
ages.sort()
table = sample.groupby(['user_age', 'is_listened']).size()
table = table.sort_index(level='is_listened')

result = table.as_matrix()

plt.bar(ages, result[13:], width=0.5, color='g', align='center')
plt.bar(ages+0.5, result[:13], width=0.5, color='r', align='center')
plt.legend(('Is Listened', 'Not Listened'), loc='upper right')

# According to age how much the people skip the song?
# yes = sample.loc[sample['is_listened'] == 1]
# no = sample.loc[sample['is_listened'] == 0]

plt.show()
