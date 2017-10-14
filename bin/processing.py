import pandas as pd
from pocket_reading.db_connect import DB
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


db = DB('pocket', 'elena')

query = 'select distinct on(item_id) * from status'
data = db.query(query)

columns = db.query('''select column_name
                   from information_schema.columns
                   where table_name = 'status';''')

columns = list(list(zip(*columns))[0])

df = pd.DataFrame(data, columns=columns)
df_read = df.loc[df['status'] == 'archived']
df_unread = df.loc[df['status'] == 'added']

read = df_read['time_read'].values
unread = df_unread['time_added'].values
added = df['time_added'].values

fig, ax = plt.subplots(3,1)
ax[0].hist(read, bins=170, color='green', alpha=0.3, label='read articles ({})'.format(len(read)))
ax[1].hist(unread, bins=170, color='red', alpha=0.3, label='unread articles ({})'.format(len(unread)))
ax[2].hist(added, bins=170, color='black', alpha=0.3, label='added articles ({})'.format(len(added)))

for ind in range(0, len(ax)):
    ax[ind].set_xlim(min(added), max(added))
    ax[ind].xaxis.set_major_locator(mdates.MonthLocator())
    ax[ind].xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    legend = ax[ind].legend(loc='upper left')
    plt.setp(ax[ind].xaxis.get_majorticklabels(), rotation=20)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
plt.show()
