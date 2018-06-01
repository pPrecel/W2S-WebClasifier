from collections import Counter

class TypeValidator:

    # check if given object is a string
    def isString(possiblyString):
        return isinstance(possiblyString, str)

    # check if given object is a dictionary
    def isDict(possiblyDictionary):
        return isinstance(possiblyDictionary, dict)

    def isTabOfDictsOfInts(checkedData, lenOfFirstTab): # sprawdzanie czy dane to tablica slownikow tablic intow
        #Bo najwazniejsza jest prosta i klarowna reprezentacja danych :)
        try:
            if not isinstance(checkedData,list) or not len(checkedData) == lenOfFirstTab:
                raise Exception
            for elem in checkedData:
                if not isinstance(elem, dict):
                    raise Exception
                for key in elem:
                    if not isinstance(elem[key], int) or not isinstance(key, str):
                        raise Exception
        except Exception:
            return False

        return True

    def isTabOfInts(inTab):
        if not isinstance(inTab, list):
            return False
        for it in inTab:
            if not isinstance(it, int):
                return False
        return True

    def isDictOfInt(checkedData):
        if not isinstance(checkedData, dict):
            print('nie bo nie jest dictem')
            return False
        for key in checkedData:
            if not isinstance(checkedData[key], int):
                print('nie bo ',checkedData[key],'nie jest intem')
                return False
        return True


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
