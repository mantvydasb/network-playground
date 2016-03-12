import urllib3
import urllib.parse

class Bruter:

    baseUrl = "http://192.168.2.1/"
    postUrl = baseUrl + "cgi-bin/login.exe"

    poolManager = urllib3.PoolManager()

    def __init__(self):
        print("Starting..")
        fields = {"pws" : self.pws}
        req = self.poolManager.urlopen("POST", self.postUrl, headers={'content-type': 'application/x-www-form-urlencoded'}, body={'pws': self.pws})
        response = self.poolManager.request('POST', self.postUrl, fields=fields, headers={'content-type': 'application/x-www-form-urlencoded'})
        print(req)

Bruter()
