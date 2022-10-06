# download data from vivino

# Not solved:
# maybe we shouldn't limit country. Or data is not enough and it take too much time to extract
# (274 samples,184 second).
# The labels are unbalanced: 274 samples, 39 negative

import requests
import pandas as pd
import utility

# boundary of rating to identify positive/negative label
labelPositive = 4.3
labelNegative = 3.3

#settings & file names
startPage=5
numWine=100
maxPage=numWine/25+startPage# 25 wine per page, 4 pages
saveName="data_cheap1" #expensive: "data"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
}


def get_wine_data(wine_id, year, page):
    api_url = "https://www.vivino.com/api/wines/{id}/reviews?per_page=50&year={year}&page={page}"  # <-- increased the number of reviews to 9999
    data = requests.get(
        api_url.format(id=wine_id, year=year, page=page), headers=headers
    ).json()  # id=152262411, year=2013

    filteredReview = []  # without rating between 2.9-4.0
    hasReview = False

    for review in data['reviews']:
        hasReview = True
        # # fetch user country
        # seo_name=review['user']['seo_name']
        # country=get_user_country(seo_name)
        # review['user']['country']=country
        # give label
        review['label'] = -1  # no not process yet
        if review['rating'] > labelPositive:
            review['label'] = 1
        if review['rating'] < labelNegative:
            review['label'] = 0
        if review['label'] != -1:
            filteredReview.append(review)

    data['reviews'] = filteredReview
    data['hasReview'] = hasReview

    return data


# fetch user country: 'united-states','sweden', ...
def get_user_country(seo_name):
    api_url = "https://www.vivino.com/api/users/{seo_name}"
    data = requests.get(
        api_url.format(seo_name=seo_name), headers=headers
    ).json()["user"]["address"]["country"]["seo_name"]

    return data


# fetch all wines under requirement
# later: make price boundary as variable, number of pages
def searchWines():
    pageIndex = startPage
    wineList = []

    # wine results of the first 25*4 wines
    while pageIndex < maxPage:
        r = requests.get(
            "https://www.vivino.com/api/explore/explore",
            params={
                "country_code": "SE",
                "language": "en",
                # "country_codes[]": ["pt", "es", "fr"],
                "currency_code": "SEK",
                # "grape_filter": "varietal",
                # "min_rating": "1",
                "order_by": "ratings_count",
                "order": "desc",
                "page": pageIndex,
                "price_range_max": "150",
                #"price_range_min": "250",
                "wine_type_ids[]": ["1", "2", "3", "4", "7", "24"],  # ,all wine types
            },
            headers=headers,
        )
        wineList += r.json()["explore_vintage"]["matches"]
        print("explored wines in page " + str(pageIndex))
        pageIndex += 1

    results = [
        (
            t["vintage"]["wine"]["winery"]["name"],
            t["vintage"]["year"],
            t["vintage"]["wine"]["id"],
            f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
            t["price"]["amount"],
            t["vintage"]["statistics"]["ratings_count"],
        )
        for t in wineList
    ]
    dataframe = pd.DataFrame(
        results,
        columns=["Winery", "Year", "Wine ID", "Wine", "price", "num_ratings"],
    )
    return dataframe

dataframe = searchWines()
ratings = []
finishedIndex=-1

for _, row in dataframe.iterrows():
    page = 1
    while True:  # while true
        print(
            f'Getting info about wine {row["Wine ID"]}-{row["Year"]} Page {page}'
        )
        # fetch data of each wine that has more than 2000 rates
        # otherwise there are not enough negative reviews
        d = get_wine_data(row["Wine ID"], row["Year"], page)

        if not d["hasReview"]:
            break
        if page>300:
            break
        for r in d["reviews"]:
            ratings.append(
                [
                    row["Wine"],
                    row["price"],
                    # r['user']['country'],
                    r['language'],
                    r["note"],
                    r["label"],
                ]
            )
        if page % 50 == 0: #save every 50 pages
            utility.saveData("I:/HCI_KTH/big data/project/codes/wine_study/wine/"+saveName+".pkl",ratings)
            print("till page saved: " + str(page)+" number of ratings: "+str(ratings.__len__()))

        page += 1

    utility.saveData("I:/HCI_KTH/big data/project/codes/wine_study/wine/"+saveName+".pkl", ratings)
    finishedIndex+=1

    print("finished ID "+str(finishedIndex))


ratings = pd.DataFrame(
        ratings, columns=["Wine", "price", "country", "Note", "label"]
        # ["Wine", "price", "country", "language","Note", "label"]
    )

    # df_out = ratings.merge(dataframe)
ratings.to_csv("I:/HCI_KTH/big data/project/codes/wine_study/wine/"+saveName+".csv", index=False)
