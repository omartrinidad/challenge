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
from preprocess import preprocess_helper as helper
# plt.style.use('seaborn-deep')

# read the sample
sample = helper.preprocess_default('data/train_sample_0.csv')

#---

def age_skip_song():
    # relationship between age and skip song
    age_listen = sample[['user_age', 'is_listened']]
    ages = age_listen['user_age'].unique()
    ages.sort()
    table = age_listen.groupby(['user_age', 'is_listened']).size()
    table = table.sort_index(level='is_listened')
    result = table.as_matrix()

    plt.bar(ages, result[13:], width=0.5, color='g', align='center')
    plt.bar(ages+0.5, result[:13], width=0.5, color='r', align='center')
    plt.legend(('Is Listened', 'Not Listened'), loc='upper right')
    plt.show()

#---

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

#---

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
    
    
#---

# draws how many users listened or not a track in a certain platform_family by age.

def draw_platform_family_by_age(id, title):
	sub_sample = sample[['platform_family','user_age','is_listened']]
	sub_sample = sub_sample[(sub_sample.platform_family == id)]
	
	ages = sub_sample['user_age'].unique()
	ages.sort()
	
	table = sub_sample.groupby(['platform_family','user_age', 'is_listened']).size()
	table = table.sort_index(level='is_listened')
	table_matrix = table.as_matrix()
	
	plt.title(title)
		
	# bug: when the number of ages is not exactly 13, but with all the data set, less probable.

	plt.bar(ages, table_matrix[13:], width=0.5, color='g', align='center')
	plt.bar(ages+0.5, table_matrix[:13], width=0.5, color='r', align='center')
	
	plt.legend(('Is Listened', 'Not Listened'), loc='upper right')
	plt.ylabel("Quantity");
	plt.xlabel("Ages");
	
	plt.show()

#---

# histogram(sample, 'release_year')
# times()
# age_skip_song()

# for platform_family 0

draw_platform_family_by_age(0, "Platform Family 0")

# for platform_family 1

draw_platform_family_by_age(1, "Platform Family 1")

# for platform_family 2

draw_platform_family_by_age(2, "Platform Family 2")


