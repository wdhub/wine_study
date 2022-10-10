# extract features from reviews
# method: frequent words / correlation words

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import utility

# build dictionary on the most frequent words
def freExtract(com_train,com_test):
    # get dictionary
    model = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
    model = model.fit(com_train)
    utility.saveData("freq_dict.pkl",model)
    # extract features
    X_train = model.transform(com_train).toarray()
    X_test = model.transform(com_test).toarray()

    return X_train,X_test

# build dictionary on the most correlated words
def corExtract(corDict,com_train):
    features = np.zeros((com_train.__len__(), corDict.__len__()))
    for (review, row) in zip(com_train, np.arange(com_train.__len__())):
        for (word, col) in zip(corDict, np.arange(corDict.__len__())):
            features[row, col] = review.count(word)

    features = normalize(features)  # normalize

    return features