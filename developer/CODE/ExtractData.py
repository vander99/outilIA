#
# Fichier de fonctions pour extraire les données d'un/plusieurs excels et les nettoyer
#

import pandas as pd
from os import listdir
from os.path import isfile, join

def extract_excel(file):
    """"Extrait un dataframe à partir d'un fichier excel standard"""
    df = pd.read_excel(file, skiprows=[0,1,2,4], usecols="D,F,C,E")
    df = df.dropna()
    return(df)


def remove_dates(df):
    """"
    Accepte un dataframe et lui supprime les colonnes 'Daily granularity' et 'YEAR'
    """
    try:
        res = df.drop(['Field GIP','Field WPR','Daily granularity', 'YEAR'], axis = 1)
    except:
        res = df
    return(res)

def maximum(list_df):
    """"
    Accepte une liste de dataframes et retourne la longueur du dataframe le plus long et son indice
    """
    maxi = len(list_df[0])
    i = 0
    res = [maxi, i]
    for df in list_df[1:] :
        i = i + 1
        if len(df) > maxi :
            maxi = len(df)
            res = [maxi, i]
    return res

def merge_inj(list_df):
    """"
    Accepte une liste de dataframes, les fusionne et retourne en résultat un dataframe
    Garde tous les scénarii d'injection même si aucun scénario de production s'ensuit
    """
    new_df = list_df[maximum(list_df)[1]]
    i = 0
    for df in list_df:
        if i == maximum(list_df)[1]:
            new_df = new_df
        else:
            new_df = new_df.merge(df, left_index=True, right_index=True)
        i = i + 1
    return(new_df)

def merge_prod(list_df):
    """"
    Accepte une liste de dataframes, les fusionne et retourne en résultat un dataframe
    Certains scénarii d'injection n'ont que 260 valeurs, nous les enlèveront donc pour ne pas tronquer la production
    """
    new_df=list_df[maximum(list_df)[1]]
    i = 0
    for df in list_df:
        if i == maximum(list_df)[1]:
            new_df = new_df
        elif len(df) < maximum(list_df)[0]:
            new_df = new_df
        else:
            new_df = new_df.merge(df, left_index=True, right_index=True)
        i = i + 1
    return(new_df)

def findFiles(directory):
    """"
    Accepte une chaine de charactère correspondant à un directory et retourne une liste contenant l'ensemble des noms de fichiers
    """
    fichiers = [f for f in listdir(directory) if isfile(join(directory, f))]
    return(fichiers)

def multi_extract_excel(directory):
    """
    Retourne une liste contenant les dataframes associés aux excels du dossier 'directory'
    
    !! Veillez à ce qu'il n'y ai que des excels dans le dossier !!

    :param: directory: un dossier contenant UNIQUEMENT des excels
    :return: df_list: une liste de dataframe. Ces derniers étant chacun associé à un excel
    """
    fichiers = findFiles(directory)
    liste_dataframes = [extract_excel(directory+"/"+fichier) for fichier in fichiers]

    return(liste_dataframes)

def CleanProd(df1):
    df1.loc[0:100,'Field GPR'] = 0
    return df1
    

def extract(directory):
    
    df_all = multi_extract_excel(directory)
    
    n = len(df_all)
    df1 = [CleanProd(remove_dates(df_all[i])) for i in range(n)]
    
    return df1

if __name__ == '__main__':
    
    import matplotlib.pyplot as plt 
    import win32com.client as win32
   
    directory="DATAV2-14012021"
    fichiers=findFiles("DATAV2-14012021")
    print(fichiers[0])
    df=extract_excel(directory+"/"+fichiers[0])

    list_df = extract(directory)
    
    
    list_df[0].to_excel('liste_df[0].xlsx')
    
    prod_df = merge_prod(list_df)
    inje_df = merge_inj(list_df)
    
    print("\n le premier dataframe  \n", list_df[0])
    print ("\n -------------------------------------- \n")
    print("\n production  \n", prod_df.columns)
    print ("\n -------------------------------------- \n")
    print("\n production  \n", inje_df.columns)
    

