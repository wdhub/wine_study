# classify datasets
# feature for now: most frequent words
# inbalance methods: weighted svm, ensemble of Bayesian

import utility


# read data, sort
fileName="data_en.csv" # "I:/HCI_KTH/big data/project/codes/wine_study/wine/data_en.csv"
comments, labels=utility.readCSV(fileName, 3,4)


# extract features from dictionary


# devide into train and test

# train, evaluate