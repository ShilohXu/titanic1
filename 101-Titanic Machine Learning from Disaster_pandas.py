import pandas
import csv
import numpy

csv_file_object = csv.reader(open('C:/Users/LZ-SANDY/Desktop/kaggle/101-Titanic Machine Learning from Disaster/train.csv'))
header = csv_file_object.__next__
data=[]

for row in csv_file_object:
    data.append(row)
print(data)