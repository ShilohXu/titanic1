# The first thing to do is to import the relevant packages
# that I will need for my script,
# these include the Numpy (for maths and arrays)
# and csv for reading and writing csv files
# If i want to use something from this I need to call
# csv.[function] or np.[function] first

import csv as csv
import numpy as np
# import warnings

# Open up the csv file in to a Python object
csv_file_object = csv.reader(
    open('C:/Users/LZ-SANDY/Desktop/kaggle/101-Titanic Machine Learning from Disaster/train.csv'))

header = csv_file_object.__next__()  # The next() command just skips the first line which is a header
data = []  # Create a variable called 'data'.
for row in csv_file_object:  # Run through each row in the csv file,
    data.append(row)  # adding each row to the data variable
data = np.array(data)  # Then convert from a list to an array

# So we add a ceiling
fare_ceiling = 40
# then modify the data in the Fare column to = 39, if it is greater or equal to the ceiling
data[data[0::, 9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = int(fare_ceiling / fare_bracket_size)

# I know there were 1st, 2nd and 3rd classes on board
number_of_classes = 3

# But it's better practice to calculate this from the data directly
# Take the length of an array of unique values in column index 2
number_of_classes = len(np.unique(data[0::, 2]))

# Initialize the survival table with all zeros
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

# for i in range(number_of_classes):  # loop through each class
#     for j in range(number_of_price_brackets):  # loop through each price bin
#
#         women_only_stats = data[(data[0::, 4] == "female") & (data[0::, 2].astype(np.float) == i + 1) & (
#             data[0:, 9].astype(np.float) >= j * fare_bracket_size) & (
#                                     data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1]
#
#         men_only_stats = data[(data[0::, 4] != "female") & (data[0::, 2].astype(np.float) == i + 1) & (
#             data[0:, 9].astype(np.float) >= j * fare_bracket_size) & (
#                               data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1]
for i in range(number_of_classes):
    for j in range(number_of_price_brackets):
        women_only_stats = data[(data[0::, 4] == 'female') & (data[0::, 2].astype(np.float) == i + 1) & (
            data[0:, 9].astype(np.float) >= j * fare_bracket_size) & (
                                    data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1]
        men_only_stats = data[(data[0::, 4] != 'female') & (data[0::, 2].astype(np.float) == i + 1) & (
            data[0::, 9].astype(np.float) >= j * fare_bracket_size) & (
                                  data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1]
        survival_table[0, i, j] = np.mean(women_only_stats.astype(np.float))
        survival_table[1, i, j] = np.mean(men_only_stats.astype(np.float))

survival_table[survival_table != survival_table] = 0.

survival_table[survival_table < 0.5] = 0
survival_table[survival_table >= 0.5] = 1

test_file = open('C:/Users/LZ-SANDY/Desktop/kaggle/101-Titanic Machine Learning from Disaster/test.csv', "r")
test_file_object = csv.reader(test_file)
header = test_file_object.__next__()
predictions_file = open(
    "C:/Users/LZ-SANDY/Desktop/kaggle/101-Titanic Machine Learning from Disaster/genderclassmodel2.csv", 'w', newline= '')
p = csv.writer(predictions_file)
p.writerow(["PassengerId", "Survived"])

for row in test_file_object:
    for j in range(number_of_price_brackets):

        try:
            row[8] = float(row[8])
        except:
            bin_fare = 3 - float(row[1])
            break
        if row[8] > fare_ceiling:
            bin_fare = number_of_price_brackets - 1
            break
        if row[8] >= j * fare_bracket_size and row[8] < (j + 1) * fare_bracket_size:
            bin_fare = j
            break
    if row[3] == 'female':  # If the passenger is female
            p.writerow([row[0], "%d" % int(survival_table[0, float(row[1]) - 1, bin_fare])])
    else:
            p.writerow([row[0], "%d" % int(survival_table[1, float(row[1]) - 1, bin_fare])])

# Close out the files.
test_file.close()
predictions_file.close()
