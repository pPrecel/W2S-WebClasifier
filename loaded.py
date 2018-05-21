import wordRepository as repo

r = repo.wordRepository.deserialize('repo.json')

for key, value in r.dictionaryOfCategoriesAndArraysOfDictionariesOfStringAndInt.items():
    print(key, len(value))

r.appendInBulk('http://scp-wiki.wikidot.com/scp-355', 'dupa', {'uch' : 0}, verbose=True)
