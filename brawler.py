import urllib3

a = urllib3.PoolManager()
r = a.request('GET', 'http://google.com/')

print(r.status, r.data)
