#!/usr/bin/python3

import pandas as pd

__all__ = ["get_data"]

DATA_FOLDER = "./data"

def read_column_names(file):
    with open(file, 'r') as f:
        content = f.readlines()
    
    return [x.strip() for x in content]

def delete_mostly_nan_columns(df):
    column_names = list()
    all_entries = len(df.index)
    nan_values = df.isnull().sum().to_numpy()

    for i in range(len(nan_values)):
        if (nan_values[i]/all_entries)>=0.3:
            column_names.append(df.columns[i])

    for name in column_names:
        if name in df.columns:
            del df[name]

def normalize_particular_columns(df, column_names):
    for col_name in column_names:
        df.iloc[:,col_name]=(df.iloc[:,col_name]-df.iloc[:,col_name].mean())/df.iloc[:,col_name].std()

def get_data():    
    columns_names = read_column_names('./data/header.txt')
    df_smt = pd.read_csv('./data/s_m_t_2020.csv', names=columns_names[1:], index_col=False)

    delete_mostly_nan_columns(df_smt)
    columns_to_normalize = [[4],[5],[6],[7],[8],[9],[10],[11],[12]]
    normalize_particular_columns(df_smt, columns_to_normalize)
    print(df_smt.head(10))
    return df_smt