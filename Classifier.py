import operator

class WebClassifier:
    #constructor
    def __init__(self):
        self.__words = {}
        self.__classes = {}

    #private methods
    def __isTabOfDictsOfInts(self, checkedData, lenOfFirstTab): # sprawdzanie czy dane to tablica slownikow tablic intow
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

    def __sumDicts(self, inputTab): #przemienia tablice slownikow w slownik tablic
        newDict = {}
        for dic in inputTab:
            for key in dic:
                newDict[key] = []
        for key in newDict:
            for dic in inputTab:
                if key in dic:
                    newDict[key].append(dic[key])
                else:
                    newDict[key].append(0)
        return newDict

    def __isTabOfStr(self, checkedData):
        for line in checkedData:
            if not isinstance(line,str):
                return False
        return True

    def __getValue(self, inputDict, word, i):
        return inputDict[word] * (self.__words[word][i] / sum(self.__words[word]))

    def __sumOfIntsInDict(self,inputDict):
        sum = 0
        for word in inputDict:
            sum += inputDict[word]
        return sum

    def __sumOfIntsInDictsOfTabs(self, inputDict, iterator):
        sum = 0
        for word in inputDict:
            sum += inputDict[word][iterator]
        return sum

    #przewiduje po maksimum zdobytego scoru, nie dokończone
    def __divideByMax(self,inputDict):
        maxOfDict = max(inputDict.items(), key=operator.itemgetter(1))[0]
        print(inputDict)

        for key in inputDict:
            inputDict[key] = inputDict[key] / inputDict[maxOfDict]

    def __predict(self, inputDict):
        listOfPred = {}

        for key in self.__classes:
            index = list(self.__classes.keys()).index(key)
            sumOfValues = 0
            for word in inputDict:
                #print('Word: ', word) #------------------------------
                if word in self.__words:
                    value = self.__getValue(inputDict, word, index) / self.__classes[key]
                    sumOfValues += value
                    #print(inputDict[word], '*', self.__words[word][i], '/', sum(self.__words[word]), '=', value)  # ----------------
            listOfPred[key] = sumOfValues

        #self.__divideByMax(listOfPred)
        return listOfPred



    #public methods
    def loadData(self, dictOfWords : list, tabOfClasses : list):

        if not isinstance(tabOfClasses, list) \
                or not self.__isTabOfDictsOfInts(list(dictOfWords), len(tabOfClasses))\
                or not self.__isTabOfStr(tabOfClasses):
            raise Exception('Bad types of input data')

        self.__words, self.__classes = self.fillData(dictOfWords, tabOfClasses)

    def fillData(self, inWordsTab, inClassesTab):
        newDictOfWords = {}
        newDictOfClasses = {}

        for label in inClassesTab:
            newDictOfClasses[label] = (int)(0)
        for label in inClassesTab:
            newDictOfClasses[label] += 1

        for dic in inWordsTab:
            for word in dic:
                newDictOfWords[word] = [(int)(0) for i in range(len(newDictOfClasses))]

        for i in range(len(inWordsTab)):
            for word in inWordsTab[i]:
                index = list(newDictOfClasses.keys()).index(inClassesTab[i])
                newDictOfWords[word][index] += inWordsTab[i][word]

        return newDictOfWords, newDictOfClasses

    def predict(self, inputWords):
        predOfWords = self.__predict(inputWords)
        self.printFormattedScores(predOfWords)

    def clear(self):
        self.__init__()

    def printWords(self):
        for word in self.__words:
            print(word, ': ', self.__words[word])
        print('class : sum of pages')
        for key, value in self.__classes.items():
            print(key,' : ', value)

    def printFormattedScores(self, predOfWords):
        s = sum(predOfWords.values())
        sortedSc = sorted(predOfWords.items(), key=operator.itemgetter(1), reverse=True)
        for x in sortedSc:
            print(x[0], ' :  ', round(x[1] / s * 100, 2), '%')
