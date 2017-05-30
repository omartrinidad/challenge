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


def distance_for_new_elements(clusters, column, unknown_ids):
    """
    This function returns a number of users that decided to hear the song, with
    unseen elements in the other cluster
    """

    # generate query string
    querito = ""
    first_block = []

    for c in clusters:
        elements = ", ".join(str(x) for x in clusters[c])
        kernel = """(select []_id, {} as kernel, user_id
            from songs
            where []_id in ({})
                  and genre_id != 0 and user_id != 0
            group by []_id, user_id, kernel
            order by []_id, user_id)""".replace("[]", column)
        kernel = kernel.format(c, elements)
        first_block.append(kernel)


    first_block = "\nunion all\n".join(str(x) for x in first_block)
    centers = ", ".join(str(x) for x in clusters.keys())


    second_block = """
                    mykernels as (
                        select center
                        from centers
                        where center in ({})
                    ),
                    elements as (
                        select []_id
                        from songs
                        where genre_id != 0 and user_id != 0 and []_id in ({})
                        group by []_id
                    ),
                    elements_users as (
                        select genre_id, user_id
                        from songs
                        where genre_id != 0 and user_id != 0 and []_id in ({})
                        group by []_id, user_id
                    ),
                    total_kernel as (
                       select kernel, count(user_id) as tot
                       from kernels
                       group by kernel
                    ),
                    total_elements as (
                       select []_id, count(user_id) as tot
                       from elements_users
                       group by []_id
                    )
                select
                    alles.kernel,
                    alles.[]_id,
                    coalesce(intersection, 0) as intersection,
                    t1.tot as cardinality_kernel,
                    t2.tot as cardinality_element
                from (
                        select mykernels.center as kernel, elements.[]_id as []_id
                        from mykernels cross join elements
                    ) as alles
                    left join
                    (
                        select
                            []_id,
                            kernel,
                            count(intersection) as intersection
                        from (
                            select
                                elements_users.[]_id,
                                kernels.kernel,
                                count(elements_users.user_id) as intersection
                            from
                                kernels inner join elements_users
                            on
                                kernels.user_id = elements_users.user_id
                            group by
                                kernels.kernel, elements_users.[]_id, elements_users.user_id
                            order by
                                kernels.kernel, elements_users.[]_id, elements_users.user_id
                        ) as gr
                        group by kernel, []_id
                    ) as grouped
                on alles.kernel = grouped.kernel and alles.[]_id = grouped.[]_id
                inner join total_kernel t1
                on t1.kernel = alles.kernel
                inner join total_elements t2
                on t2.[]_id = alles.[]_id
                """.format(centers, unknown_ids, unknown_ids).replace("[]", column)

    query = """with kernels as ( {} ), {}""".format(first_block, second_block)

    df = pd.read_sql_query(query, engine)
    jaccard = 1 - df["intersection"] / (df["cardinality_kernel"] + df["cardinality_element"] - df["intersection"])
    return df



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
