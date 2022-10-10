# classify datasets
# feature for now: most frequent words
# inbalance methods: weighted Bayesian, ensemble of Bayesian

import utility
import pickle
import extracter
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import class_weight
import numpy as np
from sklearn.metrics import accuracy_score

#settings
extractMethod="freq"# "freq": extract dictionary via frequent words, "cor": via correlated words
datasetName="expensive"

# read data, sort
fileName="data_en_"+datasetName+".csv" # "I:/HCI_KTH/big data/project/codes/wine_study/wine/data_en.csv"
comments, labels=utility.readCSV(fileName, 3,4)
cleanedComments=utility.cleanText(comments)

# devide into train and test
com_train,com_test, y_train, y_test = train_test_split(cleanedComments,labels,test_size=0.25)


# extract features from dictionary

if extractMethod=='cor':
    # read related words
    dataName = "I:/HCI_KTH/big data/project/codes/wine_study/wine/price_words.pkl"
    with open(dataName, 'rb') as load_data:
        data = pickle.load(load_data)
    corDict = data['mid_price']+data['high_price']
    corDict=list(np.unique(corDict))

    X_train=extracter.corExtract(corDict,com_train)
    X_test = extracter.corExtract(corDict, com_test)
else:
    X_train,X_test=extracter.freExtract(com_train,com_test)



# train, evaluate

#weighted Bayesian
# sample_weight
c_w = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
sample_weight=[c_w[i] for i in y_train]
sample_weight=np.array(sample_weight)

# train
y_train=y_train.astype('int')
clf=MultinomialNB().fit(X_train,y_train,sample_weight)
utility.saveData("I:/HCI_KTH/big data/project/codes/wine_study/wine/NBmodel_"+extractMethod+"_"+datasetName+".pkl",clf)

#evaluate
scores=accuracy_score(y_test.astype('int'), clf.predict(X_test))
print("Method: "+extractMethod)
print("Data: "+datasetName)
print("scores: "+str(scores))

# # on cheap data
# dataName = "I:/HCI_KTH/big data/project/codes/wine_study/wine/NBmodel_"+extractMethod+"_"+datasetName+".pkl"
# with open(dataName, 'rb') as load_data:
#     model = pickle.load(load_data)
#
# scores=accuracy_score(y_test.astype('int'), model.predict(X_test))
# print("Method: "+extractMethod)
# print("Data: "+datasetName)
# print("scores: "+str(scores))