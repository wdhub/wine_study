import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle

#read file
viv = pd.read_csv('/Users/shreeyasathe/PycharmProjects/correlation/data.csv', sep=';')
print (viv.head())
#print(len(data_dict))

viv_list = list(viv.columns)
viv_dict = dict()

for i, item in enumerate(viv_list):
    viv_dict[item] = i + 1

print(viv_dict)

def readCSV(fileName):
    rawData = pd.read_csv(fileName)
    notes = rawData.values[:, 3]  # process later
    prices = rawData.values[:, 1]
    print (notes, prices)
    return notes, prices


# clean text
def cleanText(notes):
    clearedCom = []
    for comment in notes:
        # twits-specific cleaning: mention, tags & html
        noMention = re.sub(r'@[A-Za-z0-9]+', "", str(comment))  # mention
        noTag = re.sub(r"#[A-Za-z0-9]+", "", noMention)  # tags
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
#print("before: " +notes[5])
#print("after: " +clearedCom[5])

def saveData(saveName, data):
    with open(saveName, "wb") as file:
        pickle.dump(data, file, True)

# extract dictionary model
def getDict(clearedCom):
    # if training set
    tfidModel = TfidfVectorizer(max_features=3000, min_df=1, max_df=1, stop_words=stopwords.words())
    tfidModel = tfidModel.fit(clearedCom)
    print ("model created, features extracted")
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
trainName = "data.csv"
#saveName = "viv.pkl"
filePath = os.getcwd()  # "I:/HCI_KTH/big data/project/codes/wine_study/lab"
print("current location: " + filePath)

# read and clean data
for fileName in os.listdir(filePath):
    if 'csv' in fileName:  # only read datasets
        # dictionary. type of dataset, cleaned data
        notes, prices = readCSV(filePath + "/" + fileName)
        cleanAllData[fileName] = cleanText(notes)
        allLabels[fileName] = prices
        print(fileName + " cleaning finished")

features_label = {}
model = getDict(cleanAllData[trainName]) # generate dictionary from training set

# collect frequency according to dictionary->features
for fileName, data in cleanAllData.items():
    features_label[fileName] = [model.transform(data), allLabels[fileName]]
    print(fileName + " extracting finished")
    print (features_label)