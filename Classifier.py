import operator

class WebClassifier:
    #constructor
    def __init__(self):
        self.__words = {}
        self.__classes = {}
        self.__images = {}

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

    def __isTabOfInts(self, inTab):
        if not isinstance(inTab, list):
            return False
        for it in inTab:
            if not isinstance(it, int):
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

    def __isDictOfInt(self, checkedData):
        if not isinstance(checkedData, dict):
            print('nie bo nie jest dictem')
            return False
        for key in checkedData:
            if not isinstance(checkedData[key], int):
                print('nie bo ',checkedData[key],'nie jest intem')
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
                if word in self.__words:
                    value = self.__getValue(inputDict, word, index) / self.__classes[key]
                    sumOfValues += value
            listOfPred[key] = sumOfValues

        #self.__divideByMax(listOfPred)
        return listOfPred

    def __fillData(self, inWordsTab, inClassesTab, inImagesTab):
        newDictOfWords = {}
        newDictOfClasses = {}
        newDictOfImages = {}

        for label in inClassesTab:
            newDictOfClasses[label] = inClassesTab[label]
        for label in inImagesTab:
            newDictOfImages[label] = inImagesTab[label]

        for dic in inWordsTab:
            for word in dic:
                newDictOfWords[word] = [(int)(0) for i in range(len(newDictOfClasses))]

        for i in range(len(newDictOfClasses)):
            for key in inWordsTab[i]:
                    newDictOfWords[key][i] += inWordsTab[i][key]

        return newDictOfWords, newDictOfClasses, newDictOfImages

    #public methods
    def loadData(self, dictOfWords : list, tabOfClasses : dict, tabOfImageInfo : list):
        if not isinstance(tabOfClasses, dict):
            raise Exception('Bad types of input data (1). dictOfWords must be a dict')
        if not self.__isTabOfDictsOfInts(list(dictOfWords), len(tabOfClasses)):
            raise Exception('Bad types of input data (2). dictOfWords must be a tab of dicts of ints and have this same len like tabOfClasses')
        if not self.__isDictOfInt(tabOfClasses):
            raise Exception('Bad types of input data (3). tabOfClasses must be a dict of ints')
        if not self.__isDictOfInt(tabOfImageInfo):
            raise Exception('Bad types of input data (4). tabOfImageInfo must be a dict of ints')

        self.__words, self.__classes, self.__images = self.__fillData(dictOfWords, tabOfClasses, tabOfImageInfo)



    def predict(self, inputWords, addToData=False):
        predOfWords = self.__predict(inputWords)
        self.printFormattedScores(predOfWords)

        if(addToData==True):
            classResult = max(predOfWords.items(), key=operator.itemgetter(1))[0]
            self.addData(inputWords, classResult)

    def addData(self, inputWords, inputClass):
        self.__classes[inputClass] += 1
        for key in inputWords:
            if(key in self.__words):
                self.__words[key][list(self.__classes.keys()).index(inputClass)] += inputWords[key]

            else:
                newWord = [(int)(0) for i in range(len(self.__classes))]
                newWord[list(self.__classes.keys()).index(inputClass)] = inputWords[key]
                self.__words[key] = newWord

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

    def saveToDataToFile(self, filepath):
        file = open(filepath, 'w')

        file.write('classes:\n')
        for key, value in self.__classes.items():
            file.write(key+':'+str(value)+'\n')
        file.write('\n')

        file.write('images:\n')
        for key, value in self.__images.items():
            file.write(key+':'+value+'\n')
        file.write('\n')

        file.write('worlds:\n')
        for key, value in self.__words.items():
            try:
                file.write(str(key))
            except:
                file.write('ERROR')
            for elem in value:
                file.write(' '+str(elem))
            file.write('\n')

        file.close()