#classifier utils
from Classifier import WebClassifier
import WebScrapper
import DataLoader

#server utils
from flask import Flask
from flask import request
import json

# init data loader
loader = DataLoader.DataLoader(verbose=True)

# try to load previous repository
loader.loadRepoFromJSON('repo.json')

# load links and categories from Excel
loader.loadClassesAndCategoriesFromExcel(r'Categories.xlsx')

# if site was not present in loader's WordRepository object, pull it here
loader.scrapMissingSites()

# get data for classifier
pages, classes, images = loader.getPagesClassesAndImagesCount()

# save repo for the next time
loader.saveToJSON('repo.json')

clf = WebClassifier()
clf.loadData(pages, classes, list(images.values()))

#init flask app
app = Flask(__name__)

@app.route('/')
def hello_world():
    site = request.args.get('siteUrl')
    print('predicting category for ', site, '...')
    data = WebScrapper.Scrapper().scrapPage(site)
    predicted = clf.predict(data[0], data[1])
    clf.printFormattedScores(predicted)
    return json.dumps(clf.getFormattedScores(predicted, False), indent = 4)

if __name__ == '__main__':
    app.run()

    