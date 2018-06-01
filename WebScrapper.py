import bs4
from stemming.porter2 import stem
import urllib3
import requests
import sys
import re

#1.0    initial release         Init
#1.1    Facebook                Social
#1.2    images and videos       IMG


def loadSoup(url, addBrowserHeaders=True, parser='html.parser'):

    if addBrowserHeaders:
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
    else:
        headers = None

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return bs4.BeautifulSoup(response.data, parser)


def splitStrings(soup):
    strings = []
    for ss in soup.stripped_strings:
        if len(ss) == 1: #if len of array is 1, there's no point in splitting
            strings.append(ss[0])
        else:
            for s in ss.split():
                strings.append(s)
    return strings


def getNumericContent(string):
    numbersCount = sum(c.isdigit() for c in string)
    return numbersCount / len(string)


#https://gist.github.com/braveulysses/120193
def sanitize(soup, verbose=False, additional_tags=None):
    if verbose: print('sanitize: before:',len(splitStrings(soup)),'strings')

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
    if verbose: print('sanitize: before:',len(splitStrings(soup)),'strings')
    return soup

def preprocess(strings, verbose=False,
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
        strings = [s for s in strings if getNumericContent(s) < stringsRemovalThreshold]
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
        strings = [s for s in strings if isAscii(s)]
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


def isAscii(s):
    return all(ord(c) < 128 for c in s)


def countPairs(strings):
    d = dict()

    for s in strings:
        if s in d:
            d[s] += 1
        else:
            d[s] = 1
    return d


def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g


def showPairs(dicti, order='count', ascending=False, hideWithLessThan=0):
    if order == 'count':
        for v in sorted(dicti.items(), key=itemgetter(1), reverse=not ascending):
            if v[1] > hideWithLessThan:
                print(v)
    elif order == 'alphabet':
        for key in sorted(dicti, reverse=not ascending):
            if dicti[key] > hideWithLessThan:
                print(key,': ',dicti[key])
    else:
        print('showPairs: unknown order: <',order,'>!')


def getImagesCount(imageSoup):
    image_tags = imageSoup.findAll('img')
    return len(image_tags)


def getImageSizes(imageSoup):
    image_tags = imageSoup.findAll('img')
    sizes = []
    for i in image_tags:
        width = i.get('width')
        height = i.get('height')
        if width is not None and height is not None:
            sizes.append([width, height])
    return sizes

def getImageLinks(imageSoup):
    image_tags = imageSoup.findAll('img')
    return [i.get('src') for i in image_tags]


def scrapPage(url, verbose=False):
    urllib3.disable_warnings()
    #load and clear up HTML soup
    #print(url,'-')
    #sys.stdout.flush()

    if verbose:
        print(url)
    soup = loadSoup(url)

    #print('loaded')
    soup = sanitize(soup)
    #split strings by spaces and newlines - spltting by '/' maybe? EDIT or '='?
    rawStrings = splitStrings(soup)
    #apply filters
    processedStrings = preprocess( rawStrings, removeLongEntries=True )
    #get pairs (word, count)
    pairs = countPairs( processedStrings )
    if verbose:
        print('|')

    imageSoup = loadSoup(url, 'lxml')
    return pairs, getImagesCount(imageSoup)

url = 'https://stackoverflow.com/questions/24878174/how-to-count-digits-letters-spaces-for-a-string-in-python'
url = 'https://www.nytimes.com/interactive/2018/03/22/magazine/voyages-worlds-greatest-hitchhiker.html'
url = 'http://www.vitoshacademy.com/c-wpf-23-well-written-wpf-control-examples/#14'
url = 'https://medium.com/@jamesbridle/something-is-wrong-on-the-internet-c39c471271d2'
url = 'https://medium.freecodecamp.org/we-fired-our-top-talent-best-decision-we-ever-made-4c0a99728fde'
url = 'https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings'
url = 'http://thedailywtf.com/articles/What_Is_Truth_0x3f_'
url = 'https://www.pornhub.com/'
url = 'http://www.scp-wiki.net/scp-504'
url = 'https://www.linkedin.com/pulse/why-outsourcing-your-poland-ruin-life-steve-sydenham/'
url = 'https://dialogwheel.com/2013/11/27/cutting-into-cry-of-fear-alienation-and-identity/'
url = 'https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886'
url = 'https://mydickband.bandcamp.com/'
url = 'https://unix.stackexchange.com/questions/405783/why-does-man-print-gimme-gimme-gimme-at-0030'
url = 'https://gist.github.com/joineral32/ba144be3a696f2d25c66'
url = 'https://github.com/ErisBlastar/cplusequality'
url = 'https://stackoverflow.com/questions/24878174/how-to-count-digits-letters-spaces-for-a-string-in-python'

url = 'http://scp-wiki.wikidot.com/scp-355'

urllib3.disable_warnings()

