import bruter
import xml.etree.ElementTree as xmlTree
import re
from urllib import request

class Torrent:
    title = ''
    description = ''
    link = ''
    uploadDate = ''

    def __init__(self, title, description, link, uploadDate):
        self.title = title
        self.description = description
        self.link = link
        self.uploadDate = uploadDate

class MovieSuggestor():



    linkomaniaCookie = "PHPSESSID=d44a3mfqe1udekmfi54cb0p2h7;"
    linkomania = ''

    baseUrl = "https://www.linkomanija.net/"
    loginUrl = baseUrl + "takelogin.php"
    searchUrl = baseUrl + "browse.php?incldead=0&search="
    latestMovieFeed = baseUrl + "rss.php?feed=link&cat[]=29&cat[]=52&cat[]=53&cat[]=61&passkey=14aba47f3165387ebaaf0aba38c140c2"

    def __init__(self):
        self.linkomania = bruter.Bruter(
            loginUrl=self.loginUrl,
            usernameField="username",
            passwordField="password",
            headers={"Cookie": self.linkomaniaCookie}
        )

    def login(self):
        response = self.linkomania.attemptLogin(username=self.username, password=self.password)
        return response

    def parseXMLfromString(self, string):
        root = xmlTree.fromstring(string)
        return root

    def parseTorrents(self, root):
        torrents = []

        for child in root[0]:
            if child.tag == "item":
                title = str(child.find("title").text).replace(" ", ".")
                description = child.find("description").text
                link = child.find("link").text
                uploadDate = child.find("pubDate").text
                torrent = Torrent(title, description, link, uploadDate)
                torrents.append(torrent)

        return torrents

    def sendRequest(self, url):
        response = self.linkomania.getUrlContent(url, self.linkomania.headers)
        return response

    def getDecentlyRatedMovies(self, torrents):
      for torrent in torrents:
            isDecentlyRated = re.search('(<b>Rating:<\/b> [6-9.]+\w)', torrent.description)
            if isDecentlyRated:
                rating = isDecentlyRated.group(0).strip("<b>Rating:</b> ")
                print("[%s imdb] %s " %(rating, torrent.title))


    def getLatestMoviesFeed(self):
        return self.sendRequest(self.latestMovieFeed)

movieSuggestor = MovieSuggestor()
movieSuggestor.login()

recentMovies = movieSuggestor.getLatestMoviesFeed()
torrenstFeed = movieSuggestor.parseXMLfromString(recentMovies)
torrents = movieSuggestor.parseTorrents(torrenstFeed)
decentlyRatedMovies = movieSuggestor.getDecentlyRatedMovies(torrents)

