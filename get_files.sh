#!/bin/bash

#donload all zipped data into ./temp forder
wget -q -r -l1 --no-directories --no-parent -A "*.zip" https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/20{19..20}/ -P ./temp/

#unzip all
for FILE in ./temp/*.zip
do
    unzip -o -d ./temp/ $FILE
done

#remove zipped fordels and unnecessairy csv files
rm ./temp/*.zip ./temp/k_d_[0-9]*.csv

cat ./temp/*.csv > ./data/s_m_t.csv

rm -rf ./temp/

grep -i $1 ./data/s_m_t.csv > ./data/s_m_t_$1.csv