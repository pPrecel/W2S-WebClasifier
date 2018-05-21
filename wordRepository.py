import jsonpickle

class wordRepository():

    def __init__(self):
        self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt = dict()
        self.urls = set()

    # add new category. Returns True if adding succeded.
    def addCategory(self, category, verbose=False):
        if not isinstance(category, str):
            raise ValueError('wordRepository::addCategory: expected a string, got', type(category), '.')
        if category in self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt:
            return False
        else:
            self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt[category] = dict()
            if verbose:
                print('wordRepository::addCategory: added category "',category,'".')
            return True

    # return all categories
    def getCategories(self):
        return self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt.keys()

    # sets count of given word from given category. Auto adds new category if it doesn't exist
    def setWordCount(self, category, word, count, verbose=False):
        if not isinstance(category, str):
            raise ValueError('wordRepository::addWord: expected a string for [category], got', type(category), '.')
        if not isinstance(word, str):
            raise ValueError('wordRepository::addWord: expected a string for [word], got', type(word),' .')

        if category not in self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt:
            addCategory(category, verbose=verbose)

        self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt[category][word] = count

    # returns count of given word from given category
    def getWordCount(self, category, word, verbose=False):
        if not isinstance(category, str):
            raise ValueError('wordRepository::getWordCount: expected a string for [category], got', type(category), '.')
        if not isinstance(word, str):
            raise ValueError('wordRepository::getWordCount: expected a string for [word], got', type(word),' .')

        if category not in self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt:
            raise KeyError('wordRepository::getWordCount: key ', type(category),' not found.')

        if word not in self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt[category]:
            if verbose:
                print('wordRepository::getWordCount: didn\'t found "',word,'" in "',category,'", assuming count = 0')
            self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt[category][word] = 0

        return self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt[category][word]

    # returns dictionary of words and occurences
    def getAllCategoryWords(self, category):
        if not isinstance(category, str):
            raise ValueError('wordRepository::getCategoryWords: expected a string for [category], got', type(category), '.')

        if category not in self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt:
            raise KeyError('wordRepository::getCategoryWords: key ', type(category),' not found.')

        return self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt[category]

    # add words of category
    def appendInBulk(self, url, category, words, autoAddCategory=True, verbose=False):
        if url in self.urls:
            if verbose:
                print('Url "', url,'" has been already added, skipping')
            return
        else:
            self.urls.add(url)

        if not isinstance(category, str):
            raise ValueError('wordRepository::appendWordsInBulk: expected a string for [category], got', type(category), '.')

        if category not in self.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt:
            if autoAddCategory:
                self.addCategory(category, verbose=verbose)
            else:
                raise KeyError('wordRepository::appendWordsInBulk: key ', type(category),' not found.')

        for word, count in words.items():
            newCount = self.getWordCount(category, word, verbose=verbose) + count
            self.setWordCount(category, word, newCount)

    # serialize to file
    def serialize(self, fileName):
        json = jsonpickle.encode(self)
        with open(fileName, 'w') as f:
            f.write(json)

    def deserialize(fileName):
        with open(fileName, 'r') as f:
            json = f.read()
        return jsonpickle.decode(json)