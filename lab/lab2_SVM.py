# train & evaluate SVM classifier
# use preprocessed data

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle

#prepare path
dataName="data.pkl"
trainName='train.csv'

# read data
with open(dataName, 'rb') as load_data:
    data = pickle.load(load_data)  # 加载数据

# process data for classifier
for fileName, feature_label in data.items():
    feature_label[0]=feature_label[0].toarray()# sparse matrix to normal matrix
    feature_label[1]=feature_label[1].astype('int')# data type of labels

# train

classifier = SVC(kernel='linear',random_state=1,C=1,gamma='auto')
classifier.fit(data[trainName][0], data[trainName][1])

# test


# evaluate

scores={}
for fileName, feature_label in data.items():
    scores[fileName]=accuracy_score(feature_label[1], classifier.predict(feature_label[0]))

print(scores)