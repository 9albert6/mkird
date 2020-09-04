#!/usr/bin/python3

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
from weather_api import get_data, read_column_names
from statsmodels.tsa.arima_model import ARMA


df = get_data("zakopane")

#funkcja do normalizacji kolumn
def normalize_particular_columns(df, column_names):
    for col_name in column_names:
        df.iloc[:,col_name]=(df.iloc[:,col_name]-df.iloc[:,col_name].mean())/df.iloc[:,col_name].std()

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


#zmiana formatu daty (potrzebne do predykcji)
date = pd.to_datetime((df['Rok']*10000+df['Miesiąc']*100+df['Dzień']).apply(str),format='%Y%m%d')
df.insert(loc=2, column='Data', value=date)
for i in range(0,3):
    df = df.drop(df.columns[3], axis = 1)

#sortowanie według daty
df.sort_values(by=['Data'], inplace=True)

#przewidywanie przyszłych parametrów
def make_predict(nazwa_kolumny, ilosc_dni):
    df2 = df[['Data', nazwa_kolumny]]
    df2.index = pd.DatetimeIndex(df2['Data'])
    model = ARMA(df2[nazwa_kolumny], order=(4, 2))
    model_fit = model.fit(disp=False)
    forecast = model_fit.predict(len(df2), len(df2)+ilosc_dni)
    return forecast

#stworzenie zbioru danych z prewidywanymi parametrami
predicted_data = [] 
predicted_data.append(make_predict('Średnie dobowe zachmurzenie ogólne [oktanty]', 7))
predicted_data.append(make_predict('Średnia dobowa prędkość wiatru [m/s]', 7))
predicted_data.append(make_predict('Średnia dobowa temperatura [°C]', 7))
predicted_data.append(make_predict('Średnia dobowe ciśnienie pary wodnej [hPa]', 7))
predicted_data.append(make_predict('Średnia dobowa wilgotność względna [%]', 7))
predicted_data.append(make_predict('Średnia dobowe ciśnienie na poziomie stacji [hPa]', 7))

#przygotowanie zbioru testowego
df1 = pd.DataFrame(predicted_data, index=['Średnie dobowe zachmurzenie ogólne [oktanty]', 'Średnia dobowa prędkość wiatru [m/s]', 'Średnia dobowa temperatura [°C]','Średnia dobowe ciśnienie pary wodnej [hPa]','Średnia dobowa wilgotność względna [%]','Średnia dobowe ciśnienie na poziomie stacji [hPa]'])
df1 = df1.T

#normalizacja danych 
columns_to_normalize = [[5],[6],[7],[8],[9],[10]]
normalize_particular_columns(df, columns_to_normalize)

#normalizacja danych testowych
columns_to_normalize1 = [[0], [1], [2], [3], [4], [5]]
normalize_particular_columns(df1, columns_to_normalize1)

#dane treningowe
X = df[[df.columns[3], df.columns[4], df.columns[5] ,df.columns[6], df.columns[7], df.columns[8]]]
y = df[[df.columns[11]]]

Xtrain, Xtest, ytrain, ytest  = train_test_split(X, y, test_size=0.2, random_state=42)

#Model SVN
clf= svm.SVC(kernel='linear', C=1.0)
clf.fit(Xtrain, ytrain.values.ravel())

ypred = clf.predict(Xtest)
clf_score = clf.score(Xtest, ytest)

#Model regresji liniowej
logistic_regression= LogisticRegression()
logistic_regression.fit(Xtrain, ytrain.values.ravel())
y_pred_r=logistic_regression.predict(Xtest)
    
accur = accuracy_score(ytest, y_pred_r)

#Model KNN
knn = KNeighborsClassifier()

knn.fit(Xtrain, ytrain.values.ravel())
y_pred_knn = knn.predict(Xtest)
accurKNN = accuracy_score(ytest, y_pred_knn)

#Wyniki predykcji
result_knn = knn.predict(df1)
result_log = logistic_regression.predict(df1)
result_svn = clf.predict(df1)

#funkcja zwracająca procent proprawnosci prognozy
def return_accurancy_score():
    return accurKNN,accur,clf_score 

#funkcja zwracająca listę 0,1 - deszcz/brak deszczu
def return_predicted_labels():
    return [result_knn, result_log, result_svn]

#funkcja zwracająca listę dat
def return_datetime():
    return df1.index.strftime('%d/%m/%Y').to_numpy()



print(return_predicted_labels())

