# -*- coding: utf-8 -*-
"""
This script serves to create a second data file for each city which contains only clicks as opposed
to all impressions.
"""

import csv


infiles = ['C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\Seattle Metro.txt',
           'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\Boston Metro.txt',
           'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\New Orleans Metro.txt',
           'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\San Francisco Metro.txt',
           'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\Los Angeles Metro.txt',
           'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\Austin Metro.txt']

outfiles = ['C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\Seattle_clicks.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\Boston_clicks.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\NO_clicks.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\SF_clicks.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\LA_clicks.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\Cities run1\\Austin_clicks.csv']

for i in range(len(infiles)):
    data = []
    with open(infiles[i], newline='', encoding='utf8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if row[0] == '1':
                data.append(row)
             
    with open(outfiles[i],'w') as resultFile:
        wr = csv.writer(resultFile, delimiter=',')
        wr.writerows(data)

