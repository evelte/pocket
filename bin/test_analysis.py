import shelve
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd
from pocket_reading.import_data import get_new_dataset
import pocket_reading
import os


# get updated data from pocket, and save it on shelve with today's name
# get_new_dataset(name)

file = os.path.join(pocket_reading.root, 'data', 'mshelve')
with shelve.open(file) as db:

    shelve_keys = list(db.keys())
    shelve_keys.sort()

    print('Loaded {} datasets:'.format(len(shelve_keys)))
    for k in shelve_keys:
        print(k)

    key = shelve_keys[-1]
    df = db[key]
    print('Analyzing dataset: {}'.format(key))


print(df.describe())

titles = df.resolved_title.values

text = ' '.join([str(x) for x in titles])

from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Generate a word cloud image
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# http://peekaboo-vision.blogspot.pt/2012/11/a-wordcloud-in-python.html