import time
import urllib3
import sys
import re
import threading


class Barvester():

    poolManager = urllib3.PoolManager()

    def __init__(self):
        query = sys.argv[1]
        print("Googling... " + query)
        searchResults = self.getSearchResults(query.replace(" ", "%20"))
        urls = self.extractUrlsFromBody(searchResults)
        self.startCrawling(urls)

    def startCrawling(self, urls):
        extractedUrls = []

        for url in urls:
            time.sleep(2)
            htmlBody = self.retrieveHtmlBody(url)
            extractedUrls += self.extractUrlsFromBody(htmlBody)
            self.hasAnythingInteresting(htmlBody)

        crawlingThread = threading.Thread(target=self.startCrawling, args=[extractedUrls])
        crawlingThread.start()

    def hasAnythingInteresting(self, htmlBody):
        emailPattern = '([a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+.[a-zA-Z0-9.-]+)'
        regexp = re.compile(emailPattern)
        emailsList = regexp.findall(htmlBody)

        if emailsList:
            print(emailsList)

    def getSearchResults(self, searchQuery):
        baseUrl = "http://www.google.com/search?num=1000&q="
        searchUrl = baseUrl + searchQuery
        return self.retrieveHtmlBody(searchUrl)

    def retrieveHtmlBody(self, url):
        headers = {}
        headers['User-Agent'] = "Googlebot"
        htmlBody = self.poolManager.request('GET', url, headers=headers)
        print("[>] Crawling " + url)
        return htmlBody.data

    def extractUrlsFromBody(self, htmlBody):
        urlPattern = '(href[":\/\+?_a-zA-Z=&0-9%.-]+)'
        regexp = re.compile(urlPattern)
        rawUrlsList = regexp.findall(htmlBody)
        urls = []

        for url in rawUrlsList:
            url = url.split('"')

            if len(url) >= 2:
                url = url[1].replace("/url?q=", "")
                if url.__contains__("http") \
                        and not url.__contains__("google") \
                        and not url.__contains__("https") \
                        and not url.__contains__("webmention") \
                        and not url.__contains__("mozilla.org") \
                        and not url.__contains__("facebook") \
                        and not url.__contains__("blogger"):
                    urls.append(url)
        return urls

Barvester()