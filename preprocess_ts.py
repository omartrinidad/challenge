import pandas as pd
import numpy as np
import datetime


df = pd.read_csv("data/train.csv")

df['year'] = df['ts_listen'].apply(lambda x: datetime.datetime.fromtimestamp(x).year)
df['month'] = df['ts_listen'].apply(lambda x: datetime.datetime.fromtimestamp(x).month)
df['day'] = df['ts_listen'].apply(lambda x: datetime.datetime.fromtimestamp(x).day)
df['hour'] = df['ts_listen'].apply(lambda x: datetime.datetime.fromtimestamp(x).hour)
df['minute'] = df['ts_listen'].apply(lambda x: datetime.datetime.fromtimestamp(x).minute)
df['weekday'] = df['ts_listen'].apply(lambda x: datetime.datetime.fromtimestamp(x).isoweekday())

df.to_csv("data/train_p.csv")

