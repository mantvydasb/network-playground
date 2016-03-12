import urllib3
import urllib.parse

class Bruter:

    postUrl = "http://192.168.2.8/phpMyAdmin/index.php?token=ff022fa5b1845dcf5dfbd84c4e3a4964"
    usernameField = "pma_username"
    passwordField = "pma_password"
    usernameValue = "msfadmin"
    passwordValue = "msfadmin"
    poolManager = urllib3.PoolManager()

    def __init__(self):
        print("Starting..")
        fields = { self.usernameField: self.usernameValue, self.passwordField: self.passwordValue}
        req = self.poolManager.request("POST", self.postUrl, fields=fields, headers={'Content-type': 'application/x-www-form-urlencoded'})
        print(req)

Bruter()
