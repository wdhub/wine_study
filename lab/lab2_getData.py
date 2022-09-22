# get comments from Booking.com
# comments under: Queen's Hotel, crystalplaza

import urllib.request as urllib2
import re
import pandas as pd


def getData(baseURL,totalReview):
    pageIndex = 1  # which page
    numReview = 0  # number of reviews
    reviewList = []
    labelList = []

    while(numReview<totalReview):
        url=baseURL+"&page="+str(pageIndex)+"&r_lang=en&rows=75&"
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        html = html.decode('iso8859-1')
        # find reviews
        html=html.replace('\n','')#delete \n. There are \n in some reviews, and regulator couldn't find the <\span>
        reg = '<span itemprop="reviewBody">(.+?)</span>'#|Positive point|Negative point
        review = re.compile(reg).findall(html)

        # find labels
        reg = '"review_neg "><svg aria-label="(.+?)\"|"review_pos "><svg aria-label="(.+?)\"'#|Positive point|Negative point
        lab = re.compile(reg).findall(html)
        #change into standard labels: negative 0, positive 1
        lab_new =[0 if i ==('Negative point', '') else i for i in lab]
        lab =[1 if i ==('', 'Positive point') else i for i in lab_new]

        numReview+=lab.__len__()
        if(lab.__len__()<1):# no more reviews
            break
        print("number of reviews: "+str(numReview)+" page: "+str(pageIndex))
        labelList+=lab
        reviewList+=review
        pageIndex+=1

    return labelList, reviewList



totalReview=170
baseURL='https://www.booking.com/reviews/se/hotel/queens.en-gb.html?label=gen173nr-1FEgdyZXZpZXdzKIICOOgHSDNYBGjIAYgBAZgBLbgBF8gBD9gBAegBAfgBC4gCAagCA7gCiaqwmQbAAgHSAiQxODliZWNkNC1kOWM3LTQ4NmUtOGMxYi1jOWIwMzY4ZGYyZmbYAgbgAgE&sid=b5d2fdb194d2f95a580b7326313d21ef&customer_type=total&hp_nav=0&old_page=0&order=featuredreviews'
labelList1, reviewList1=getData(baseURL,totalReview)

# reviews from one hotel is not enough
baseURL='https://www.booking.com/reviews/se/hotel/crystalplaza.en-gb.html?label=gen173nr-1FEgdyZXZpZXdzKIICOOgHSDNYBGjIAYgBAZgBLbgBF8gBD9gBAegBAfgBC4gCAagCA7gCiaqwmQbAAgHSAiQxODliZWNkNC1kOWM3LTQ4NmUtOGMxYi1jOWIwMzY4ZGYyZmbYAgbgAgE&sid=b5d2fdb194d2f95a580b7326313d21ef&customer_type=total&hp_nav=0&old_page=0&order=featuredreviews'
totalReview=30
labelList2, reviewList2=getData(baseURL,totalReview)

labelList=labelList1+labelList2
reviewList=reviewList1+reviewList2

#save into csv
dataframe = pd.DataFrame({'score':labelList,'text':reviewList})
dataframe.to_csv("booking.csv",index=False)