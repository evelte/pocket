import shelve
import pocket
import pandas as pd
import datetime
import pocket_reading
from pocket_reading import secrets
import os


pocket_instance = pocket.Pocket(secrets.POCKET_CONSUMER_KEY, secrets.ACCESS_TOKEN)


def convert_date(timestmp):
    d = datetime.datetime.fromtimestamp(int(timestmp)).strftime('%Y-%m-%d')
    return d


def get_new_dataset():
    res = pocket_instance.get(state='all')[0]
    articles = res['list']
    print('Loaded {} files'.format(len(articles)))

    imported = []
    for art in articles:
        imported.append(articles[art])

    return pd.DataFrame(imported)


def store_df(df, name):
    filename = os.path.join(pocket_reading.root, 'data', 'mshelve')
    with shelve.open(filename) as db:
        db[name] = df


if __name__ == '__main__':

    df = get_new_dataset()
    store_df(df, 'test')
