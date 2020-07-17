#!/usr/bin/python3

import urllib.request
import pandas as pd
from pathlib import Path
import zipfile

SITE_URL_SYNOP = "https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/miesieczne/synop/2020/2020_m_s.zip"
SITE_URL_HEADER = "https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/miesieczne/synop/s_m_t_format.txt"


def get_data():
    Path("./data").mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(SITE_URL_SYNOP, './data/2020_m_s.zip')
    urllib.request.urlretrieve(SITE_URL_HEADER, './data/header.txt')


    with zipfile.ZipFile('./data/2020_m_s.zip', 'r') as zip_ref:
        zip_ref.extractall('./data')

    df_smt = pd.read_csv('./data/s_m_t_2020.csv', encoding='iso-8859-2', header=None)

    print(df_smt.sample(10))
    
    return df_smt
get_data()
