#!/usr/bin/python3

import pandas as pd

__all__ = ["get_data"]

DATA_FOLDER = "./data"

def read_column_names(file):
    with open(file, 'r') as f:
        content = f.readlines()
    
    return [x.strip() for x in content]

def get_data():    
    columns_names = read_column_names('./data/header.txt')
    df_smt = pd.read_csv('./data/s_m_t_2020.csv', names=columns_names[1:], index_col=False)

    return df_smt

get_data()