import jsonpickle
from Utilities import TypeValidator

class WordRepository():

    def __init__(self):

        # dictionary of categories and arrays of dictionaries of string and int
        self.data = dict()

        # all urls
        self.urls = set()

        # dictionary of categories and articles count
        self.imagesCounts = dict()

        # dictionary of categories and images count
        self.articlesCounts = dict()

    # add new category. Returns True if adding succeded.
    def addCategory(self, category, verbose=False):
        if not TypeValidator.isString(category):
            raise ValueError('wordRepository::addCategory: expected a string, got', type(category), '.')
        if category in self.data:
            return False
        else:
            self.data[category] = dict()
            self.articlesCounts[category] = 0
            self.imagesCounts[category] = 0
            if verbose:
                print('wordRepository::addCategory: added category "',category,'".')
            return True

    # return all categories
    def getCategories(self):
        return self.data.keys()

    # sets count of given word from given category. Auto adds new category if it doesn't exist
    def setWordCount(self, category, word, count, verbose=False):
        if not TypeValidator.isString(category):
            raise ValueError('wordRepository::addWord: expected a string for [category], got', type(category), '.')
        if not TypeValidator.isString(word):
            raise ValueError('wordRepository::addWord: expected a string for [word], got', type(word),' .')

        if category not in self.data:
            self.addCategory(category, verbose=verbose)

        self.data[category][word] = count

    # returns count of given word from given category
    def getWordCount(self, category, word, verbose=False):
        if not TypeValidator.isString(category):
            raise ValueError('wordRepository::getWordCount: expected a string for [category], got', type(category), '.')
        if not TypeValidator.isString(word):
            raise ValueError('wordRepository::getWordCount: expected a string for [word], got', type(word),' .')

        if category not in self.data:
            raise KeyError('wordRepository::getWordCount: key ', type(category),' not found.')

        if word not in self.data[category]:
            if verbose:
                print('wordRepository::getWordCount: didn\'t found "',word,'" in "',category,'", assuming count = 0')
            self.data[category][word] = 0

        return self.data[category][word]

    # returns dictionary of words and occurences
    def getAllCategoryWords(self, category):
        if not TypeValidator.isString(category):
            raise ValueError('wordRepository::getCategoryWords: expected a string for [category], got', type(category), '.')

        if category not in self.data:
            raise KeyError('wordRepository::getCategoryWords: key ', type(category),' not found.')

        return self.data[category]

    # add words of category
    def appendInBulk(self, url, category, words, imagesCount, autoAddCategory=True, verbose=False):
        if url in self.urls:
            if verbose:
                print('Url "', url,'" has been already added, skipping')
            return
        else:
            self.urls.add(url)

        if not TypeValidator.isString(category):
            raise ValueError('wordRepository::appendWordsInBulk: expected a string for [category], got', type(category), '.')

        if category not in self.data:
            if autoAddCategory:
                self.addCategory(category, verbose=verbose)
            else:
                raise KeyError('wordRepository::appendWordsInBulk: key ', type(category),' not found.')

        self.articlesCounts[category] += 1
        self.imagesCounts[category] += imagesCount
        for word, count in words.items():
            newCount = self.getWordCount(category, word, verbose=verbose) + count
            self.setWordCount(category, word, newCount)

    # get urls
    def getAllUrls(self):
        return self.urls

    # serialize to file
    def serialize(self, fileName):
        json = jsonpickle.encode(self)
        with open(fileName, 'w') as f:
            f.write(json)

    # deserialize from path
    def deserialize(fileName):
        with open(fileName, 'r') as f:
            json = f.read()
        return jsonpickle.decode(json)

    # return dictionaries<word, count>,  categories and dictionaries<category, word count>
    def getPagesClassesAndImagesCount(self):
        pages = []

        for c in self.data.keys():
            pages.append(self.data[c])

        return pages, self.articlesCounts, self.imagesCounts