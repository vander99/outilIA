from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor



########################################### 
#                Injection                #                                 
###########################################


deg = 3

'''
GIR, WGV         ---> Tcst,a,b
______________________________
'''


def GIRi_WGV_Tcst(GIR):
    return 0
def GIRi_WGV_a(GIR):
    return 0
def GIRi_WGV_b(GIR):
    return 0


Cfg_GirWgv_a  = ['sk' ,LinearRegression()]
Cfg_GirWgv_b  = ['sk' ,LinearRegression()]
Cfg_GirWgv_Tcst = ['sk',LinearRegression()]


def minmaxfun(x1,y1,x2,y2,x,alpha=1.):
    
    b=(y1*(x1**alpha)-y2*(x2**alpha))/(x1**alpha-x2**alpha)
    a=(y1-b)*(x1**alpha)  
    return a/(pow(x,alpha))+b

'''
GIR,GIP, WGV      ---> Tcst,a,b
_______________________________
'''

def GIRi_GIP_WGV_Tcst(GIR):
    return 0
def GIRi_GIP_WGV_a(GIR):
    return 0
def GIRi_GIP_WGV_b(GIR):
    return 0


Cfg_GirGipWgv_a  = ['sk' ,LinearRegression()]
Cfg_GirGipWgv_b  = ['sk' ,LinearRegression()]
Cfg_GirGipWgv_Tcst = ['sk' ,LinearRegression()]




########################################### 
#                PRODUCTION               #                                 
###########################################

'''
GPR, Vi           ---> Tcst,a,b
______________________________
'''



def GPRi_WGV_Tcst(GIR, WGV):
    return 0
def GPRi_WGV_a(GIR, WGV):
    return 0
def GPRi_WGV_b(GIR, WGV):
    return 0


Cfg_GprWgv_a    = ['sk' ,LinearRegression()]
Cfg_GprWgv_b    = ['sk' ,LinearRegression()]
Cfg_GprWgv_Tcst = ['sk' ,LinearRegression()]

'''
GPR,GIP, Vi        ---> Tcst,a,b
_______________________________
'''


def GPRi_GIP_WGV_Tcst(GPR,GIP,WGV):
    return 0
def GPRi_GIP_WGV_a(GPR,GIP,WGV):
    return 0
def GPRi_GIP_WGV_b(GPR,GIP,WGV):
    return 0


Cfg_GprGipWgv_a    = ['sk' ,LinearRegression()]
Cfg_GprGipWgv_b    = ['sk' ,LinearRegression()]
Cfg_GprGipWgv_Tcst = ['sk' ,LinearRegression()]


########################################### 
#            WATER  PRODUCTION            #                                 
###########################################


'''
GPR,GIP, Vi        ---> Wmax,Wprod
___________________________________
'''


def GPRi_GIP_WGV_Wmax(GIR,GIP,WGV):
    return 0
def GPRi_GIP_WGV_Wp(GIR,GIP,WGV):
    return 0

Cfg_GprGipWgv_Wmax    = ['sk' ,LinearRegression()]
Cfg_GprGipWgv_Wp      = ['sk' ,LinearRegression()]

if __name__ == '__main__':
    print('test')