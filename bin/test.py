import os
import pocket_reading
import shelve

file = os.path.join(pocket_reading.root, 'data', 'mshelve')
with shelve.open(file) as db:

    keys = db.keys()
    for k in keys:
        print(k)

    ds = db[k]

    print(ds.head())