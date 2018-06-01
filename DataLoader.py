import WordRepository as repo
import WebScrapper
import ExcelReader
import queue
import threading
import time


class DataLoader:

    def __init__(self, verbose=False):
        self.repository = repo.WordRepository() # categories, words and urls
        self.verbose = verbose
        self.excelDictionary = None # links and categories loaded from xlsx file

    # init word repository from JSON file
    def loadRepoFromJSON(self, fileName):
        try:
            self.repository = repo.WordRepository.deserialize(fileName)
            if self.verbose:
                print('DataLoader::loadFromJSON: loaded ', len(self.repository.data) ,' categories')
            return True
        except FileNotFoundError:
            if self.verbose:
                print('DataLoader::loadFromJSON: cannot find file "', fileName ,'"')
            return False

    # open Excel file and read links with categories
    def loadClassesAndCategoriesFromExcel(self, fileName):
        self.excelDictionary = ExcelReader.ExcelReader.readLinksAndCategories(fileName, verbose=self.verbose)

        if self.verbose:
            count = 0
            for links in self.excelDictionary.values():
                count += len(links)
            print('DataLoader::loadFromExcel: loaded', count, ' pairs')

    # find and download missing sites
    def scrapMissingSites(self):

        urls = self.repository.getAllUrls()

        unscrappedCount = 0
        unscrappedDictionary = dict()
        for category, links in self.excelDictionary.items():
            for link in links:
                if link not in urls:
                    if category not in unscrappedDictionary:
                        unscrappedDictionary[category] = list()
                    unscrappedDictionary[category].append(link)
                    unscrappedCount += 1


        if self.verbose:
            print('DataLoader::scrapMissing: found',unscrappedCount,'unscrapped urls')

        resultUrls, resultPages, resultImagesCount, resultClasses = self.scrapFromNet(unscrappedDictionary)

        for i in range(len(resultPages)):
            self.repository.appendInBulk(resultUrls[i], resultClasses[i], resultPages[i], resultImagesCount[i])

    # download sites from given dictionary
    def scrapFromNet(self, dicti):

        flat = self.flattenDictionary(dicti)

        if len(flat) == 0:
            if self.verbose:
                print('DataLoader::scrapFromNet: nothing to do here, skipping')
            return list(), list(), list(), list()

        if self.verbose:
            print('DataLoader::scrapFromNet: started loading words')

        workQueue = queue.Queue(maxsize=0)
        num_threads = min(64, len(flat))

        for i in range(len(flat)):
            workQueue.put((i,flat[i]))

        def crawl(q, resultPages, resultImagesCount, resultClasses, resultUrls):
            while not q.empty():
                work = q.get()

                category = work[1][0]
                url = work[1][1]

                pageData, imagesCount = WebScrapper.Scrapper().scrapPage(url, self.verbose)

                resultPages[work[0]] = pageData
                resultImagesCount[work[0]] = imagesCount
                resultClasses[work[0]] = category
                resultUrls[work[0]] = url

                q.task_done()


        start = time.time()

        resultPages = [0] * len(flat)
        resultClasses = [0] * len(flat)
        resultUrls = [0] * len(flat)
        resultImagesCount = [0] * len(flat)
        for i in range(num_threads):
            worker = threading.Thread(target=crawl, args=(workQueue, resultPages, resultImagesCount, resultClasses, resultUrls))
            worker.setDaemon(True)
            worker.start()

        workQueue.join()

        end = time.time()
        if self.verbose:
            print('DataLoader::scrapFromNet: finished, time elapsed:',round(end - start, 3), 's')

        return resultUrls, resultPages, resultImagesCount, resultClasses

    # ...
    def flattenDictionary(self, dictionary):
        flat = []
        for key in dictionary.keys():
            for value in dictionary[key]:
                flat.append((key, value))
        return flat

    # save repository to JSON file
    def saveToJSON(self, fileName):
        self.repository.serialize(fileName)

    # get learning data
    def getPagesClassesAndImagesCount(self):
        return self.repository.getPagesClassesAndImagesCount()