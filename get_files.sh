#!/bin/bash

MAIN_FILE=./data/s_m_t.csv
CITY_FILE=./data/s_m_t_$1.csv

if [ -z $1 ] ; then
    echo "First parameter needed!" && exit 1;
fi

if [ -f "$CITY_FILE" ] ; then
    echo "$CITY_FILE already exists."
    exit 0
fi
if [ -f "$MAIN_FILE" ] ; then
    echo "$MAIN_FILE exists, generating file for concrete city."
    #get data of single city
    grep -i $1 ./data/s_m_t.csv > ./data/s_m_t_$1.csv
    exit 0
fi

#download all zipped data into ./temp forder
wget -q -r -l1 --no-directories --no-parent -A "*.zip" https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/20{19..20}/ -P ./temp/

#unzip all
for FILE in ./temp/*.zip
do
    unzip -o -d ./temp/ $FILE
done

#remove zipped fordels and unnecessairy csv files
rm ./temp/*.zip ./temp/k_d_[0-9]*.csv

#concatenate all data to signle file
cat ./temp/*.csv > ./data/s_m_t.csv

#remove temp file
rm -rf ./temp/

#get data of single city
grep -i $1 ./data/s_m_t.csv > ./data/s_m_t_$1.csv