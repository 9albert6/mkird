import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from weather_api import *

df = get_data("zakopane")

#tworzenie labeli
value = []
data = df['Suma opadu dzień  [mm]']
data = data.to_numpy()
for row in data:
    if row == 0:
        value.append(0)
    elif row > 0:
        value.append(1)
df['deszcz w dzień']= value

value1 = []
data1 = df['Suma opadu noc   [mm]']
data1 = data1.to_numpy()
for row1 in data1:
    if row1 == 0:
        value1.append(0)
    elif row1 > 0:
        value1.append(1)
df['deszcz w nocy']= value

#wywalenie niepotrzebnych kolumn
df = df.drop(df.columns[11],axis = 1)
df = df.drop(df.columns[11],axis = 1)

#normalizacja danych
columns_to_normalize = [[5],[6],[7],[8],[9],[10]]
normalize_particular_columns(df, columns_to_normalize)

#zmiana formatu daty (potrzebne do predykcji)
date = pd.to_datetime((df['Rok']*10000+df['Miesiąc']*100+df['Dzień']).apply(str),format='%Y%m%d')
df.insert(loc=2, column='Data', value=date)
for i in range(0,3):
    df = df.drop(df.columns[3],axis = 1)

#sortowanie według daty
df.sort_values(by=['Data'], inplace=True)