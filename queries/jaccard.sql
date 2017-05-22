-- genre_id = 0 has a lot of rows!!!
-- Jaccard Distance
-- A \intersection B / A \union B

with elements as (
        select genre_id, user_id
        from sample_genre
        group by genre_id, user_id
     ),
     genres as (
        select genre_id
        from sample_genre
        group by genre_id
     ),
     total as (
        select genre_id, count(user_id) as tot
        from (
            select genre_id, user_id
            from sample_genre
            group by genre_id, user_id
        ) as subquery
        group by genre_id
      )
select alles.set_a,
       alles.set_b,
       coalesce(intersection, 0) as intersection,
       t1.tot as cardinality_a,
       t2.tot as cardinality_b
from
    (
     select G1.genre_id as set_a, G2.genre_id as set_b
     from genres as G1 cross join genres as G2
    ) as alles
    left join
    (select A.genre_id as set_a,
            B.genre_id as set_b,
            count(A.user_id) as intersection
    from
        elements as A inner join elements as B
        on A.user_id = B.user_id
    group by
        A.genre_id, B.genre_id
    order by
        set_a, set_b
    ) as grouped
    on alles.set_a = grouped.set_a and alles.set_b = grouped.set_b
    inner join total t1
    on t1.genre_id = alles.set_a
    inner join total t2
    on t2.genre_id = alles.set_b
