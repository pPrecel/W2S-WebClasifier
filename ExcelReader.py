import pandas
import math


class ExcelReader:

    # returns dictionary of pairs (url, category)
    def readLinksAndCategories(fileName, verbose=True):

        if verbose:
            print('ExcelReader::read: reading "',fileName,'"')

        # load Excel file
        try:
            data = pandas.read_excel(fileName)
        except FileNotFoundError:
            print('ExcelReader::read: file "',fileName,'" not found.')
            return dict()

        # get values
        try:
            links = data['link'].values
            categories = data['category'].values
        except KeyError:
            print('ExcelReader::read: invalid Excel file! We need "link" and "category" columns!')
            return dict()

        pairs = dict()

        # foreach loaded pair
        for i in range(len(data.values)):

            # check
            if ExcelReader.isLoadedWordInvalid(links[i]):
                if verbose:
                    print('ExcelReader::read: no value for link, skipping')
                continue;
            if ExcelReader.isLoadedWordInvalid(categories[i]):
                if verbose:
                    print('ExcelReader::read: no value for category, skipping!')
                continue;


            # add category IF NOT EXISTS
            if categories[i] not in pairs.keys():
                pairs[categories[i]] = list()
            #add new links
            pairs[categories[i]].append(links[i])

        # for debugging
        if verbose:
            s  = 0
            for k in pairs.keys():
                print(k, len(pairs[k]))
                s += len(pairs[k])

            print('total: ',s)

        return pairs

    # when the cell is empty, pandas returns nan
    def isLoadedWordInvalid(word):
        return isinstance(word, float) and math.isnan(word)