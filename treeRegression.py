import math

import numpy as np
import pandas as pd

from CSV import MyCSV
from tree.tree import MyTree


def count_entr(param: str) -> dict:
    entr = {}
    for i in data_percent[param].unique():
        pi = len(data_percent[data_percent[param] == i]) / len(data_percent)
        entr[i] = - (pi * math.log10(pi))

    entr = dict(sorted(entr.items(), key=lambda x: x[1], reverse=True))
    return entr




my_CSV = MyCSV()
data = my_CSV.data[['country', 'year', 'oil prices']]
data = data.sample(frac=1).reset_index(drop=True)

percent = 0.75
data_percent = data.iloc[:int(len(data) * percent)]
other_data = data.iloc[int(len(data) * percent):]

pi_year = count_entr('year')

pi_country = count_entr('country')
tree = MyTree(data_percent, list(pi_country.keys()))

d = other_data.groupby(['country', 'year'])['oil prices'].agg(np.average).reset_index()
print(d)
for i in d.to_numpy():
    print(i[0], i[1], tree.search(i[0], i[1]), d['oil prices'][d['country'] == i[0]][d['year'] == i[1]].to_numpy()[0])
