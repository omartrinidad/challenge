from sklearn.utils import resample
import pickle
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import preprocessing as pre
from sklearn.preprocessing import normalize
from sklearn import preprocessing


def clean_columns(df, elements):
    """
    """
    for element in elements:
        del df[element]


def add_columns(df):
    df["years_ago"] = 2016 - pd.to_numeric(df["release_year"])
    del df["release_year"]

    #encoder = preprocessing.LabelEncoder()
    #df["genre"] = encoder.fit_transform(df["genre"])
    #df["artist"] = encoder.fit_transform(df["artist"])


testdf = pre.default("data/test.csv")
test = pickle.load(open("test_set.ds", "rb"))
test["release_year"] = testdf["release_year"]

#clean_columns(test, ["artist"])
add_columns(test)

primero = pickle.load(open("dataset_two.ds", "rb"))
segundo = pickle.load(open("segundillo.ds", "rb"))
tercero = pickle.load(open("tercerillo.ds", "rb"))

#clean_columns(primero, ["artist"])
clean_columns(segundo, ["ages_cat", "media_id", "album_id", "artist_id", "genre_id", "user_id"])
clean_columns(tercero, ["ages_cat", "media_id", "album_id", "artist_id", "genre_id", "user_id"])

add_columns(primero)
add_columns(segundo)
add_columns(tercero)

# resampling
# we have 85659 1s, and 42742 0s, so we need 42917 new zeros, so, double the
# number of ones

frames = [primero, segundo, tercero]
ndf = pd.concat(frames)

indexes_zero = ndf[ndf["is_listened"] == 0].index
indexes_one = ndf[ndf["is_listened"] == 1].index

zeros = ndf.loc[indexes_zero]
ones = ndf.loc[indexes_one]
ones = ones.sample(len(zeros))

frames = [ones, zeros]
ndf = pd.concat(frames)

# shuffle
ndf.sample(frac=1)

# normalized dataset
# ndf["is_listened"].value_counts()

y = ndf["is_listened"]
del ndf["is_listened"]
x = ndf


# split data into train and test sets
seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=seed)

# normalize
X_train = normalize(X_train)
X_test = normalize(X_test)

# fit model no training data
model = XGBClassifier()
model.fit(X_train, y_train)

# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

# PREDICTIONS
sample_id = test["sample_id"]
del test["sample_id"]

test = normalize(test)

y_pred = model.predict(test)
predictions = [round(value) for value in y_pred]

solution = open("solution.csv", "wb")
solution.write("sample_id,is_listened\n")
# final prediction

for s, p in zip(sample_id, predictions):
    line = "{},{}\n".format(int(s), p)
    solution.write(line)

solution.close() 
