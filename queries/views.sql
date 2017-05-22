-- create views to get the 2000 rows genres, artists, media, albums with more
-- users

create or replace view sample_genre as
--create view sample_genres as
    select common.genre_id, songs.user_id
    from
    (
        select genre_id
        from (
            select genre_id, count(user_id) as tot
            from (
                select genre_id, user_id
                from songs
                where genre_id != 0 and user_id != 0
                group by genre_id, user_id
            ) as counting
            group by genre_id
        ) as counting_
        order by tot desc
        limit 2000
    ) as common
    inner join songs
    on common.genre_id = songs.genre_id
    where user_id != 0;


create or replace view sample_artist as
    select common.artist_id, songs.user_id
    from
    (
        select artist_id
        from (
            select artist_id, count(user_id) as tot
            from (
                select artist_id, user_id
                from songs
                where genre_id != 0 and user_id != 0
                group by artist_id, user_id
            ) as counting
            group by artist_id
        ) as counting_
        order by tot desc
        limit 2000
    ) as common
    inner join songs
    on common.artist_id = songs.artist_id
    where user_id != 0;


create or replace view sample_media as
    select common.media_id, songs.user_id
    from
    (
        select media_id
        from (
            select media_id, count(user_id) as tot
            from (
                select media_id, user_id
                from songs
                where genre_id != 0 and user_id != 0
                group by media_id, user_id
            ) as counting
            group by media_id
        ) as counting_
        order by tot desc
        limit 2000
    ) as common
    inner join songs
    on common.media_id = songs.media_id
    where user_id != 0;


create or replace view sample_album as
    select common.album_id, songs.user_id
    from
    (
        select album_id
        from (
            select album_id, count(user_id) as tot
            from (
                select album_id, user_id
                from songs
                where genre_id != 0 and user_id != 0
                group by album_id, user_id
            ) as counting
            group by album_id
        ) as counting_
        order by tot desc
        limit 2000
    ) as common
    inner join songs
    on common.album_id = songs.album_id
    where user_id != 0;
