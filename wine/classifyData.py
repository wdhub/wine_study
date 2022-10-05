# classify datasets
# feature for now: most frequent words
# inbalance methods: weighted Bayesian, ensemble of Bayesian

import utility
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.utils import class_weight
import numpy as np
from sklearn.metrics import accuracy_score

# read data, sort
fileName="data_en.csv" # "I:/HCI_KTH/big data/project/codes/wine_study/wine/data_en.csv"
comments, labels=utility.readCSV(fileName, 3,4)
cleanedComments=utility.cleanText(comments)

# devide into train and test
com_train,com_test, y_train, y_test = train_test_split(cleanedComments,labels,test_size=0.25)


# extract features from dictionary
# --------------to be updated-----------------
# get dictionary
model = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
model = model.fit(com_train)
# extract features
X_train=model.transform(com_train).toarray()
X_test=model.transform(com_test).toarray()



# train, evaluate

#weighted Bayesian
# sample_weight
c_w = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
sample_weight=[c_w[i] for i in y_train]
sample_weight=np.array(sample_weight)

# train
y_train=y_train.astype('int')
clf=MultinomialNB().fit(X_train,y_train,sample_weight)

#evaluate
scores=accuracy_score(y_test.astype('int'), clf.predict(X_test))