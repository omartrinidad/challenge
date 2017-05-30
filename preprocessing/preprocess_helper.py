import pandas as pd
import preprocess_funcs
import numpy as np
from datetime import datetime
fromtimestamp = datetime.fromtimestamp


def add_times2categorical(dataframe):
    """Converts timestamp columns to categorical columns"""
    # dataframe['year'] = dataframe['ts_listen'].apply(lambda x: fromtimestamp(x).year)
    # dataframe['month'] = dataframe['ts_listen'].apply(lambda x: fromtimestamp(x).month)
    # dataframe['day'] = dataframe['ts_listen'].apply(lambda x: fromtimestamp(x).day)
    dataframe['hour'] = dataframe['ts_listen'].apply(lambda x: fromtimestamp(x).hour)
    # dataframe['minute'] = dataframe['ts_listen'].apply(lambda x: fromtimestamp(x).minute)
    dataframe['weekday'] = dataframe['ts_listen'].apply(lambda x: fromtimestamp(x).isoweekday())
    dataframe['is_weekend'] = dataframe['ts_listen'].apply(lambda x: 1 if fromtimestamp(x).isoweekday() > 5 else 0)
    return dataframe


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


def add_ages2categorical(dataframe):
    """converts age column to categorical values:
    """
    dataframe['ages_cat'] = dataframe['user_age'].apply(lambda x: classify_age(x))
    return dataframe


def add_releaseyear(dataframe):
    """extract release year from release date"""
    dataframe['release_year'] = dataframe['release_date'].apply(lambda x: str(x)[:4])
    return dataframe


def drop_columns(dataframe, col_names):
    col_indexes = np.nonzero(dataframe.columns.isin(col_names))[0]
    return dataframe.drop(dataframe.columns[col_indexes], axis=1)


def preprocess_default(pathname):
    """
    Examples:
        >>> preprocess_default("data/train_sample_0.csv")
    """
    df = pd.read_csv(pathname)
    df = preprocess_funcs.add_times2categorical(df)
    df = preprocess_funcs.add_releaseyear(df)
    df = preprocess_funcs.add_ages2categorical(df)
    df = preprocess_funcs.drop_columns(df, ['ts_listen', 'release_date'])

    # test export!
    # df.to_csv("../data/testhaha.csv", index=False)

    return df
