import shelve
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd
from pocket_reading.import_data import get_new_dataset

# name of dataset is defined using today's date
today = datetime.datetime.now().date()
name = str(today)

# get updated data from pocket, and save it on shelve with today's name
get_new_dataset(name)

with shelve.open('mshelve') as db:

    shelve_keys = list(db.keys())
    shelve_keys.sort()

    print('Loaded {} datasets:'.format(len(shelve_keys)))
    for k in shelve_keys:
        print(k)

    dfs = [db[key] for key in shelve_keys]

collect_date_list = []
read_articles_list = []
read_words_list = []
unread_articles_list = []
unread_words_list = []

for df_ind, df_all in enumerate(dfs):
    df_name = shelve_keys[df_ind]

    df_all['time_added'] = df_all['time_added'].apply(lambda x: int(x))

    df_read = df_all[df_all['status'] == '1']
    df_unread = df_all[df_all['status'] == '0']

    # filter by year
    def filter_by_year(dataset, start_year, end_year):
        start = mdates.date2num(datetime.date(start_year, 1, 1))
        end = mdates.date2num(datetime.date(end_year, 1, 1))

        dates_list = dataset['time_added'].tolist()

        # convert the epoch format to matplotlib date format
        dates_list = mdates.epoch2num(dates_list)

        selected = [dataset.iloc[[index]]['resolved_id'].values[0] for index, x in enumerate(dates_list) if start <= x < end]
        filtered = dataset[dataset.resolved_id.isin(selected)]

        return filtered


    # analyzing year
    year = 2017

    #df_read = filter_by_year(df_read, year, year + 1)
    #df_unread = filter_by_year(df_unread, year, year + 1)

    mpl_read = mdates.epoch2num(df_read['time_added'].tolist())
    mpl_unread = mdates.epoch2num(df_unread['time_added'].tolist())

    read_words = df_read.word_count.fillna(0).astype(int).sum()
    unread_words = df_unread.word_count.fillna(0).astype(int).sum()

    collect_date = datetime.datetime.strptime(df_name, '%Y-%m-%d')

    collect_date_list.append(collect_date)
    read_articles_list.append(len(mpl_read))
    read_words_list.append(read_words)
    unread_articles_list.append(len(mpl_unread))
    unread_words_list.append(unread_words)

    # print summary
    print('\nDataset: ', df_name)
    print('Number of read articles: {}'.format(len(mpl_read)))
    print('Total number of words: {}'.format(read_words))
    print('\nNumber of articles to read: {}'.format(len(mpl_unread)))
    print('Total number of words: {}'.format(unread_words))
    print('***********************************\n\n')

    # plot it
    # fig, ax = plt.subplots(1,1)
    # ax.hist(mpl_read, bins=170, color='lightblue', label='read articles ({})'.format(len(mpl_read)))
    # ax.hist(mpl_unread, bins=170, color='black', alpha=0.3, label='unread articles ({})'.format(len(mpl_unread)))
    # ax.xaxis.set_major_locator(mdates.MonthLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    # legend = ax.legend(loc='upper center')
    # plt.setp(ax.xaxis.get_majorticklabels(), rotation=70)
    # plt.show()


average_articles_read = []
average_words_read = []
timeline = []
for dataset_index in range(0, len(collect_date_list)-1):
    time_delta = (collect_date_list[dataset_index+1]-collect_date_list[dataset_index]).days
    read_articles = read_articles_list[dataset_index+1] - read_articles_list[dataset_index]
    read_words = read_words_list[dataset_index + 1] - read_words_list[dataset_index]

    average_articles_read.append(round(read_articles / time_delta, 1))
    average_words_read.append(int(read_words / time_delta))
    timeline.append(str(collect_date_list[dataset_index+1].date()))

    print('Analyzing set {}/{}'.format(dataset_index+1, len(collect_date_list)-1))
    print('Reading time: {} days'.format(time_delta))
    print('Number of read articles: {}'.format(read_articles))
    print('Number of read words: {}'.format(read_words))
    print('')

print(timeline)
print(average_articles_read)
print(average_words_read)

import seaborn as sns
sns.set(style="white")

average_read = pd.DataFrame({'read_articles': average_articles_read,
                             'read_words': average_words_read,
                             'time': timeline})

sns.set_style("white")
fig, ax = plt.subplots()
ax = sns.barplot(x="time", y="read_articles", data=average_read)
ax2 = ax.twinx()
sns.barplot(x="time", y="read_words", data=average_read)
# sns.despine(ax=ax, right=True, left=True)
# sns.despine(ax=ax2, left=True, right=False)
#ax2.spines['right'].set_color('white')

#

sns.plt.show()
