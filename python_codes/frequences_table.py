#!/usr/bin/env python
# coding: utf-8

# In[121]:


#################################################################################################
# CALCULATE FREQUENCY TABLE FOR MULTIPLE VARIABLES INCLUDING PERCENTAGE AND CUMULATIVE PERCENTAGE
# KEY WORDS: FRECUENCIA,FRECUENCIAS,FRECUENCY,COUNT,CONTEO,PERCENTAGE
# AUTHORS: DANIEL J & SONIA S
# DATE: 14 / 02 / 2018
#################################################################################################

#Loading necessary libraries
import datetime
import pandas as pd 
import numpy as np

def frequences_table(col,dataframe):
    #Parameters description:
    #dataframe: Table of frequences to be used in DataFrame format
    #col: Variable name to perform the frequency table method
    #Drop missing values from variable (remove missing, eliminar missing, eliminar NaN, eliminar datos faltantes)
    frequences=dataframe[col].dropna()
    #Calculate percentages of participation
    percentages=np.around(frequences*100/frequences.sum(),2)
    #Calculate cumulative percentages
    cum_percentajes=np.around(100*frequences.cumsum()/frequences.sum(),2)
    #Concatenate variables calculed previously
    frequences=pd.concat([frequences,percentages,cum_percentajes],sort=False,axis=1)
    #Include ID variables
    frequences.insert(loc=0, column='variable', value=col)
    frequences.insert(loc=1, column='values', value=list(frequences.index))
    #Change columns names
    frequences.columns = ['variable','values','count','%','% cum']
    #Calculate maximum participation from categories
    frequences['max_particip']= frequences['%'].max()    
    frequences=pd.DataFrame(frequences)
    
    #Drop duplicates from frecuency table
    frequences_reduced=frequences.drop_duplicates(["variable","max_particip"])
    
    #Include "missing" value if neccesary
    if "missing" not in frequences["values"]:        
        frequences = frequences.append(pd.Series([col, "missing", 0, 0,100,np.asscalar(frequences_reduced.iloc[[0], [5]].values)], index=frequences.columns ), ignore_index=True)

    ret = {
        'frequences': frequences,
        'frequences_reduced': frequences_reduced
    }
    return ret
