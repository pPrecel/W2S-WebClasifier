from collections import Counter

class TypeValidator:

    # check if given object is a string
    def isString(possiblyString):
        return isinstance(possiblyString, str)

    # check if given object is a dictionary
    def isDict(possiblyDictionary):
        return isinstance(possiblyDictionary, dict)

    # check if given object is a int
    def isInteger(possiblyInteger):
        return isinstance(possiblyInteger, int)

    # check if given object is a list
    def isList(possiblyList):
        return isinstance(possiblyList, list)

    def isTabOfDictsOfInts(checkedData, lenOfFirstTab): # sprawdzanie czy dane to tablica slownikow tablic intow
        #Bo najwazniejsza jest prosta i klarowna reprezentacja danych :)
        try:
            if not TypeValidator.isList(checkedData):
                print('cheked', type(checkedData))
                raise ValueError('TypeValidator::isTabOfDictsOfInts: checked data should be list, not ',type(checkedData),'!')
            if len(checkedData) != lenOfFirstTab:
                raise ValueError('TypeValidator::isTabOfDictsOfInts: checked data length should be',lenOfFirstTab,', not ', len(checkedData),'!')
            for elem in checkedData:
                if not TypeValidator.isDict(elem):
                    raise ValueError('TypeValidator::isTabOfDictsOfInts: expected type of elem is dict, got: ', type(elem))
                for key in elem:
                    if not TypeValidator.isInteger(elem[key]):
                        raise ValueError('TypeValidator::isTabOfDictsOfInts: expected type of elem[key] is list, got: ', type(elem[key]))
                    if not TypeValidator.isString(key):
                        raise ValueError('TypeValidator::isTabOfDictsOfInts: expected type of key is string, got: ', type(key))
        except ValueError:
            return False

        return True

    def isTabOfInts(inTab):
        if not TypeValidator.isList(inTab):
            return False
        for it in inTab:
            if not TypeValidator.isInteger(it):
                return False
        return True

    def isDictOfInt(checkedData):
        if not TypeValidator.isDict(checkedData):
            return False

        return all([TypeValidator.isInteger(v) for v in checkedData.values()])


class Utility:

    # check if character is ascii
    def isAscii(s):
        return all(ord(c) < 128 for c in s)

    # count word occurences in list
    def countPairs(strings):
        return dict(Counter(strings))

    # return content of digits in a string
    def getNumericContent(string):
        numbersCount = sum(c.isdigit() for c in string)
        return numbersCount / len(string)
