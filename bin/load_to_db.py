import os
import pocket_reading
import shelve
import datetime
from pocket_reading.db_connect import DB


db = DB('pocket', 'elena')

# 0, 1, 2 - 1 if the item is archived - 2 if the item should be deleted
create_pocket_status = '''DROP TYPE IF EXISTS pocket_status CASCADE;
                       CREATE TYPE pocket_status AS ENUM ('added', 'archived', 'to_delete')'''
db.execute(create_pocket_status)

create_table = '''DROP TABLE IF EXISTS status;
               CREATE TABLE IF NOT EXISTS status
               (
               item_id BIGINT,
               excerpt TEXT,
               favorite BOOL,
               given_title TEXT,
               given_url TEXT,
               has_image BOOL,
               has_video BOOL,
               is_article BOOL,
               resolved_id BIGINT,
               resolved_title TEXT,
               resolved_url TEXT,
               sort_id INT,
               status pocket_status,
               time_added TIMESTAMP,
               time_favorited TIMESTAMP,
               time_read TIMESTAMP,
               time_updated TIMESTAMP,
               word_count BIGINT,
               status_update_date TIMESTAMP,
               CONSTRAINT listing_id PRIMARY KEY (item_id, status_update_date));
               '''
db.execute(create_table)

file = os.path.join(pocket_reading.root, 'data', 'mshelve')
with shelve.open(file) as shel:
    df = shel['test']

for index, row in df.iterrows():

    item_id = int(row.item_id)
    excerpt = row.excerpt
    favorite = False if row.favorite == '0' else True
    given_title = row.given_title
    given_url = row.given_url
    has_image = False if row.has_image == '0' else False
    has_video = False if row.has_video == '0' else False
    is_article = False if row.is_article == '0' else False
    resolved_id = int(row.resolved_id)
    resolved_title = row.resolved_title
    resolved_url = row.resolved_url
    sort_id = int(row.sort_id) if row.sort_id else None
    status = 'added' if row.status == '0' else ('archived' if row.status == '1' else 'to_delete')
    time_added = convert_epoch_to_date(row.time_added)
    time_favorited = convert_epoch_to_date(row.time_favorited)
    time_read = convert_epoch_to_date(row.time_read)
    time_updated = convert_epoch_to_date(row.time_updated)
    try:
        word_count = int(row.word_count)
    except:
        word_count = None
    status_update_date = str(datetime.datetime.now())

    values = [item_id, excerpt, favorite, given_title, given_url, has_image, has_video, is_article, resolved_id,
              resolved_title, resolved_url, sort_id, status, time_added, time_favorited, time_read, time_updated,
              word_count, status_update_date]

    insert_line = '''INSERT INTO status
                          (item_id, excerpt, favorite, given_title, given_url, has_image, has_video, is_article,
                          resolved_id, resolved_title, resolved_url, sort_id, status, time_added, time_favorited,
                          time_read, time_updated, word_count, status_update_date)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                          '''

    db.execute(insert_line, values)

print('READY!!')

# aux functions
# ======================================================================================================================

def convert_epoch_to_date(epoch):
    if int(epoch) == 0:
        return None
    else:
        date = datetime.datetime.fromtimestamp(int(epoch))
        return date
