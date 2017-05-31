from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

import preprocessing as pre
import pandas as pd
import pickle


def preprocess_zeros_test(test, alles):
    """
    This function updates the value of genres with 0 and learn which one should
    be the correct value
    """

    zeros = alles.loc[alles["genre_id"] == 0]
    no_zeros = alles.loc[alles["genre_id"] != 0]

    y = no_zeros["genre_id"]
    del no_zeros["genre_id"]
    x = no_zeros

    seed = 7
    test_size = 0.33
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=seed)

    # fit model no training data
    model = XGBClassifier()
    model.fit(X_train, y_train)

    y = zeros["genre_id"]
    del zeros["genre_id"]
    x = zeros

    # make predictions for test data
    pred = model.predict(X)
    predictions = [round(value) for value in pred]

    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    return x, y, predictions


def clean_columns(df, elements):
    """
    """
    for element in elements:
        del df[element]


def add_columns(df):
    df["years_ago"] = 2016 - pd.to_numeric(df["release_year"])
    del df["release_year"]


primero = pickle.load(open("dataset_two.ds", "rb"))
segundo = pickle.load(open("segundo.ds", "rb"))
tercero = pickle.load(open("tercero.ds", "rb"))

clean_columns(primero, ["artist"])
clean_columns(segundo, ["ages_cat", "media_id", "album_id", "artist_id", "user_id", "media", "is_listened"])
clean_columns(tercero, ["ages_cat", "media_id", "album_id", "artist_id", "user_id", "media", "is_listened"])

#add_columns(primero)
add_columns(segundo)
add_columns(tercero)

## Join all these together
frames = [segundo, tercero]
ndf = pd.concat(frames)

## Get rid off of genres zeros
#test = pickle.load(open("test_set.ds", "rb"))
test = pre.default("data/test.csv")
clean_columns(test, ["ages_cat", "album_id", "artist_id", "user_id", "media_id"])
add_columns(test)
x, y, predictions = preprocess_zeros_test(test, ndf)
