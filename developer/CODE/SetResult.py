from tkinter.constants import N, Y
import tkinter.filedialog as fd 
import tkinter as tk
import numpy as np  
from SetData  import *
from SetModel import *
from Config   import *
from tkinter import Tk, Label, Button, Radiobutton, IntVar

def SetResult(root,case=0):
    '''
    '''         
     
    if case =="PROD(GPRi,GIP,WGV)":
        Train_directory = fd.askdirectory(parent=root,title='Choose train directory')
        DATA_train,df_train = SetData(Train_directory,'Field GPR',distance_prod,True)
        print("TRAIN DATA IMPORTED")
        Test_directory = fd.askdirectory(parent=root,title='Choose test directory')
        DATA_test, df_test = SetData(Test_directory,'Field GPR',distance_prod,True)
        print("TEST DATA IMPORTED")
        L      = DATA_train.Lengh.values[0]
        t0     = DATA_train.t0.min()
        tf     = DATA_train.tf.values[0]
        Days   = range(0,L)
        
        fTcst  = GprGipWgvTpModel(DATA_train, Cfg_GprGipWgv_Tcst)
        fa     = GprGipWgvaModel(DATA_train, Cfg_GprGipWgv_a)
        fb     = GprGipWgvbModel(DATA_train, Cfg_GprGipWgv_b)
        fwm    = GprGipWgvWmaxModel(DATA_train, Cfg_GprGipWgv_Wmax)
        fwp    = GprGipWgvWpModel(DATA_train, Cfg_GprGipWgv_Wp)        
        

        
        def f(GPR, GIP,WGV):
            print('t0 = ', t0)
            print('tf = ', tf)
            
            Tcst = int(fTcst(GPR,GIP,WGV))

            X = [fa(GPR,GIP,WGV),fb(GPR,GIP,WGV)]
            y    = np.array([0]*L)
            
            y[t0:t0+Tcst] = GPR
            y[t0+Tcst:tf] = [fun_prod(X,t) for t in Days[t0+Tcst:tf]]
            
            n= len(y)
            for i in range(n):
                if y[i]>GPR:
                    print("WARNING : GIR reached :", y[i], "> GIRi= ",GPR)
                    y[i]=GPR
                elif y[i]<0:
                    print("WARNING : GIR <0")
                    y[i]=GPR
                    
            return Tcst,y
        
        
        nts = len(df_test)
        
        AllGpri = DATA_test.GPRi.values
        AllGip = DATA_test.GIP.values
        AllVinj = DATA_test.WGV.values
        AllTcst = DATA_test.Tcst.values
        AllWm   = DATA_test.Wmax.values
        AllWp   = DATA_test.Wp.values
        
        PredTcst = np.array([f(AllGpri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        PredWm = np.array([fwm(AllGpri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        PredWp = np.array([fwp(AllGpri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        
        ErrDec=[]
        for i in range(nts):
            PrdDec  = f(AllGpri[i],AllGip[i],AllVinj[i])[1][t0:t0+AllTcst[i]]
            ReelDec = df_test[i].loc[t0:t0+AllTcst[i]-1,'Field GPR'].values
            
            ErrDec.append(np.mean((ReelDec-PrdDec)/(ReelDec+1))) 
        
        ErrDec= np.mean(np.array(ErrDec))       
        ErrTcst = np.mean((AllTcst - PredTcst)/(AllTcst+1))
        ErrWm = np.mean((AllWm - PredWm)/(AllWm+1))
        ErrWp = np.mean((AllWp - PredWp)/(AllWp+1))
        
        return f,fwm,fwp,df_train,df_test,fwm,fwp,ErrTcst,ErrDec,ErrWm,ErrWp
        

    elif case =="INJ(GIRi,WGV)":
        Train_directory = fd.askdirectory(parent=root,title='Choose train directory')

        DATA_train,df_train = SetData(Train_directory,'Field GIR',distance_prod,False)
        print("TRAIN DATA IMPORTED")

        L      = DATA_train.Lengh.values[0]
#        t0     = DATA_train.t0.values[0]
        
        tf     = DATA_train.tf.values[0]
        Days   = range(0,L)
        t0     = 15
        
        fTcst = GirWgvTpModel(DATA_train, Cfg_GirWgv_Tcst)
        fa    = GirWgvaModel(DATA_train, Cfg_GirWgv_a)
        fb    = GirWgvbModel(DATA_train, Cfg_GirWgv_b)
        fwm    = GprGipWgvWmaxModel(DATA_train, Cfg_GprGipWgv_Wmax)
        fwp    = GprGipWgvWpModel(DATA_train, Cfg_GprGipWgv_Wp) 

        def f(GIR,WGV):
            print('t0 = ', t0)
            print('tf = ', tf)
            
            Tcst = int(fTcst(GIR))

            X = [fa(GIR),fb(GIR)]
            y    = np.array([0]*L)

            y[t0:t0+Tcst] = GIR
            y[t0+Tcst:tf] = [fun_inj(X,t) for t in Days[t0+Tcst:tf]]

            n= len(y)
            for i in range(n):
                if y[i]>GIR:
                    print("WARNING : GIR reached :", y[i], "> GIRi= ",GIR)
                    y[i]=GIR
                elif y[i]<0:
                    print("WARNING : GIR <0")
                    y[i]=GIR
            
            s    = 0
            ifin = 0
            while (s<=WGV) and (ifin<370):
                s=s+y[i]
                ifin+=1
            
            y[ifin:]=0
            return Tcst,y

        Test_directory = fd.askdirectory(parent=root,title='Choose test directory')

        DATA_test, df_test = SetData(Test_directory,'Field GIR',distance_prod,False)
        print("TEST DATA IMPORTED")
        nts = len(df_test)

        AllGiri = DATA_test.GIRi.values
        AllGip = DATA_test.GIP.values
        AllVinj = DATA_test.WGV.values
        AllTcst = DATA_test.Tcst.values

        AllWm   = DATA_test.Wmax.values
        AllWp   = DATA_test.Wp.values
        
        PredTcst = np.array([f(AllGiri[i],AllVinj[i])[0] for i in range(nts)])
        PredWm = np.array([fwm(AllGiri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        PredWp = np.array([fwp(AllGiri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        print("Seating ERROR")
        ErrDec=[]
        for i in range(nts):
            PrdDec  = f(AllGiri[i],AllVinj[i])[1][t0:t0+AllTcst[i]]
            ReelDec = df_test[i].loc[t0:t0+AllTcst[i]-1,'Field GIR'].values
            
            ErrDec.append(np.mean((ReelDec-PrdDec)/(ReelDec+1))) 
        
        ErrDec= np.mean(np.array(ErrDec))       
        ErrTcst = np.mean((AllTcst - PredTcst)/(AllTcst+1))
        ErrWm = np.mean((AllWm - PredWm)/(AllWm+1))
        ErrWp = np.mean((AllWp - PredWp)/(AllWp+1))
        
        return f,fwm,fwp,df_train,df_test,fwm,fwp,ErrTcst,ErrDec,ErrWm,ErrWp
        
    elif case =="INJ(GIRi,GIP,WGV)":
        Train_directory = fd.askdirectory(parent=root,title='Choose train directory')

        DATA_train,df_train = SetData(Train_directory,'Field GIR',distance_prod,False)
        print("TRAIN DATA IMPORTED")
        
        L      = DATA_train.Lengh.values[0]
        t0     = DATA_train.t0.min()
        tf     = DATA_train.tf.values[0]
        Days   = range(0,L)
        
        fTcst = GirGipWgvTpModel(DATA_train, Cfg_GirGipWgv_Tcst)
        fa    = GirGipWgvaModel(DATA_train, Cfg_GirGipWgv_a)
        fb    = GirGipWgvbModel(DATA_train, Cfg_GirGipWgv_b)
        fwm   = GprGipWgvWmaxModel(DATA_train, Cfg_GprGipWgv_Wmax)
        fwp   = GprGipWgvWpModel(DATA_train, Cfg_GprGipWgv_Wp)  
        
        print('t0 = ', t0)
        print('tf = ', tf)
        
        def f(GIR, GIP,WGV):
            
            print('t0 = ', t0)
            print('tf = ', tf)
            
            Tcst = int(fTcst(GIR,GIP))

            X = [fa(GIR,GIP),fb(GIR,GIP)]
            y    = np.array([0]*L)
            
            y[t0:t0+Tcst] = GIR
            y[t0+Tcst:tf] = [fun_inj(X,t) for t in Days[t0+Tcst:tf]]
            
            n= len(y)
            for i in range(n):
                if y[i]>GIR:
                    print("WARNING : GIR reached :", y[i], "> GIRi= ",GIR)
                    y[i]=GIR
                elif y[i]<0:
                    print("WARNING : GIR <0")
                    y[i]=GIR
                    
            s    = 0
            ifin = 0
            while (s<=WGV) and (ifin<370):
                s=s+y[i]
                ifin+=1
            
            y[ifin:]=0
            
            return Tcst,y
        
        Test_directory = fd.askdirectory(parent=root,title='Choose test directory')

        DATA_test, df_test = SetData(Test_directory,'Field GIR',distance_prod,False)
        print("TEST DATA IMPORTED")
        nts = len(df_test)
        print("Seating ERROR")
        AllGiri = DATA_test.GIRi.values
        AllGip = DATA_test.GIP.values
        AllVinj = DATA_test.WGV.values
        AllTcst = DATA_test.Tcst.values
        
        AllWm   = DATA_test.Wmax.values
        AllWp   = DATA_test.Wp.values
        
        PredTcst = np.array([f(AllGiri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        PredWm = np.array([fwm(AllGiri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        PredWp = np.array([fwp(AllGiri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        print("Seating ERROR")
        ErrDec=[]
        for i in range(nts):
            PrdDec  = f(AllGiri[i],AllGip[i],AllVinj[i])[1][t0:t0+AllTcst[i]]
            ReelDec = df_test[i].loc[t0:t0+AllTcst[i]-1,'Field GIR'].values
            
            ErrDec.append(np.mean((ReelDec-PrdDec)/(ReelDec+1))) 
        
        ErrDec= np.mean(np.array(ErrDec))       
        ErrTcst = np.mean((AllTcst - PredTcst)/(AllTcst+1))
        ErrWm = np.mean((AllWm - PredWm)/(AllWm+1))
        ErrWp = np.mean((AllWp - PredWp)/(AllWp+1))
        
        return f,fwm,fwp,df_train,df_test,fwm,fwp,ErrTcst,ErrDec,ErrWm,ErrWp
    
    else:
        Train_directory = fd.askdirectory(parent=root,title='Choose train directory')

        DATA_train,df_train = SetData(Train_directory,'Field GPR',distance_prod,False)
        print("TRAIN DATA IMPORTED")
        L      = DATA_train.Lengh.values[0]
        t0     = DATA_train.t0.min()
        tf     = DATA_train.tf.values[0]
        Days   = range(0,L)
        fTcst = GprWgvTpModel(DATA_train, Cfg_GprWgv_Tcst)
        fa    = GprWgvaModel(DATA_train, Cfg_GprWgv_a)
        fb    = GprWgvbModel(DATA_train, Cfg_GprWgv_b)
        fwm    = GprGipWgvWmaxModel(DATA_train, Cfg_GprGipWgv_Wmax)
        fwp    = GprGipWgvWpModel(DATA_train, Cfg_GprGipWgv_Wp)          

        
        def f(GPR, WGV):
            
            print('t0 = ', t0)
            print('tf = ', tf)
            
            Tcst = int(fTcst(GPR, WGV))

            X = [fa(GPR, WGV),fb(GPR, WGV)]
            y    = np.array([0]*L)
            
            y[t0:t0+Tcst] = GPR
            y[t0+Tcst:tf] = [fun_prod(X,t) for t in Days[t0+Tcst:tf]]
            
            n= len(y)
            for i in range(n):
                if y[i]>GPR:
                    print("WARNING : GPR reached :", y[i], "> GPRi= ",GPR)
                    y[i]=GPR
                elif y[i]<0:
                    print("WARNING : GPR <0")
                    y[i]=GPR
                    
            
            return Tcst,y
            
        Test_directory = fd.askdirectory(parent=root,title='Choose test directory')

        DATA_test, df_test = SetData(Test_directory,'Field GPR',distance_prod,False)
        print("TEST DATA IMPORTED")
        nts = len(df_test)
        print("Seating ERROR")
        AllGpri = DATA_test.GPRi.values
        AllVinj = DATA_test.WGV.values
        AllTcst = DATA_test.Tcst.values
        AllGip = DATA_test.GIP.values        
        AllWm   = DATA_test.Wmax.values
        AllWp   = DATA_test.Wp.values
        
        PredTcst = np.array([f(AllGpri[i],AllVinj[i])[0] for i in range(nts)])
        PredWm = np.array([fwm(AllGpri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])
        PredWp = np.array([fwp(AllGpri[i],AllGip[i],AllVinj[i])[0] for i in range(nts)])

        print("Seating ERROR")
        ErrDec=[]
        for i in range(nts):
            PrdDec  = f(AllGpri[i],AllVinj[i])[1][t0:t0+AllTcst[i]]
            ReelDec = df_test[i].loc[t0:t0+AllTcst[i]-1,'Field GPR'].values
            
            ErrDec.append(np.mean((ReelDec-PrdDec)/(ReelDec+1))) 
        
        ErrDec= np.mean(np.array(ErrDec))       
        ErrTcst = np.mean((AllTcst - PredTcst)/(AllTcst+1))
        ErrWm = np.mean((AllWm - PredWm)/(AllWm+1))
        ErrWp = np.mean((AllWp - PredWp)/(AllWp+1))
        
        return f,fwm,fwp,df_train,df_test,fwm,fwp,ErrTcst,ErrDec,ErrWm,ErrWp
    
 
    




def DecrErr(X,fun,t,y):
    '''
    '''
    yapp = np.array([fun(X,i) for i in t])
    y = np.array(y)
    
    Err = abs(y-yapp)/y
    
    return Err


    
    



if __name__ == '__main__':
    root = tk.Tk()
    # f ,err= SetResult(root)
    # TT,YY = f(3093.088013,239101.7286)
    # print('plateau = ', TT)
    # print("\nError\n",err)
    # plt.plot(YY)
    # plt.show()