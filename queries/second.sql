-- Jaccard Distance for an unknown element and the existing clusters
-- Here with dummy data! In Python is built dinamically!

with kernels as (
         (
             select genre_id, 1 as kernel, user_id
             from songs
             where genre_id in (21, 33, 2, 4)
                   and genre_id != 0 and user_id != 0
             group by genre_id, user_id, kernel
             order by genre_id, user_id
         )
         union all
         (
             select genre_id, 3 as kernel, user_id
             from songs
             where genre_id != 0 and genre_id in (21, 33)
                   and user_id != 0
             group by genre_id, user_id, kernel
             order by genre_id, user_id
         )
     ),
     mykernels as (
         select center
         from centers
         where center in (1, 3)
     ),
     -- all new elements
     elements as (
         select genre_id
         from songs
         where genre_id != 0 and genre_id in (1202, 123, 200, 100)
               and user_id != 0
         group by genre_id
     ),
     -- all new elements and the correspondant users
     elements_users as (
        select genre_id, user_id
        --from elements inner join songs
        --on elements.genre_id = songs.genre_id
        from songs
        where genre_id != 0 and genre_id in (1202, 123, 200, 100)
              and user_id != 0
        group by songs.genre_id, songs.user_id
     ),
     -- get the cardinality for each cluster
     total_kernel as (
        select kernel, count(user_id) as tot
        from kernels
        group by kernel
     ),
     total_elements as (
        select genre_id, count(user_id) as tot
        from elements_users
        group by genre_id
     )
select *
from elements_users;
--    alles.kernel,
--    alles.genre_id,
--    coalesce(intersection, 0) as intersection,
--    t1.tot as cardinality_kernel,
--    t2.tot as cardinality_element
--from
--    (
--        select mykernels.center as kernel, elements.genre_id as genre_id
--        from mykernels cross join elements
--    ) as alles
--    left join
--    (
--        -- is it possible to delete this sub-select?
--        select
--            genre_id,
--            kernel,
--            count(intersection) as intersection
--        from (
--            select
--                elements_users.genre_id,
--                kernels.kernel,
--                count(elements_users.user_id) as intersection
--            from
--                kernels inner join elements_users
--            on
--                kernels.user_id = elements_users.user_id
--            group by
--                kernels.kernel, elements_users.genre_id, elements_users.user_id
--            order by
--                kernels.kernel, elements_users.genre_id, elements_users.user_id
--        ) as gr
--        group by kernel, genre_id
--    ) as grouped
--    on alles.kernel = grouped.kernel and alles.genre_id = grouped.genre_id
--    inner join total_kernel t1
--    on t1.kernel = alles.kernel
--    inner join total_elements t2
--    on t2.genre_id = alles.genre_id
