# train & evaluate Bayesian classifier
# use preprocessed data

from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.metrics import accuracy_score
import pickle

#prepare path
filePath="I:/HCI_KTH/big data/project/codes/wine_study/lab"
dataName=filePath+'/'+"data.pkl"
trainName='train.csv'
testName='test.csv'

# read data
with open(dataName, 'rb') as load_data:
    data = pickle.load(load_data)  # 加载数据

# process data for classifier
for fileName, feature_label in data.items():
    feature_label[0]=feature_label[0].toarray()# sparse matrix to normal matrix
    feature_label[1]=feature_label[1].astype('int')# data type of labels

# train
classifiers=[GaussianNB(),MultinomialNB(),BernoulliNB()]
for clf in classifiers:
    clf = clf.fit(data[trainName][0], data[trainName][1])


# test


# evaluate
clf_scores=[]
for clf in classifiers:
    scores={}
    for fileName, feature_label in data.items():
        scores[fileName]=accuracy_score(feature_label[1], clf.predict(feature_label[0]))

    clf_scores.append(scores)