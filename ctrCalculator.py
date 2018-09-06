# -*- coding: utf-8 -*-
"""
This script takes in the counts for impressions and clicks per tract in each city and calculates ctr per
tract, as well as some further statistics.
"""

import csv
import numpy as np
import matplotlib.pyplot as plt


#Strings for input and output file names
allfiles =['C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\NO allpoints.csv', 
           'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Seattle allpoints.csv',
           'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Boston allpoints.csv',
           'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\LA allpoints.csv',
           'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\SF allpoints.csv',
           'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Austin allpoints.csv']

clickfiles = ['C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\NO clickcounts.csv',
              'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Seattle clickcounts.csv',
              'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Boston clickcounts.csv',
              'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\LA clickcounts.csv',
              'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\SF clickcounts.csv',
              'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Austin clickcounts.csv']

outfiles = ['C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\NO_ctr.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Seattle_ctr.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Boston_ctr.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\LA_ctr.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\SF_ctr.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Austin_ctr.csv']

filteredoutfiles = ['C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\NO_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Seattle_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Boston_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\LA_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\SF_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Austin_ctr_filtered.csv']


ctrs = []
posctrs = []

allpoints = []
clicks = []
output = []
pointsum = [0, 0, 0, 0, 0, 0]
rejections = [0, 0, 0, 0, 0, 0]
tractcount = [0, 0, 0, 0, 0, 0]


for i in range(len(allfiles)):
    allpoints = []
    clicks = []
    output = []
    tempctrs = []
    tempposctrs = []
    tempfilteredctrs = []
    
    
    #read files with all impressions and only clicks respectively
    with open(allfiles[i], newline='', encoding='utf8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            allpoints.append(row)
            output.append(row)
             
    with open(clickfiles[i], newline='', encoding='utf8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            clicks.append(row)
            
    for j in range(1, len(allpoints)):
        tractcount[i] = tractcount[i] + 1
        pointsum[i] = pointsum[i] + int(allpoints[j][9])
        #filter tracts with less than 5 impressions
        if float(allpoints[j][9]) >= 5:
            #calculate ctr
            output[j][9] = float(clicks[j][9])/float(allpoints[j][9])
            #check that tract IDs match and ctr is in correct bounds
            if clicks[j][3] != allpoints[j][3] or output[j][9] >= 1:
                print("WRONG!")
            tempctrs.append(output[j][9])
            if output[j][9] != 0:
                tempposctrs.append(output[j][9])
            tempfilteredctrs.append(output[j])
        else:
            output[j][9] = 0
            rejections[i] = rejections[i] + 1            
            
    #Output all tract ctrs, these files are unused in the analysis
    with open(outfiles[i],'w') as resultFile:
        wr = csv.writer(resultFile, delimiter=',')
        wr.writerows(output)
     
    #output ctr for tracts with more than 5 impressions
    with open(filteredoutfiles[i],'w') as resultFile:
        wr = csv.writer(resultFile, delimiter=',')
        wr.writerows(tempfilteredctrs)
    
    #Create arrays of just ctrs for histograms and statistics    
    ctrs.append(tempctrs)
    posctrs.append(tempposctrs)

for i in range(len(rejections)):
    rejections[i] = float(rejections[i])/tractcount[i] 

titles = ['New Orleans', 'Seattle', 'Boston', 'Los Angeles', 'San Francisco', 'Austin']

#Produce ctr histograms with and without 0 ctr tracts and output other statistics
for i in range(len(ctrs)):

    plt.hist(ctrs[i], bins=100)
    plt.title(titles[i])
    plt.show()
    plt.close()
    plt.hist(posctrs[i], bins=100)
    plt.title(titles[i])
    plt.xlabel("ctr")
    plt.ylabel("# of tracts")
    plt.show()
    plt.close()

    print(titles[i])
    print(np.mean(ctrs[i]))
    print(np.median(posctrs[i]))
    print(np.std(ctrs[i]))
    print(np.min(posctrs[i]))
    print(np.max(ctrs[i]))
    

