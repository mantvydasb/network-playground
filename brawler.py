import urllib3
import re

BASE_URL = "http://www.google.co.uk/search?num=500&q="
QUERY = "%laura.klimaviciute@gmail.com%22"
SEARCH_URL = BASE_URL + QUERY
URL_PATTERN = '(href[":\/\+?_a-zA-Z=&0-9%.-]+)'
RESULTS_PER_PAGE = 1000
HEADERS = {}
HEADERS['User-Agent'] = 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
URL_REGEX = re.compile(URL_PATTERN)
POOL_MANAGER = urllib3.PoolManager()

def getRequestData():
    global request, response
    request = POOL_MANAGER.request('GET', SEARCH_URL, headers=HEADERS)
    response = request.data

def printOutUrls():
    urlsList = URL_REGEX.findall(response)
    for url in urlsList:
        url = url.split('"')

        if len(url) >= 2:
            url = url[1]
            if "http" in url or "https" in url:
                print(url)

getRequestData()
printOutUrls()