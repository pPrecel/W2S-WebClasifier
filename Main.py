from Classifier import WebClassifier
import WebScrapper
import wordRepository as repo
from jeszczenowszescrapy import startJeszczeNowszy

#pages, classes = nowescrapy.loadFromExcel()

#clf = WebClassifier()
#clf.loadData(pages, classes)
#clf.printWords()

#clf.predict(WebScrapper.scrapPage('https://en.wikipedia.org/wiki/Computer_programming'))


#---------------------------------------------------
pages, classes = startJeszczeNowszy()

clf = WebClassifier()
clf.loadData(pages, classes)
clf.printWords()

clf.predict(WebScrapper.scrapPage('http://dawidpolap.pl/'))

exit()

r = repo.wordRepository.deserialize('repo.json')

classes = r.getCategories()
pages = []
for c in classes:
    pages.append(r.getAllCategoryWords(c))