--.timer on <--- sqlite

-- genre_id = 0 has a lot of rows!!!

-- Jaccard Distance :)
with elements as (
              select genre_id, user_id
              from songs
              where is_listened = 0 and genre_id != 0 
              group by genre_id, user_id
     ),
     total as (
        select genre_id, count(user_id) as tot
        from songs
        where is_listened = 0 and (genre_id != 0)
        group by genre_id
      )
select A.genre_id as set_a,
       B.genre_id as set_b,
       count(A.user_id) as intersection,
       t1.tot as cardinality_a,
       t2.tot as cardinality_b
from
    elements as A inner join elements as B
    on A.genre_id != B.genre_id
       and A.user_id = B.user_id
    inner join total t1
    on t1.genre_id = A.genre_id
    inner join total t2
    on t2.genre_id = B.genre_id
group by
    A.genre_id, B.genre_id, t1.tot, t2.tot
order by
    set_a, set_b
