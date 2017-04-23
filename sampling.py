import pandas as pd

df = pd.read_csv("data/train.csv")

for i in range(0, 10):
    train_sample = df.sample(250000)
    filename = "data/train_sample_" + str(i) + ".csv"
    train_sample.to_csv(filename, index=False)
