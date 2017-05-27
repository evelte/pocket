import shelve
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd
from pocket_reading.import_data import get_new_dataset

# get updated data from pocket, and save it on shelve with today's name
# get_new_dataset(name)

with shelve.open('mshelve') as db:

    shelve_keys = list(db.keys())
    shelve_keys.sort()

    print('Loaded {} datasets:'.format(len(shelve_keys)))
    for k in shelve_keys:
        print(k)

    key = shelve_keys[-1]
    df = db[key]
    print('Analyzing dataset: {}'.format(key))


print(df.describe())

# http://peekaboo-vision.blogspot.pt/2012/11/a-wordcloud-in-python.html