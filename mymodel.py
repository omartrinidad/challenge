from sklearn.utils import resample
import pickle
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

test = pickle.load(open("test_set.ds", "rb"))

df = pickle.load(open("dataset_two.ds", "rb"))
del df['release_year']


# resampling
# we have 85659 1s, and 42742 0s, so we need 42917 new zeros, so, double the
# number of ones
indexes = df[df["is_listened"] == 0].index
repeated = df.loc[indexes]
frames = [df, repeated]
ndf = pd.concat(frames)

# shuffle
ndf.sample(frac=1)

# normalized dataset
# ndf["is_listened"].value_counts()

y = df["is_listened"]
del df["is_listened"]
x = df


# split data into train and test sets
seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=seed)

# fit model no training data
model = XGBClassifier()
model.fit(X_train, y_train)

# make predictions for test data
#y_pred = model.predict(X_test)
#predictions = [round(value) for value in y_pred]

# evaluate predictions
# accuracy = accuracy_score(y_test, predictions)
# print("Accuracy: %.2f%%" % (accuracy * 100.0))

# PREDICTIONS
sample_id = test["sample_id"]
del test["sample_id"]

y_pred = model.predict(test)
predictions = [round(value) for value in y_pred]

solution = open("solution.csv", "wb")
solution.write("sample_id,is_listened\n")
# final prediction

for s, p in zip(sample_id, predictions):
    line = "{},{}\n".format(int(s), p)
    solution.write(line)

solution.close()
