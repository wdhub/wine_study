# clean the data from raw comments
# filter out stop words, mention and tags
# separate emoji and text---->maybe emoji later
# create dictionary from training set and test set
# extract feature vectors for all the datasets and save them
import re
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# read original data
fileName="train.csv" #"I:/HCI_KTH/big data/project/codes/wine_study/lab/train.csv"
rawData=pd.read_csv(fileName,header=1)
comments=rawData.values[:,1] #process later
labels=rawData.values[:,0]

# clean mention & tags
# mention begin with @ and end with space
clearedCom=[]
for comment in comments:
    noMention=re.sub("@[A-Za-z0-9]+","", comment)
    noTag_mention=re.sub("#[A-Za-z0-9]+","", noMention)
    # Remove all the special characters
    processed_feature = re.sub(r'\W', ' ', str(features[sentence]))

    # remove all single characters
    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

    # Remove single characters from the start
    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature)

    # Substituting multiple spaces with single space
    processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

    # Removing prefixed 'b'
    processed_feature = re.sub(r'^b\s+', '', processed_feature)

    # Converting to Lowercase
    processed_feature = processed_feature.lower()

    clearedCom.append(noTag_mention)

# see if the result is right
print("before: "+comments[5])
print("after: "+clearedCom[5])




# clean stop words


# vectorize