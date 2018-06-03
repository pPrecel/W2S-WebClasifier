from Utilities import TypeValidator
from Utilities import Utility
import operator

class WebClassifier:
    #constructor
    def __init__(self):
        self.__words = {} # słownik przechowuje wszystkie słowa w postaci [], gdzie każdy index tej tablicy odpowiada indeksowi w słowniku classes
        self.__classes = {}# słownik klas, który zawiera ilość stron w postaci {klasa : ilość stron}
        self.__images = {}# słownik obrazków, który zawiera klasę, oraz ilość wystąpień obrazka w postaci {klasa : ilość obrazków}

    #private methods
    def __getValueForWords(self, inputDict, word, i): # pobiera wartość dla słów na podstawie ilości słów na stronie i w bazie stron
        return inputDict[word] * (self.__words[word][i] / sum(self.__words[word]))

    def __getValueForImage(self, inputImage, key): # pobiera wartość dla obrazków na podstawie ilości obrazków na stronie i stronach w bazie
        return inputImage * (self.__images[key] / sum([value for key, value in self.__images.items()]))

    def __getWeight(self, index, key): # oblicza wagi dla obrazków i słów na podstawie ich wystąpień na stronach
        sumOfWords = sum([value[index] for key, value in self.__words.items()])
        wordsWeight = sumOfWords / (sumOfWords + self.__images[key])
        imagesWeight = self.__images[key] / (sumOfWords + self.__images[key])

        return wordsWeight, imagesWeight

    def __predict(self, inputDict, inputImage):
        listOfPred = {}

        for key in self.__classes:
            index = list(self.__classes.keys()).index(key) # wyliczanie indexu w słodniku słów
            # głównych na podstawie klasy, którą poddajemy badaniu

            wordsWeight, imagesWeight = self.__getWeight(index, key) # wyliczanie wag,
            # przeg które będą mnożone ostateczne wyniki

            sumOfValues = 0 # zmienna, która uzupełniana jest wynikami klasyfikacji dla poszczególnych słów i obrazków
            wordValue = 0
            imageValue = 0

            for word in inputDict: # obliczanie wyniku klasyfikacyjnego dla słów
                if word in self.__words:
                    value = self.__getValueForWords(inputDict, word, index)
                    wordValue += value

            imageValue = self.__getValueForImage(inputImage, key) # obliczanie wyniku klasyfikacyjnego dla obrazkow

            #Dodawanie wartości i mnożenie ich przez wagi:
            sumOfValues = (wordValue*wordsWeight) + (imageValue*imagesWeight)

            listOfPred[key] = sumOfValues

        return listOfPred

    def __fillData(self, inWordsTab, inClassesTab, inImagesTab): # przetwarza dane wejściowe na słowniki, którymi operuje program
        newDictOfWords = {}
        newDictOfClasses = {}
        newDictOfImages = {}

        for label in inClassesTab:
            newDictOfClasses[label] = inClassesTab[label]
            index = list(inClassesTab.keys()).index(label)
            newDictOfImages[label] = inImagesTab[index]

        for dic in inWordsTab:
            for word in dic:
                newDictOfWords[word] = [(int)(0) for i in range(len(newDictOfClasses))]

        for i in range(len(newDictOfClasses)):
            for key in inWordsTab[i]:
                    newDictOfWords[key][i] += inWordsTab[i][key]

        return newDictOfWords, newDictOfClasses, newDictOfImages

    #public methods
    def loadData(self, dictOfWords : list, dictOfClasses : dict, tabOfImageInfo : list):# wczytuje bazę słów, klas i obrazków
        if not TypeValidator.isDict(dictOfClasses):
            raise ValueError('Bad types of input data (1). dictOfWords must be a dict')
        if not TypeValidator.isTabOfDictsOfInts(list(dictOfWords), len(dictOfClasses)):
            raise ValueError('Bad types of input data (2). dictOfWords must be a tab of dicts of ints and have this same len like tabOfClasses')
        if not TypeValidator.isDictOfInt(dictOfClasses):
            raise ValueError('Bad types of input data (3). dictOfClasses must be a dict of ints')
        if not TypeValidator.isTabOfInts(tabOfImageInfo):
            raise ValueError('Bad types of input data (4). tabOfImageInfo must be a tab of ints')

        self.clear()
        self.__words, self.__classes, self.__images = self.__fillData(dictOfWords, dictOfClasses, tabOfImageInfo)



    def predict(self, inputWords, inputImages, addToData=False): # główna metoda, która odpowiada za przewidywanie stron
        predOfWords = self.__predict(inputWords, inputImages)
        self.printFormattedScores(predOfWords, dramatic=False)

        if(addToData==True):
            classResult = max(predOfWords.items(), key=operator.itemgetter(1))[0]
            self.addData(inputWords, inputImages, classResult)

    def addData(self, inputWords,inputImages, inputClass): # dodaje jedną stronę do bazy stron (bez przewidywania)
        if inputClass in self.__classes:
            self.__classes[inputClass] += 1
            self.__images[inputClass] += inputImages
        else:
            self.__classes[inputClass] = 1
            self.__images[inputClass] = inputImages

        for key in inputWords:
            if(key in self.__words):
                self.__words[key][list(self.__classes.keys()).index(inputClass)] += inputWords[key]

            else:
                newWord = [(int)(0) for i in range(len(self.__classes))]
                newWord[list(self.__classes.keys()).index(inputClass)] = inputWords[key]
                self.__words[key] = newWord

    def clear(self): # czyszczenie klasy
        self.__init__()

    def printWords(self): # Wypisuje bazę danych na konsolę
        for word in self.__words:
            print(word, ': ', self.__words[word])

        print('class : sum of images')
        for key, value in self.__images.items():
            print(key, ' : ', value)

        print('class : sum of pages')
        for key, value in self.__classes.items():
            print(key,' : ', value)

    def printFormattedScores(self, predOfWords, dramatic=True): # wypisuje dane wyjściowe w postaci przystępnej

        if dramatic:
            for key in predOfWords:
                predOfWords[key] **= 2;

        s = sum(predOfWords.values())
        sortedSc = sorted(predOfWords.items(), key=operator.itemgetter(1), reverse=True)
        for x in sortedSc:
            print(x[0], ' :  ', round(x[1] / s * 100, 2), '%')

    def saveToDataToFile(self, filepath): # zapisuje bazę danych do pliku txt
        file = open(filepath, 'w')

        file.write('classes:\n')
        for key, value in self.__classes.items():
            file.write(key+':'+str(value)+'\n')
        file.write('\n')

        file.write('images:\n')
        for key, value in self.__images.items():
            file.write(key+':'+str(value)+'\n')
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