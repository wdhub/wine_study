import utility
import numpy as np
from nltk.corpus import stopwords
from apyori import apriori

#read file
fileName="I:/HCI_KTH/big data/project/codes/wine_study/wine/data_en.csv"
comments, prices=utility.readCSV(fileName, 3,1)

# transform as list of list
price_com_set=[]
en_stops = set(stopwords.words('english'))
for (price,com) in zip(prices,comments):
    # price grouping
    priceLabel='unknown_price'
    if(price<=150):
        priceLabel="low_price"
    if (price>=250) & (price<=350):
        priceLabel="middle_price"
    if price>350:
        priceLabel = "high_price"

    # clean comments
    cleanedCom=utility.cleanText([com]) # clean special symbols etc
    splitedCom=str(cleanedCom[0]).split() # split into list of words
    noStopCom=list(set(splitedCom).difference(set(en_stops))) # delete stop words

    #combine
    noStopCom.append(priceLabel)
    price_com_set.append(noStopCom)



# call apriori
association_rules = apriori(price_com_set, min_support=0.003, min_confidence=0.1, min_lift=3, min_length=2)
association_results = list(association_rules)

# sort results related to price
pairs=[]
highWords=[]
midWords=[]
lowWords=[]

for item in association_results:
    #decode result
    newPair = [x for x in item.items]

    # select price related
    inter= {'low_price', 'high_price', 'middle_price'}.intersection(set(newPair))
    if (inter.__len__()!=0) & (newPair not in pairs): # price related, not added before
        pairs.append(newPair)
        if 'low_price' in newPair:
            lowWords+=list(set(newPair)-{'low_price'})
        if 'middle_price' in newPair:
            midWords+=list(set(newPair)-{'middle_price'})
        if 'high_price' in newPair:
            highWords+=list(set(newPair)-{'high_price'})

highWords=list(np.unique(highWords)) # delete repeat
midWords=list(np.unique(midWords)) # delete repeat
lowWords=list(np.unique(lowWords)) # delete repeat

#save results
utility.saveData("I:/HCI_KTH/big data/project/codes/wine_study/wine/price_words.pkl", {'low_price':lowWords,'mid_price':midWords,'high_price':highWords})

import matplotlib.pyplot as plt
from matplotlib_venn import venn3
g = venn3(subsets=[lowWords,midWords,highWords],set_labels = ('low', 'median','high'),)
plt.show()