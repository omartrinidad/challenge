################################################################################
# SQL queries to summarize the dataset
# good tutorial to configure postgresql: https://suhas.org/sqlalchemy-tutorial/
################################################################################

import sqlite3
import psycopg2
import pandas as pd
from preprocess import preprocess_helper as helper
from sqlalchemy import create_engine


try:
    # sqlite3
    # conn = sqlite3.connect(dbfile)
    # dbfile = r'data/train_sample_0.db'

    # postgresql
    engine = create_engine('postgresql://datascience:ds@localhost:5432/songs')
    # read and save the csv
    sample = helper.preprocess_default('data/train_sample_1.csv')
    # sample.to_sql('songs', engine, if_exists='replace')
except ValueError:
    print(ValueError)


def count_users(column):
    """
    This function returns the number of users that decided to hear the song
    """

    query = """select count_users
               from
                   (select {}, count(user_id) as count_users
                   from songs
                   group by {}
                   ) summary
               group by count_users""".format(column, column)

    df = pd.read_sql_query(query, engine)
    # normalize the dataset

    # df = df.sample(frac=1)

    return df


df = count_users('genre_id')
