# some functions that are repeatedly used
# functions: readCSV, cleanText, saveData


import re
import pandas as pd
import pickle

# read 2 columns from original data
def readCSV(fileName, column1, column2):
    rawData = pd.read_csv(fileName)
    comments = rawData.values[:, column1]  # process later
    labels = rawData.values[:, column2]
    return comments, labels


# clean text
# I/O: list of comments
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

# save data as pickle file
def saveData(saveName, data):
    with open(saveName, "wb") as file:
        pickle.dump(data, file, True)