'''
Description
------------

In all function bellow
df : DataFrame of one scenario ['GIR,GPR,...']

'''

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from Config import *

########################################### 
#                Injection                #                                 
###########################################

'''
GIR, WGV         ---> Tcst,a,b
______________________________
'''


def GirWgvTpModel(DATA_train, Cfg_GirWgv_Tp=['sk',LinearRegression()]):
    '''
    Create function that predict the constant part 
    '''
    if Cfg_GirWgv_Tp[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> Tp: Sklearn') 
        model = Cfg_GirWgv_Tp[1]
        model.fit(DATA_train[["GIRi"]], DATA_train.Tcst)
        return lambda GIRi : model.predict([[GIRi]])
    
    else:        
        GIRiall = DATA_train.GIRi.values
        Tcstall = DATA_train.Tcst.values
        imin = np.argmin(GIRiall)
        imax = np.argmax(GIRiall)
        return lambda x: minmaxfun(GIRiall[imin],Tcstall[imin],GIRiall[imax],Tcstall[imax],x,2)

def GirWgvaModel(DATA_train, Cfg_GirWgv_a=['sk',LinearRegression()]):
    '''
    Create function that predict a 
    '''
    if Cfg_GirWgv_a[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> a: Sklearn') 
        model = Cfg_GirWgv_a[1]
        model.fit(DATA_train[["GIRi"]], DATA_train.a)
        return lambda GIRi : model.predict([[GIRi]])
    
    else:
        return GIRi_WGV_a
    
def GirWgvbModel(DATA_train, Cfg_GirWgv_b=['sk',LinearRegression()]):
    '''
    Create function that predict b
    '''
    if Cfg_GirWgv_b[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> b: Sklearn') 
        model = Cfg_GirWgv_b[1]
        model.fit(DATA_train[["GIRi"]], DATA_train.b)
        return lambda GIRi : model.predict([[GIRi]])
    
    else:
        return GIRi_WGV_b



'''
GIR,GIP, WGV      ---> Tcst,a,b
_______________________________
'''
""
def GirGipWgvTpModel(DATA_train, Cfg_GirWgv_Tp=['sk',LinearRegression()]):
    '''
    Create function that predict the constant part 
    '''
    if Cfg_GirWgv_Tp[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,GIP,WGV --> Tp: Sklearn') 
        model = Cfg_GirWgv_Tp[1]
        model.fit(DATA_train[["GIRi","GIP"]], DATA_train.Tcst)
        return lambda GIRi, GIP: model.predict([[GIRi,GIP]])
    
    else:
        return GIRi_GIP_WGV_Tcst

def GirGipWgvaModel(DATA_train, Cfg_GirWgv_a=['sk',LinearRegression()]):
    '''
    Create function that predict a 
    '''
    if Cfg_GirWgv_a[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> a: Sklearn') 
        model = Cfg_GirWgv_a[1]
        model.fit(DATA_train[["GIRi","GIP"]], DATA_train.a)
        return lambda GIRi,GIP: model.predict([[GIRi,GIP]])
    
    else:
        return GIRi_GIP_WGV_a
    
def GirGipWgvbModel(DATA_train, Cfg_GirWgv_b=['sk',LinearRegression()]):
    '''
    Create function that predict b
    '''
    if Cfg_GirWgv_b[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> b: Sklearn') 
        model = Cfg_GirWgv_b[1]
        model.fit(DATA_train[["GIRi","GIP"]], DATA_train.b)
        return lambda GIRi,GIP : model.predict([[GIRi,GIP]])
    
    else:
        return GIRi_GIP_WGV_b


########################################### 
#                PRODUCTION               #                                 
###########################################

'''
GPR, WGV         ---> Tcst,a,b
______________________________
'''


def GprWgvTpModel(DATA_train, Cfg_GprWgv_Tp=['sk',LinearRegression()]):
    '''
    Create function that predict the constant part 
    '''
    if Cfg_GprWgv_Tp[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> Tp: Sklearn') 
        model = model = make_pipeline(MinMaxScaler(),
                  PolynomialFeatures(3),
                  Cfg_GprWgv_Tp[1])
        model.fit(DATA_train[["GPRi","WGV"]], DATA_train.Tcst)
        return lambda GPRi,WGV : model.predict([[GPRi,WGV]])
    
    else:
        return GPRi_WGV_Tcst

def GprWgvaModel(DATA_train, Cfg_GprWgv_a=['sk',LinearRegression()]):
    '''
    Create function that predict a 
    '''
    if Cfg_GprWgv_a[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GPR,WGV --> a: Sklearn') 
        model = make_pipeline(MinMaxScaler(),
                  PolynomialFeatures(3),
                  Cfg_GprWgv_a[1])
        model.fit(DATA_train[["GPRi","WGV"]], DATA_train.a)
        return lambda GPRi,WGV : model.predict([[GPRi,WGV]])
    
    else:
        return GPRi_WGV_a
    
def GprWgvbModel(DATA_train, Cfg_GprWgv_b=['sk',LinearRegression()]):
    '''
    Create function that predict b
    '''
    if Cfg_GprWgv_b[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> b: Sklearn') 
        model = make_pipeline(MinMaxScaler(),
                  PolynomialFeatures(3),
                  Cfg_GprWgv_b[1])
        model.fit(DATA_train[["GPRi","WGV"]], DATA_train.b)
        return lambda GPRi,WGV : model.predict([[GPRi,WGV]])
    
    else:
        return GPRi_WGV_b
    


'''
GIR,GIP, WGV      ---> Tcst,a,b
_______________________________
'''

def GprGipWgvTpModel(DATA_train, Cfg_GprGipWgv_Tp=['sk',LinearRegression()]):
    '''
    Create function that predict the constant part 
    '''
    if Cfg_GprGipWgv_Tp[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GPR,GIP,WGV --> Tp: Sklearn') 
        model = make_pipeline(MinMaxScaler(),
                  PolynomialFeatures(2),
                  Cfg_GprGipWgv_Tp[1])
        
        model.fit(DATA_train[["GPRi","GIP","WGV"]], DATA_train.Tcst)
        return lambda GPRi, GIP,WGV: model.predict([[GPRi,GIP,WGV]])
    
    else:
        return GPRi_GIP_WGV_Tcst

def GprGipWgvaModel(DATA_train, Cfg_GprGipWgv_a=['sk',LinearRegression()]):
    '''
    Create function that predict a 
    '''
    if Cfg_GprGipWgv_a[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GIR,WGV --> a: Sklearn') 
        model = make_pipeline(MinMaxScaler(),
                  PolynomialFeatures(2),
                  Cfg_GprGipWgv_a[1])
        
        model.fit(DATA_train[["GPRi","GIP","WGV"]], DATA_train.a)
        return lambda GPRi,GIP,WGV: model.predict([[GPRi,GIP,WGV]])
    
    else:
        return GPRi_GIP_WGV_a
    
def GprGipWgvbModel(DATA_train, Cfg_GprGipWgv_b=['sk',LinearRegression()]):
    '''
    Create function that predict b
    '''
    if Cfg_GprGipWgv_b[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GPR,WGV --> b: Sklearn') 
        model = make_pipeline(MinMaxScaler(),
            PolynomialFeatures(2),
            Cfg_GprGipWgv_b[1])
        
        model.fit(DATA_train[["GPRi","GIP","WGV"]], DATA_train.b)
        return lambda GPRi,GIP,WGV : model.predict([[GPRi,GIP,WGV]])
    
    else:
        return GPRi_GIP_WGV_b

########################################### 
#             WATER PRODUCTION            #                                 
###########################################


def GprGipWgvWmaxModel(DATA_train, Cfg_GprGipWgv_Wmax=['sk',LinearRegression()]):
    '''
    Create function that predict Wmax
    '''
    if Cfg_GprGipWgv_Wmax[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GPR,WGV --> Wmax: Sklearn') 
        model = make_pipeline(MinMaxScaler(),
            PolynomialFeatures(2),
            Cfg_GprGipWgv_Wmax[1])
        
        model.fit(DATA_train[["GPRi","GIP","WGV"]], DATA_train.Wmax)
        return lambda GPRi,GIP,WGV : model.predict([[GPRi,GIP,WGV]])
    
    else:
        return GPRi_GIP_WGV_Wmax
    
def GprGipWgvWpModel(DATA_train, Cfg_GprGipWgv_Wp=['sk',LinearRegression()]):
    '''
    Create function that predict Wmax
    '''
    if Cfg_GprGipWgv_Wp[0]=='sk':
        #if the model choosen is in the sklearn librairie
        print('GPR,WGV --> Wp: Sklearn') 
        model = make_pipeline(MinMaxScaler(),
            PolynomialFeatures(2),
            Cfg_GprGipWgv_Wp[1])
        
        model.fit(DATA_train[["GPRi","GIP","WGV"]], DATA_train.Wp)
        return lambda GPRi,GIP,WGV : model.predict([[GPRi,GIP,WGV]])
    
    else:
        return GPRi_GIP_WGV_Wp






