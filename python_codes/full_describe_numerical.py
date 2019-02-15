#!/usr/bin/env python
# coding: utf-8

# In[121]:


############################################################################
# CALCULATE SUMMARY STATISTICS FOR NUMERICAL VARIABLES
# KEY WORDS: UNIVARIATE,UNIVARIADO,DESCRIPTIVE ANALYSIS,ANALISIS DESCRIPTIVO,
# DESCRIBIR, EXPLORATORY ANALYSIS, ANALISIS EXPLORATORIO
# AUTHORS: DANIEL J & SONIA S
# DATE: 13 / 02 / 2018
############################################################################

#Loading necessary libraries
import datetime
import pandas as pd 
import numpy as np

def full_describe_numerical(dataframe,variables="all",variability=20,completeness=10):
    #Parameters description:
    #dataframe: Table to be used in DataFrame format
    #variables: Variables to perform the describe method. Available values: "all", type sequence (ie. '1:8'), 
    #type lis of numbers or variables labels (ie. '1,4,9' o 'var1,var2,var3')
    #completeness: Minimum completeness accepted for variables (value betwen 0 y 100)
    #variability: Minimum variablility accepted for variables (ie. 0,2,10,20,50,100)
    print("Describe procedure starts, Time: "+ datetime.datetime.now().strftime("%H:%M:%S"))
    start1 = datetime.datetime.now()
    inicial_varnames=dataframe.columns
    dataframe=dataframe.select_dtypes(include='number')
    if variables == "all": #If desired for all the variables
        #Calculate describe adding (concatenar,concatenate) the missing count
        summary=pd.concat([dataframe.describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.isnull().sum().to_frame(name = 'missing').T],sort=False)
    elif ":" in variables: #If desired for sequence of variables n1:n2
        #Calculate describe adding (concatenar,concatenate) the missing count
        variables_serie=list(pd.to_numeric((variables).split(':')))
        variables_serie=list(pd.Series(range(variables_serie[0],variables_serie[1])))
        summary=pd.concat([dataframe.iloc[:,variables_serie].describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.iloc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
    else:
        try: #If desired for numeric array (posiciones,positions) of variables [n1,n2,n3,...]
            # Dividir valor de variables por coma, creando lista numerica
            variables_serie=list(pd.to_numeric((variables).split(',')))
            #Calculate describe adding (concatenar,concatenate) the missing count
            summary=pd.concat([dataframe.iloc[:,variables_serie].describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.iloc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
        except: 
            # Create list from string separated for comma
            variables_serie=list(variables.split(","))
            # Check if exists any column name which doesn't exist in the dataframe (in,contains,contiene,valor en)
            if set(list(variables_serie)).issubset(list(inicial_varnames)):
                #Leave only the column names that exist in the dataframe (intersection,interseccion,valores comunes,common values)
                variables_serie=list(set(variables_serie) & set(dataframe.columns))
            if set(list(variables_serie)).issubset(list(dataframe.columns)): #If desired for string array (colomn names) of variables ['nam1','nam2','nam3',...]
                #Calculate describe adding (concatenar,concatenate) the missing count
                summary=pd.concat([dataframe.loc[:,variables_serie].describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.loc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
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
        #Calulation of variability
        summary['variability'] = np.where(summary['min']==summary['max'], '00_variation', 
                                           np.where(summary['1%']==summary['99%'], '02_variation', 
                                                   np.where(summary['5%']==summary['95%'], '10_variation', 
                                                           np.where(summary['10%']==summary['90%'], '20_variation', 
                                                                   np.where(summary['25%']==summary['75%'], '50_variation', 
                                                                           'high_variability')))))
        if variability == 0:
            summary['decision_variability'] = "accept"
        elif variability == 2:
            summary['decision_variability'] = np.where(summary['variability']=='00_variation', 'reject',
                                                        'accept')
        elif variability == 10:
            summary['decision_variability'] = np.where((summary['variability']=='00_variation') | (summary['variability']=='02_variation'), 'reject',
                                                        'accept')
        elif variability == 20:
            summary['decision_variability'] = np.where((summary['variability']=='00_variation') | (summary['variability']=='02_variation') | (summary['variability']=='10_variation'), 'reject',
                                                        'accept')
        elif variability == 50:
            summary['decision_variability'] = np.where((summary['variability']=='00_variation') | (summary['variability']=='02_variation') | (summary['variability']=='10_variation') | (summary['variability']=='20_variation'), 'reject',
                                                        'accept')
        elif variability == 100: 
            summary['decision_variability'] = np.where((summary['variability']=='00_variation') | (summary['variability']=='02_variation') | (summary['variability']=='10_variation') | (summary['variability']=='20_variation') | (summary['variability']=='50_variation'), 'reject',
                                                        'accept')
        else:
            summary['decision_variability']="INVALID VALUE"
            print("Invalid entry for parameter 'variability'")
        #Calculation of completeness
        summary['decision_completeness']=np.where(summary['% missing']==0,'accept_100',
                                                 np.where(summary['% missing']>completeness, 'reject','accept')) 
    else:
        summary="Invalid entry for parameter 'variables'"
        
    print("Completeness and variability calculation finished. Elapsed time: "+str((datetime.datetime.now() - start2).seconds)+" secs")
    
    
    print("Calculation of whole process finished. Total elapsed time: "+str((datetime.datetime.now() - start1).seconds)+" secs")
    print("Input parameters: variables='"+str(variables)+"', variability= "+str(variability)+", completeness="+str(completeness))
    
    return summary

