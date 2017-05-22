################################################################################
#
# SQL queries to summarize the dataset
# good tutorial to configure postgresql: https://suhas.org/sqlalchemy-tutorial/
#
# The best way to import from .CSV to Postgres table
# \copy songs from 'data/train.csv' delimiter ',' csv;
#
################################################################################

import sqlite3
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np


try:
    # postgresql
    engine = create_engine('postgresql://datascience:ds@localhost:5432/songs')
except ValueError as e:
    print(e)


def count_users(column):
    """
    This function returns a number of users that decided to hear the song
    """

    query = """
        with elements as (
                select {}_id, user_id
                from sample_{}
                group by {}_id, user_id
             ),
             groups as (
                select {}_id
                from sample_{}
                group by {}_id
             ),
             total as (
                select {}_id, count(user_id) as tot
                from (
                    select {}_id, user_id
                    from sample_{}
                    group by {}_id, user_id
                ) as subquery
                group by {}_id
              )
        select alles.set_a,
               alles.set_b,
               coalesce(intersection, 0) as intersection,
               t1.tot as cardinality_a,
               t2.tot as cardinality_b
        from
            (select G1.{}_id as set_a, G2.{}_id as set_b
             from groups as G1 cross join groups as G2
            ) as alles
            left join
            (select A.{}_id as set_a,
                    B.{}_id as set_b,
                    count(A.user_id) as intersection
            from
                elements as A inner join elements as B
                on A.user_id = B.user_id
            group by
                A.{}_id, B.{}_id
            order by
                set_a, set_b
            ) as grouped
            on alles.set_a = grouped.set_a and alles.set_b = grouped.set_b
            inner join total t1
            on t1.{}_id = alles.set_a
            inner join total t2
            on t2.{}_id = alles.set_b
    """.replace("{}", column)

    df = pd.read_sql_query(query, engine)
    jaccard = 1 - df["intersection"] / (df["cardinality_a"] + df["cardinality_b"] - df["intersection"])
    size = int(np.sqrt(jaccard.size))
    matrix = np.reshape(jaccard, (size, size))

    return matrix, df['set_b'][0:int(size)]
