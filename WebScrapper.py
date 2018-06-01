from stemming.porter2 import stem
from Utilities import Utility
import bs4
import urllib3
import requests
import re

#1.0    initial release         Init
#1.1    Facebook                Social
#1.2    images and videos       IMG
#1.3    wrapped in class        Classic

class Scrapper:

    def __init__(self):
        urllib3.disable_warnings()

    #load BeautifulSoup from url
    def loadSoup(self, url, addBrowserHeaders=True, parser='html.parser'):

        #fake header to bypass some websites' security
        fakeUserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

        if addBrowserHeaders:
            headers = requests.utils.default_headers()
            headers.update({
                'User-Agent': fakeUserAgent,
            })
        else:
            headers = None

        http = urllib3.PoolManager()
        response = http.request('GET', url)
        return bs4.BeautifulSoup(response.data, parser)

    # split soup strings into a collection of separate words
    def splitStrings(self, soup):
        strings = []
        for ss in soup.stripped_strings:
            if len(ss) == 1: #if len of array is 1, there's no point in splitting
                strings.append(ss[0])
            else:
                for s in ss.split():
                    strings.append(s)
        return strings

    # https://gist.github.com/braveulysses/120193
    def sanitize(self, soup, verbose=False, additional_tags=None):
        if verbose: print('sanitize: before:',len(self.splitStrings(soup)),'strings')

        tag_whitelist = [
            'a', 'abbr', 'address', 'b', 'code',
            'cite', 'em', 'i', 'ins', 'kbd',
            'q', 'samp', 'small', 'strike', 'strong', 'sub',
            'sup', 'var'
        ]

        if additional_tags is not None:
            tag_whitelist.extend(additional_tags)

        attr_whitelist = {
            'a': ['href', 'title', 'hreflang'],
            'img': ['src', 'width', 'height', 'alt', 'title']
        }

        tag_blacklist = [ 'script', 'style' ]

        attributes_with_urls = [ 'href', 'src' ]

        for comment in soup.findAll(
            text=lambda text: isinstance(text, bs4.Comment)):
            comment.extract()
        for tag in soup.findAll():
            if tag.name.lower() in tag_blacklist:
                tag.extract()
            elif tag.name.lower() not in tag_whitelist:
                tag.hidden = True
            else:
                for attr in tag.attrs:
                    if tag.name.lower() in attr_whitelist and attr[0].lower() in attr_whitelist[ tag.name.lower() ]:
                        if attr[0].lower() in attributes_with_urls:
                            if not re.match(r'(https?|ftp)://', attr[1].lower()):
                                tag.attrs.remove(attr)
        if verbose: print('sanitize: before:',len(self.splitStrings(soup)),'strings')
        return soup

    # perform collecction cleanup
    def preprocess(self, strings, verbose=False,
                   removeNumericStrings=True, stringsRemovalThreshold=0.1,
                   removeLinks=True,
                   toLowerCase=True,
                   stripTrailingPunctuation=True, punctuation ='|&<>\“”"_=:!.,()?…\/{}][;:',  #todo - replace instead of strip?
                   removeEmptyEntries=True,
                   removeShortEntries=True, minEntryLength=2,
                   removeLongEntries=False, maxEntryLength=20,
                   removeTheAAn=True,
                   stemming=True,
                   stripTrailingNumbers=True,
                   removeNonAsciiWords=True,
                   ):

        if verbose: print('preprocess: started with',len(strings),'strings')

        if toLowerCase:
            strings = [s.lower() for s in strings]

        if removeNumericStrings:
            strings = [s for s in strings if Utility.getNumericContent(s) < stringsRemovalThreshold]
            if verbose: print('preprocess: removeNumbers:',len(strings),'strings')

        if removeLinks:
            strings = [s for s in strings if re.match('https?://(?:[-\*w.]|(?:%[\da-fA-F]{2}))+', s) == None]
            if verbose: print('preprocess: removeLinks:',len(strings),'strings')

        if removeLongEntries:
            strings = [s for s in strings if len(s) <= maxEntryLength]
            if verbose: print('preprocess: removeLongEntries:', len(strings),'strings')

        if removeTheAAn:
            theAAn = ['the', 'a', 'an']
            strings = [s for s in strings if s not in theAAn]
            if verbose: print('preprocess: removeTheAAn:', len(strings),'strings')

        if removeNonAsciiWords:
            strings = [s for s in strings if Utility.isAscii(s)]
            if verbose: print('preprocess: removeNonAsciiWords:',len(strings),'strings')

        if stripTrailingPunctuation:
            for i, s in enumerate(strings):
                for p in punctuation:
                    strings[i] = s.rstrip(p).lstrip(p)

        if stripTrailingNumbers:
            numbers = '1234567890'
            for i, s in enumerate(strings):
                for p in numbers:
                    strings[i] = s.rstrip(p).lstrip(p)

            for i in range(len(strings)):
                for p in punctuation:
                    strings[i] = strings[i].rstrip(p).lstrip(p)

            newstrings = []
            for i in range(len(strings)):
                s = strings[i]
                for p in punctuation:
                    s = s.rstrip(p).lstrip(p)
                newstrings.append(s)
            strings = newstrings

        if removeEmptyEntries:
            strings = [s for s in strings if s != None]
            if verbose: print('preprocess: removeEmptyEntries:', len(strings),'strings')

        if removeShortEntries:
            strings = [s for s in strings if len(s) >= minEntryLength]
            if verbose: print('preprocess: removeShortEntries:', len(strings),'strings')

        if stemming:
            strings = [stem(s) for s in strings]

        return strings

    # get count of 'img' tags in HTML soup
    def getImagesCount(self, imageSoup):
        image_tags = imageSoup.findAll('img')
        return len(image_tags)

    # [unused] get height and widths (if any) in HTML soup
    def getImageSizes(self, imageSoup):
        image_tags = imageSoup.findAll('img')
        sizes = []
        for i in image_tags:
            width = i.get('width')
            height = i.get('height')
            if width is not None and height is not None:
                sizes.append([width, height])
        return sizes

    # [unused] get links of images
    def getImageLinks(self, imageSoup):
        image_tags = imageSoup.findAll('img')
        return [i.get('src') for i in image_tags]

    # scrap page, returning dictionary of word occurences and image count
    def scrapPage(self, url, verbose=False):

        if verbose:
            print(url)
        soup = self.loadSoup(url)

        soup = self.sanitize(soup)
        #split strings by spaces and newlines - spltting by '/' maybe? EDIT or '='?
        rawStrings = self.splitStrings(soup)
        #apply filters
        processedStrings = self.preprocess( rawStrings, removeLongEntries=True )
        #get pairs (word, count)
        pairs = Utility.countPairs( processedStrings )
        if verbose:
            print('|')

        imageSoup = self.loadSoup(url, 'lxml')
        return pairs, self.getImagesCount(imageSoup)

    urllib3.disable_warnings()

