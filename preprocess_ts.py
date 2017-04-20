import pandas as pd
import numpy as np
from datetime import datetime
fromtimestamp = datetime.fromtimestamp


def sampling(name_file):
    """
    From original dataset recovers a sample and save this as serialized file
    After data is saved we read it in the next way:
    sample = pd.read_pickle(name_file)
    """
    dataset = pd.read_csv("data/train.csv")
    sample = dataset.sample(100000)
    sample.to_pickle(name_file)


def times2categorical(dataset):
    """Converts timestamp columns to categorical columns"""
    dataset['year'] = dataset['ts_listen'].apply(lambda x: fromtimestamp(x).year)
    dataset['month'] = dataset['ts_listen'].apply(lambda x: fromtimestamp(x).month)
    dataset['day'] = dataset['ts_listen'].apply(lambda x: fromtimestamp(x).day)
    dataset['hour'] = dataset['ts_listen'].apply(lambda x: fromtimestamp(x).hour)
    dataset['minute'] = dataset['ts_listen'].apply(lambda x: fromtimestamp(x).minute)
    dataset['weekday'] = dataset['ts_listen'].apply(lambda x: fromtimestamp(x).isoweekday())
    return dataset


def classify_age(age):
    """"""
    cat = ""
    if age <= 19:
        cat = "teen"
    elif age >= 26 and age <= 25:
        cat = "young"
    elif age >= 26 and age <= 29:
        cat = "adult"
    else:
        cat = "thirty_guy"
    return cat


def ages2categorical(dataset):
    """converts age column to categorical values:
    """
    dataset['ages_cat'] = dataset['user_age'].apply(lambda x: classify_age(x))
    return dataset


def release2categorical(dataset):
    """Converts release column to categorical values:
    80's, 90's, 2000's, 2010's
    """
    dataset['release_year'] = dataset['release_date'].apply(lambda x: fromtimestamp(x).year)
    return dataset


# already done
# df = pd.read_csv("data/train.csv")
# times2categorical(df)
# df.to_csv("data/train_p.csv")
