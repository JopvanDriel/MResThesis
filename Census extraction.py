# -*- coding: utf-8 -*-
"""
This script serves to take the census tables for a single state and calculate the features for that state.
The .csv files taken in are created by QGIS from the raw databases provided by the US census bureau.

The code can be adjusted for any other city by simply replacing the input and output files to be a new city
"""

import csv

censusfiles = ["C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\01 age sex.csv",
               "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\02 race.csv", 
               "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\11 households.csv",
               "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\15 education.csv",
               "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\17 poverty.csv",
               "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\19 income.csv",
               "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\23 unemployment.csv",
               "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\24 occupation.csv"]

censustables = [[], [], [], [], [], [], [], []]

#Define which attributes are needed
attributes = [["B01001e1", 0],
              ["B01001e8", 0], ["B01001e9", 0], ["B01001e10", 0], ["B01001e11", 0], ["B01001e12", 0], 
              ["B01001e32", 0], ["B01001e33", 0], ["B01001e34", 0], ["B01001e35", 0], ["B01001e36", 0],
              ["B01002e1", 0],
              ["B02001e1", 0], ["B02001e2", 0], ["B02001e3", 0], ["B02001e4", 0], ["B02001e5", 0], 
              ["B02001e6", 0], ["B02001e7", 0], ["B02001e8", 0],
              ["B11001e1", 0],
              ["B15002e1", 0], ["B15002e19", 0],
              ["B15002e15", 0], ["B15002e16", 0], ["B15002e17", 0], ["B15002e18", 0],
              ["B15002e32", 0], ["B15002e33", 0], ["B15002e34", 0], ["B15002e35", 0],
              ["B17001e1", 0],
              ["B17017e2", 0],
              ["B19001e1", 0], ["B19001e2", 0], ["B19001e3", 0], ["B19001e4", 0], ["B19001e5", 0], ["B19001e6", 0],
              ["B19001e7", 0], ["B19001e8", 0], ["B19001e9", 0], ["B19001e10", 0], ["B19001e11", 0], ["B19001e12", 0],
              ["B19001e13", 0], ["B19001e14", 0], ["B19001e15", 0], ["B19001e16", 0], ["B19001e17", 0],
              ["B23025e1", 0],
              ["B23025e5", 0],
              ["C24010e1", 0],
              ["C24010e15", 0],
              ["C24010e51", 0],
              ["B19013e1", 0]]

ordercheck = []
output = []
#read data from files
for i in range(len(censusfiles)):
    with open(censusfiles[i], newline='', encoding='utf8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if i == 0:
                ordercheck.append(row[1])
                output.append([row[1]])
            censustables[i].append(row)
            
#Find indices of relevant attributes in census files
for i in range(len(censustables)):
    for j in range(len(censustables[i])):
        if j == 0:
            for k in range(len(censustables[i][j])):
                for row in attributes:
                    if censustables[i][j][k] == row[0]:
                        row[1] = [i, k]
        else:
            if censustables[i][j][1] != ordercheck[j]:
                print("Wrong")


# read appropriate attributes from census tables
for row in attributes:
    for i in range(len(output)):
        output[i].append(censustables[row[1][0]][i][row[1][1]])


"""
The following blocks calculate the various features to be used later.

Given that the number of rows is relatively small at this point (a few 1000 tracts per city), the
choice is made to separate each feature completely for clarity of the code. For larger numbers of tracts
the blocks could be combined to significantly improve performance.
"""

#Calculate race diversity indices
raceginis = []
for i in range(1, len(output)):
    row = output[i]
    total = 0
    for j in range(13, 21):
        total = total + float(row[j])
    temp = 0
    coeff = 0
    for i in range(13, 21):
        if total != 0:
            temp = (float(row[i])/float(total))**2
            coeff = coeff + temp
    raceginis.append(1 - coeff)
 
#Calculate Income diversity indices       
incomeginis = []
for i in range(1, len(output)):
    row = output[i]
    total = 0
    for j in range(34, 50):
        total = total + float(row[j])
    temp = [0, 0, 0]
    coeff = 0
    for i in range(34, 40):
        temp[0] = temp[0] + float(row[i])
    for i in range(40, 46):
        temp[1] = temp[1] + float(row[i]) 
    for i in range(46, 50):
        temp[2] = temp[2] + float(row[i])
    for i in range(len(temp)):
        if total != 0:
            coeff = coeff + (temp[i]/total)**2
    incomeginis.append(1 - coeff)
 
#Calculate Young people proportions        
youngprops = []
for i in range(1, len(output)):
    row = output[i]
    count = 0
    for j in range(2, 12):
        count = count + float(row[j])
    if float(row[1]) != 0:
        youngprops.append(count/float(row[1]))
    else: youngprops.append(0)

#Calculate talent indices    
talentprops = []
for i in range(1, len(output)):
    row = output[i]
    count = 0
    total = 0
    for j in range(22, 24):
        total = total + float(row[j])
    for j in range(24, 32):
        count = count + float(row[j])
    if total != 0:
        talentprops.append(count/total)
    else: talentprops.append(0)

#Initialize output table with column headers    
table = [["ID", "Race_Diversity", "Income_Diversity", "Talent_Index", "Young_People", "Median_Age", 
          "Poverty", "Unemployment", "Median_Income"]]

"""
Write rows of the output table
Some features are given directly in the census table and need only be normalized, so they are calculated
at this stage.
As before, this can be combined into a single loop with teh fauture calculations if more tracts are
considered.
"""
for i in range(0, len(output)-1):
    temp = [output[i+1][0]]
    temp.append(raceginis[i])
    temp.append(incomeginis[i])
    temp.append(talentprops[i])
    temp.append(youngprops[i])
    temp.append(output[i+1][11])
    if float(output[i+1][32]) != 0:
        temp.append(float(output[i+1][33])/float(output[i+1][32]))
    else: temp.append(0)
    if float(output[i+1][50]) != 0:
        temp.append(float(output[i+1][51])/float(output[i+1][50]))
    else: temp.append(0)
    temp.append(output[i+1][56])
    table.append(temp)
 
#Write output table to file    
with open("C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\Features.csv",'w') as resultFile:
    wr = csv.writer(resultFile, delimiter=',')
    wr.writerows(table)
