import bruter
import xml.etree.ElementTree as xmlTree
from urllib import request

class Torrent:
    title = ''
    description = ''
    link = ''

    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link

class MovieSuggestor():


    linkomaniaCookie = "PHPSESSID=d44a3mfqe1udekmfi54cb0p2h7;"
    linkomania = ''

    baseUrl = "https://www.linkomanija.net/"
    loginUrl = baseUrl + "takelogin.php"
    searchUrl = baseUrl + "browse.php?incldead=0&search="
    latestMovies = baseUrl + "rss.php?feed=link&cat[]=29&cat[]=52&cat[]=53&cat[]=61&passkey=14aba47f3165387ebaaf0aba38c140c2"

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
                torrent = Torrent(title, description, link)
                torrents.append(torrent)

        return torrents

    def sendRequest(self, url):
        response = self.linkomania.getUrlContent(url, self.linkomania.headers)
        return response

    def getRecentlyUploadedMovies(self):
        return self.sendRequest(self.latestMovies)

movieSuggestor = MovieSuggestor()
movieSuggestor.login()

recentMovies = movieSuggestor.getRecentlyUploadedMovies()
torrenstFeed = movieSuggestor.parseXMLfromString(recentMovies)
torrents = movieSuggestor.parseTorrents(torrenstFeed)

for torrent in torrents:
    print(torrent.title)

# print(str(recentMovies))
