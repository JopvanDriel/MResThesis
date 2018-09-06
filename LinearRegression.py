# -*- coding: utf-8 -*-
"""
This script performs the final linear regression and random forest analysis, and outputs the results
"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import statsmodels.api as sm
from sklearn.ensemble import RandomForestRegressor

censusinfiles = ["C:\\Users\\Jop\\Documents\\Thesis\\census data\\Louisiana\\Features.csv",
                 "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Washington\\Features.csv",
                 "C:\\Users\\Jop\\Documents\\Thesis\\census data\\California\\Features.csv",
                 "C:\\Users\\Jop\\Documents\\Thesis\\census data\\California\\Features.csv",
                 "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Texas\\Features.csv",
                 "C:\\Users\\Jop\\Documents\\Thesis\\census data\\Boston\\Features.csv"]

ctrinfiles = ['C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\NO_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Seattle_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\LA_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\SF_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Austin_ctr_filtered.csv',
            'C:\\Users\\Jop\\Documents\\Thesis\\QGIS stuff\\Boston_ctr_filtered.csv']

census = [[], [], [], [], [], []]
ctr = [[], [], [], [], [], []]
data = [[], [], [], [], [], []]
columnnames = [[], [], [], [], [], []]

#Import data from files
for i in range(len(censusinfiles)):
    #Census data
     with open(censusinfiles[i], newline='', encoding='utf8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if row != []:
                #Some rows have empty fields, likely due to being water areas. These are removed
                if row[8] != '':
                    #row[0] is the tract ID, this needs to be cut slightly to accomodate for differing formats
                    temp = [row[0][5:]]
                    for j in range(1, len(row)):
                        temp.append(row[j])
                    census[i].append(temp)
     
     #advertising data   
     with open(ctrinfiles[i], newline='', encoding='utf8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if row != []:
                #row[3] is tract ID, row[9] is ctr
                ctr[i].append([row[3][7:], row[9]])
                

"""
The following block joins the adversting data and census data tables using pandas dataframes with 
the tract ID set as index in both tables.

The join itself is performed as an inner join to remove tracts which are outside the city or
did not meet the 5 impressions minimum.
"""
for i in range(len(census)):
    columnnames[i] = census[i][0]
    del census[i][0]             
    census[i] = pd.DataFrame(census[i], columns=columnnames[i])
    census[i].set_index(columnnames[i][0], inplace=True)
    ctr[i] = pd.DataFrame(ctr[i])
    ctr[i].set_index(0, inplace=True)
    
    data[i] = census[i].join(ctr[i], how='inner')

finalarrays = [[], [], [], [], [], []]

#Perform transformations on variables to ensure normal distributions
for i in range(len(census)):
    temp = np.transpose(np.array(data[i]))
    for j in range(len(temp)-1):
        for k in range(len(temp[j])):
            temp[j][k] = float(temp[j][k])
            
            if columnnames[i][j] == "Income_Diversity":
                if temp[j][k] != 0:
                    temp[j][k] = log(temp[j][k])
            if columnnames[i][j] == "Talent_Index":
                if temp[j][k] != 0:
                    temp[j][k] = log(temp[j][k])
        #This block can be uncommented to display plot for inspection of the distribution
        """    
        plt.hist(temp[j].tolist(), bins=30)
        plt.title(columnnames[i][j])
        plt.show()
        plt.close()
        """
    #The 8th column holds ctr, which is removed here so that finalarrays holds only features
    finalarrays[i] = np.delete(np.transpose(temp), 8, 1).astype(float)


#Check variance inflation factors and remove correlated features    
for i in range(len(finalarrays)):
    #Columnnames[i][0] is an empty string which needs to be removed
    del columnnames[i][0]
    
    while(True):
        tempmax = 0
        #cycle through features and calculate the VIF for each feature
        for j in range(len(np.transpose(finalarrays[i]))):
            vif = variance_inflation_factor(finalarrays[i].astype(float), j)
            #if the VIF is the largest encountered so far and is greater than 10 the index is stored
            if vif > 10 and vif > tempmax:
                tempmax = vif
                maxindex = j
        #If a VIF greater than 10 was encountered remove the feature with the largest VIF
        if tempmax > 10:
            finalarrays[i] = np.delete(finalarrays[i], maxindex, 1)
            del columnnames[i][maxindex]
        #If no VIF are greater tha 10 the process is done
        else:
            break

vifs = [[], [], [], [], [], []]
variables = []

#Perform linear regression and random forests        
for i in range(len(finalarrays)):
     #recalculate VIFs for inspection
     for j in range(len(np.transpose(finalarrays[i]))):
         vifs[i].append(variance_inflation_factor(finalarrays[i].astype(float), j))
     
     """
     x and y are the features and ctr respectively, x needs to have an extra column of constants to
     allow the chose linear regression package to function correctly
    
     finalarrays is only features, so ctr needs to be taken from an earlier table
     """
     x = add_constant(finalarrays[i])
     y = np.array(data[i].loc[:, 1]).astype(float)
     #Perform linear regression and report results
     ols = sm.OLS(y, x)
     results = ols.fit()
     print(results.summary())
     #Perform random forest and report results
     forest = RandomForestRegressor()
     forest.fit(x, y)
     print(forest.score(x, y))
     print(columnnames[i])
     print(forest.feature_importances_)
