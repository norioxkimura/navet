
from __future__ import print_function

import csv

def read(path):
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            for i, j in enumerate(row):
                row[i] = row[i].decode('cp932')
                print(row[i], end=' ')
            print('')

