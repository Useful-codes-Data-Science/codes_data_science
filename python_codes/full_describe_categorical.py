#!/usr/bin/env python
# coding: utf-8

# In[14]:


############################################################################
# CALCULATE SUMMARY STATISTICS FOR CATEGORICAL VARIABLES
# KEY WORDS: UNIVARIATE,UNIVARIADO,DESCRIPTIVE ANALYSIS,ANALISIS DESCRIPTIVO,
# DESCRIBIR, EXPLORATORY ANALYSIS, ANALISIS EXPLORATORIO
# AUTHORS: DANIEL J & SONIA S
# DATE: 13 / 02 / 2018
############################################################################

#Loading necessary libraries
import datetime
import pandas as pd 
import numpy as np
from Functions.frequences_table import *

def full_describe_categorical(dataframe,variables="all",variability=20,completeness=10,h_cardinality=50):
    #Parameters description:
    #dataframe: Table to be used in DataFrame format
    #variables: Variables to perform the describe method. Available values: "all", type sequence (ie. '1:8'), 
    #type lis of numbers or variables labels (ie. '1,4,9' o 'var1,var2,var3')
    #completeness: Minimum completeness accepted for variables (value betwen 0 y 100)
    #variability: Minimum variablility accepted for variables (ie. 0,2,10,20,50,100)
    #h_cardinality: Value to establish when a variable has high cardinality problems
    print("Describe procedure starts, Time: "+ datetime.datetime.now().strftime("%H:%M:%S"))
    start1 = datetime.datetime.now()
    inicial_varnames=dataframe.columns
    dataframe=dataframe.select_dtypes(include='object')
    if variables == "all": #If desired for all the variables
        #Calculate describe adding (concatenar,concatenate) the missing count
        summary=pd.concat([dataframe.describe(include="all"), dataframe.isnull().sum().to_frame(name = 'missing').T],sort=False)
    elif ":" in variables: #If desired for sequence of variables n1:n2
        #Calculate describe adding (concatenar,concatenate) the missing count
        variables_serie=list(pd.to_numeric((variables).split(':')))
        variables_serie=list(pd.Series(range(variables_serie[0],variables_serie[1])))
        summary=pd.concat([dataframe.iloc[:,variables_serie].describe(include="all"), dataframe.iloc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
    else:
        try: #If desired for numeric array (posiciones,positions) of variables [n1,n2,n3,...]
            # Dividir valor de variables por coma, creando lista numerica
            variables_serie=list(pd.to_numeric((variables).split(',')))
            #Calculate describe adding (concatenar,concatenate) the missing count
            summary=pd.concat([dataframe.iloc[:,variables_serie].describe(include="all"), dataframe.iloc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
        except: 
            # Create list from string separated for comma
            variables_serie=list(variables.split(","))
            # Check if exists any column name which doesn't exist in the dataframe (in,contains,contiene,valor en)
            if set(list(variables_serie)).issubset(list(inicial_varnames)):
                #Leave only the column names that exist in the dataframe (intersection,interseccion,valores comunes,common values)
                variables_serie=list(set(variables_serie) & set(dataframe.columns))
            if set(list(variables_serie)).issubset(list(dataframe.columns)): #If desired for string array (colomn names) of variables ['nam1','nam2','nam3',...]
                #Calculate describe adding (concatenar,concatenate) the missing count
                summary=pd.concat([dataframe.loc[:,variables_serie].describe(include="all"), dataframe.loc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
            else: #Garbage Collector in other case
                summary="Invalid entry for 'variables' parameter"
                
    print("Describe procedure finished. Elapsed time: "+str((datetime.datetime.now() - start1).seconds)+" secs")
    
    start2 = datetime.datetime.now()
    print("Starts completeness and variability calculation, Time: "+ datetime.datetime.now().strftime("%H:%M:%S"))
    if isinstance(summary, pd.DataFrame)==True: #Verifiying if there is any error in the parameters and checking ig summary was created
        #Calculate total count
        summary.loc['total count']=summary.loc[['count','missing']].sum()
        #Calculation of percentage of missing
        summary.loc['% missing']=np.around((summary.loc['missing']*100/summary.loc['total count']).astype(np.double),4)
                
        #Transpose data
        summary=summary.T

        #Include ID variables
        summary.insert(loc=0, column='variable', value=list(summary.index))

        #Calculation of variability
        #Fill NaN values with "missing" category (rellenar misssing, fill missing, imputar missing)
        dataframe=dataframe.fillna("missing")
        #Calculate frequency table for all variables
        frequences=dataframe.apply(pd.value_counts)

        extended_freq_table=[]
        frequences_reduced=[]
        for column in dataframe: #Iterate over dataframe to calculate frequencies per variable
            extended_freq_table.append(frequences_table(column,frequences)['frequences'])
            frequences_reduced.append(frequences_table(column,frequences)['frequences_reduced'])
        
        #Concatenate values from the list in a Dataframe
        extended_freq_table = pd.concat(extended_freq_table, axis=0)
        frequences_reduced = pd.concat(frequences_reduced, axis=0).loc[:,["variable","max_particip"]]
        frequences_reduced['variability'] = np.where(frequences_reduced['max_particip']>=100, '00_variation', 
                                                     np.where(frequences_reduced['max_particip']>=98, '02_variation', 
                                                              np.where(frequences_reduced['max_particip']>=90, '10_variation', 
                                                                       np.where(frequences_reduced['max_particip']>=80, '20_variation', 
                                                                                np.where(frequences_reduced['max_particip']>=50, '50_variation', 
                                                                                         'high_variability')))))

        if variability == 0:
            frequences_reduced['decision_variability'] = "accept"
        elif variability == 2:
            frequences_reduced['decision_variability'] = np.where(frequences_reduced['variability']=='00_variation', 'reject',
                                                        'accept')
        elif variability == 10:
            frequences_reduced['decision_variability'] = np.where((frequences_reduced['variability']=='00_variation') | (frequences_reduced['variability']=='02_variation'), 'reject',
                                                        'accept')
        elif variability == 20:
            frequences_reduced['decision_variability'] = np.where((frequences_reduced['variability']=='00_variation') | (frequences_reduced['variability']=='02_variation') | (frequences_reduced['variability']=='10_variation'), 'reject',
                                                        'accept')
        elif variability == 50:
            frequences_reduced['decision_variability'] = np.where((frequences_reduced['variability']=='00_variation') | (frequences_reduced['variability']=='02_variation') | (frequences_reduced['variability']=='10_variation') | (frequences_reduced['variability']=='20_variation'), 'reject',
                                                        'accept')
        elif variability == 100: 
            frequences_reduced['decision_variability'] = np.where((frequences_reduced['variability']=='00_variation') | (frequences_reduced['variability']=='02_variation') | (frequences_reduced['variability']=='10_variation') | (frequences_reduced['variability']=='20_variation') | (frequences_reduced['variability']=='50_variation'), 'reject',
                                                        'accept')
        else:
            frequences_reduced['decision_variability']="INVALID VALUE"
            print("Invalid entry for parameter 'variability'")
        
        #Join summary and frequences_reduces in one final table    
        summary=summary.set_index('variable').join(frequences_reduced.set_index('variable'))
        
        #Calculation of completeness
        summary['decision_completeness']=np.where(summary['% missing']==0,'accept_100',
                                                 np.where(summary['% missing']>completeness, 'reject','accept')) 
        #Calculation of high cardinality
        summary['decision_high_cardin']=np.where(summary['unique']>h_cardinality,'high_cardinality',
                                                 'accept')

    else:
        summary="Invalid entry for parameter 'variables'"
        
    print("Completeness and variability calculation finished. Elapsed time: "+str((datetime.datetime.now() - start2).seconds)+" secs")
    
    
    print("Calculation of whole process finished. Total elapsed time: "+str((datetime.datetime.now() - start1).seconds)+" secs")
    print("Input parameters: variables='"+str(variables)+"', variability= "+str(variability)+", completeness="+str(completeness)+", h_cardinality="+str(h_cardinality))
    
    ret = {
        'summary': summary,
        'extended_freq_table': extended_freq_table
    }
    return ret
