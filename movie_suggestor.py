import bruter
from urllib import request

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
        self.linkomania.attemptLogin(username=self.username, password=self.password)

    def sendRequest(self, url):
        response = self.linkomania.getUrlContent(url, self.linkomania.headers)
        return response

    def getRecentlyUploadedMovies(self):
        return self.sendRequest(self.latestMovies)

movieSuggestor = MovieSuggestor()
recentMovies = movieSuggestor.getRecentlyUploadedMovies()
print(str(recentMovies))
