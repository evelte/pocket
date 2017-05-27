import shelve
import pocket
from pprint import pprint
import pandas as pd
import datetime
import pocket_reading
from pocket_reading import secrets
import os


pocket_instance = pocket.Pocket(secrets.POCKET_CONSUMER_KEY, secrets.ACCESS_TOKEN)

def convert_date(timestmp):
    d = datetime.datetime.fromtimestamp(int(timestmp)).strftime('%Y-%m-%d')
    return d


def get_new_dataset(name):
    res = pocket_instance.get(state='all')
    res = res[0]

    fields = list(res.keys())
    print(fields)

    pprint(res['list'])

    articles = res['list']
    n_articles = len(articles)

    article_fields = list(articles.keys())
    print(article_fields)

    imported = []
    for art in articles:
        imported.append(articles[art])

    df_all = pd.DataFrame(imported)[['resolved_title', 'resolved_id', 'status', 'word_count',
                                     'time_added']]

    filename = os.path.join(pocket_reading.root, 'data', 'mshelve')
    with shelve.open(filename) as db:
        db[name] = df_all
