import pandas


def read():
    df = pandas.read_excel(r'Categories.xlsx')
    #print(df.columns)

    links = df['link'].values
    categories = df['category'].values

    dicti = dict()

    for i in range(len(df.values)):
        if categories[i] not in dicti.keys():
            dicti[categories[i]] = list()
        dicti[categories[i]].append(links[i])

    for k in dicti.keys():
        print(k, len(dicti[k]))

    return dicti




#UŻYCIE Z MAINA

#IMPORT ReadExcel

# dicti = ReadExcel.read()
#
# pages =  []
# classes = []
#
# for key in dicti.keys():
#     print(key)
#     for link in dicti[key]:
#         print(link)
#         pages.append(WebScrapper.scrapPage(link))
#         classes.append(key)
#
# clf = WebClassifier()
# clf.loadData(pages, classes)
#
# clf.printWords()
#
# clf.predict(WebScrapper.scrapPage('https://en.wikipedia.org/wiki/Computer_programming'))