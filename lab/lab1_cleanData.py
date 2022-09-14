# clean the data from raw comments
# filter out stop words, mention and tags
# separate emoji and text---->maybe emoji later
# create dictionary from training set and test set
# extract feature vectors for all the datasets and save them
# ------------no! The dictionary need to be the same!-------------------
import re
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle


# read original data
def readCSV(fileName):
    rawData = pd.read_csv(fileName)
    comments = rawData.values[:, 1]  # process later
    labels = rawData.values[:, 0]
    return comments, labels


# clean text
def cleanText(comments):
    clearedCom = []
    for comment in comments:
        # twits-specific cleaning: mention, tags & html
        noMention = re.sub("@[A-Za-z0-9]+", "", comment)  # mention
        noTag = re.sub("#[A-Za-z0-9]+", "", noMention)  # tags
        # HTML
        temp = re.sub(r'^(https:\S+)', ' ', noTag)
        noHTML = re.sub(r'[a-zA-Z]+://[^\s]*', '', temp)

        # clean single characters, spaces, transform to lowercase
        noSpecial = re.sub(r'\W', ' ', noHTML)  # Remove all the special characters
        # single characters
        noSingle = re.sub(r'\s+[a-zA-Z]\s+', ' ', noSpecial)
        noSingle = re.sub(r'\^[a-zA-Z]\s+', ' ', noSingle)
        # space
        oneSpace = re.sub(r'\s+', ' ', noSingle, flags=re.I)  # Substitute multiple spaces with single space
        noEndSpace = oneSpace.strip()  # first and last space
        cleared = noEndSpace.lower()  # Convert to Lowercase

        clearedCom.append(cleared)

    return clearedCom


# # see if the result is right
# print("before: "+comments[5])
# print("after: "+clearedCom[5])

# save data
def saveData(saveName, data):
    with open(saveName, "wb") as file:
        pickle.dump(data, file, True)


# extract dictionary model
def getDict(clearedCom):
    # if training set
    tfidModel = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
    tfidModel = tfidModel.fit(clearedCom)

    # dictionary=tfidModel.vocabulary_
    # sortedDict=sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    # sortedDict=sortedDict[0:2500-75]
    return tfidModel

#----------------------------------main---------------------------------------

# # prepare stop words
# nltk.download('stopwords')

# prepare location
cleanAllData = {}
allLabels = {}
trainName = "train.csv"
saveName = "data.pkl"
filePath = os.getcwd()  # "I:/HCI_KTH/big data/project/codes/wine_study/lab"
print("current location: " + filePath)

# read and clean data
for fileName in os.listdir(filePath):
    if 'csv' in fileName:  # only read datasets
        # dictionary. type of dataset, cleaned data
        comments, labels = readCSV(filePath + "/" + fileName)
        cleanAllData[fileName] = cleanText(comments)
        allLabels[fileName] = labels
        print(fileName + " cleaning finished")


# generate features

# structure: {'train.csv':[feature sparse matrix, label vector],...}
features_label = {}
model = getDict(cleanAllData[trainName])# generate dictionary from training set

# collect frequency according to dictionary->features
for fileName, data in cleanAllData.items():
    features_label[fileName] = [model.transform(data), allLabels[fileName]]
    print(fileName + " extracting finished")

# save result
saveData(filePath + "/" + saveName, features_label)
