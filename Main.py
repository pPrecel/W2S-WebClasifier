from Classifier import WebClassifier
import WebScrapper
import DataLoader

# init data loader
loader = DataLoader.DataLoader(verbose=True)

# try to load previous repository
loader.loadRepoFromJSON('repo.json')

# load links and categories from Excel
loader.loadClassesAndCategoriesFromExcel(r'Categories.xlsx')

# if site was not present in loader's WordRepository object, pull it here
loader.scrapMissingSites()

# get data for classifier
pages, classes = loader.getPagesAndClasses()

clf = WebClassifier()
clf.loadData(pages, classes)
#clf.printWords()

site = 'http://dawidpolap.pl/'
print('predicting category for ',site,'...')
clf.predict(WebScrapper.scrapPage(site))

# save repo for the next time
loader.saveToJSON('repo.json')
