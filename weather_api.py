#!/usr/bin/python3

import pandas as pd
import subprocess
import shlex
from platform import system

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
        df[col_name]=(df[col_name]-df[col_name].mean())/df[col_name].std()

def get_data(city_name):    
    columns_names = read_column_names('./data/header.txt')
    if system() is not "Linux":
        sys.exit("ONLY LINUX")
    subprocess.call(shlex.split(f'./get_files.sh {city_name}'))
    df_smt = pd.read_csv(f'./data/s_m_t_{city_name}.csv', names=columns_names[1:], index_col=False)
    delete_mostly_nan_columns(df_smt)
    columns_to_normalize = ['Średnia dobowa temperatura [°C]', 'Status pomiaru TEMP',
       'Status pomiaru WLGS', 'Średnia dobowa prędkość wiatru [m/s]',
       'Status pomiaru FWS', 'Średnie dobowe zachmurzenie ogólne [oktanty]',
       'Status pomiaru NOS']
    normalize_particular_columns(df_smt, columns_to_normalize)
    return df_smt