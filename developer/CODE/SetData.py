'''
Description
------------

In all function bellow
df       : DataFrame of one scenario ['GIR,GPR,...']
tol      : is used to avoid problems in detection of the parameter caused by the fluctuation 

'''

from ExtractData import *

import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from scipy.optimize import least_squares



def Vi(df):
    '''
    return the injected volume of the scnario df
    '''
    vi = sum(df['Field GIR'])
    return vi


def t0(df,column='Field GIR', tol=0.1):
    '''
    return   : The day of the start of the injection or production
    column   : Take 'Field GIR' for injection and 'Field GPR' for production
    '''
    
    m   = max(df[column])  
    return min(df.loc[df[column]>=m-tol*m,column].index)

def tf(df,column='Field GIR', tol=0.):
    '''
    return   : The day of the end of the injection or production
    column   : Take 'Field GIR' for injection and 'Field GPR' for production
    '''
    return min(df.loc[((df[column].index>=(Tcst(df,column)+t0(df,column))) & (df[column]==0)),column].index)

def IsolateCurve(df_all,column='Field GIR'):
    '''
    return a serie where there is just the value of the curve
    that will avoid problems if each scenario have different start and end
    '''
    N = len(df_all)
    
    Isodf_all=[]
    for i in range(N):
        #we iolate the curve of each scenarios
        df= df_all[i]
        val = df.iloc[t0(df,column)-2:tf(df,column)+2][column].values
        n    = len(val)
        Isodf = pd.DataFrame(index=[i for i in range(n)],data = {column: val})
        Isodf_all.append(Isodf)
    
    return Isodf_all

def Tcst(df,column='Field GIR', tol=10.): 
    '''
    return the constante part
    '''
    m   = max(df[column])
    return len(df.loc[ df[column]>=m-tol,column])

def CstPart(df,column):
    '''
    return the serie that contain only the constante part
    '''
    return df.iloc[t0(df,column):t0(df,column)+Tcst(df,column)][column]

def DecPart(df,column):
    '''
    return the serie that contain only the descendent part
    '''
    return df.iloc[t0(df,column)+Tcst(df,column):tf(df,column)][column]



def fun_inj(X, t):
    '''
    the function that is used to approximate the decreasing part in injection
    '''
    t=np.array(t)
    alpha = 1.5
    return (X[0])*t/(t**alpha+(X[1]))

def distance_inj(X, t, y):
    t=np.array(t)
    return fun_inj(X, t) - y   

def fun_prod(X, t):
    '''
    the function that is used to approximate the decreasing part in injection
    '''
    t=np.array(t)
    alpha = 1.5
    return X[0]*t/(pow(t,alpha)+X[1])-t

def distance_prod(X, t, y):
    t=np.array(t)
    return fun_prod(X, t) - y

def ab(df,column,distance,X0=[0,0]):
    '''
    DfDecPart : DataFrame of one scenario ['index,GIR/GPR']
    '''
    serie = DecPart(df,column)
    y     = serie.values
    t     = serie.index
    
    res_lsq = least_squares(distance,X0,args=(t,y))
    
    return [*res_lsq.x]
    
def GXRi(df, column):
    '''
    return GPRi or GIRi depending on the column chosen
    '''
    return max(df[column])

def GIP(df):
    '''
    return GIP depending on the column chosen
    '''
    return df['Field GIP'][t0(df,'Field GIR')]

def Wmax(df):
    return df['Field WPR'].values[t0(df,'Field GPR')+Tcst(df,'Field GPR')]

def Wp(df):
    return sum(df['Field WPR'])

def FilesVerfication(df_all,column='Field GIR'):
    '''
    this function is for the verfication of the function in this file
    '''
    N = len(df_all)
    
    try:
        os.mkdir('VerficationFigures')
        print('Output file created')
    except:
        print('Output file alredy existe')
    
    for i in range(N):   
        df = df_all[i]
        n = len(df)
        y = np.array([0]*n)
        y[t0(df,column):tf(df,column)]=max(df[column])+10
        
        z = np.array([0]*n)
        z[t0(df,column):t0(df,column) + Tcst(df,column)]=max(df[column])+10
        
        fig = plt.figure()
        plt.figure().clear()
        
        plt.plot(df[column])
        plt.plot(y)
        plt.plot(z)
        
        plt.xlabel('Days')
        plt.ylabel(column)
        
      
        
        plt.savefig(f'VerficationFigures\\Verf_t0_tf_Tcst_{i}.png')
        
        plt.figure().clear()
        plt.close()
    
    for i in range(N): 
        plt.figure().clear()
        savefile = f'VerficationFigures\\Verf_ab_{i}.png'
        Verab(df_all[i],savefile,column,True)

    
    return None



def Verab(df,savefile,column='Field GIR',save=False):
    '''
    plot the approximation that was done using least square
    '''
    plt.figure().clear()
    X = ab(df,column,distance_inj)
    
    serie = DecPart(df,column)
    y     = serie.values
    t     = serie.index
    
    yapx  = [fun_inj(X, i) for i in t]
    
    plt.plot(t,yapx,'--r')
    plt.plot(t,y)
    
    if save : plt.savefig(savefile)
    plt.close()
    
    return None

#Main function
def SetData(Directory, column = 'Field GPR',distance = distance_prod,save= True):
    '''
    Do the main function of this file, create the dataframe that will be used by the model
    '''
    extr = extract(Directory)
    df_all = extr
    nall   = len(df_all)
    
    AllAb = np.array([ab(df_all[i],column,distance,X0=[0,0]) for i in range(nall)])
    
    dict_data = {
        'SCN':              [i for i in range(nall)],
        'Lengh':            [len(df_all[i]) for i in range(nall)], 
        'GPRi':             [GXRi(df_all[i],'Field GPR') for i in range(nall)],
        'GIRi':             [GXRi(df_all[i],'Field GIR') for i in range(nall)],
        'GIP':              [GIP(extr[i]) for i in range(nall)],
        'WGV':            [Vi(extr[i]) for i in range(nall)],
        'Tcst':             [Tcst(df_all[i],column) for i in range(nall)],
        't0':               np.array([t0(extr[i],column) for i in range(nall)]),
        'tf':               np.array([tf(extr[i],column) for i in range(nall)]),
        'Period':           np.array([tf(extr[i],column) for i in range(nall)]) - np.array([t0(extr[i],column) for i in range(nall)]),
         'a':               AllAb[:,0],
         'b':               AllAb[:,1],
         'Wmax':            np.array([Wmax(extr[i]) for i in range(nall)]),
         'Wp':            np.array([Wp(extr[i]) for i in range(nall)])
        } 
    
    Data = pd.DataFrame(dict_data)

    if save: 
        Data.to_excel("DataPred.xlsx",
                         sheet_name='Production')
    
    return Data, df_all



if __name__ == '__main__':
    
    '''
    to verifie if the t0, Tcst, tf have the exact value we plot figures
    that are constante beween the days that were deducted and we compare it
    with the reel figures  
    '''
    Directory = "DATA"
    df_all = extract(Directory)
    df = df_all[0]
    FilesVerfication(df_all, 'Field GIR')
    SetData(Directory, 'Field GPR',distance_prod,True)
    