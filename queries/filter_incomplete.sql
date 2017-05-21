-- media_id, there is no id = 0
-- album_id, there is no id = 0
select count(*)
from songs
where genre_id != 0 and user_id != 0
