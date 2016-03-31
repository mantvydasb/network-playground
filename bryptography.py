from Crypto.Util import *
from Crypto.PublicKey import *
from Crypto.PublicKey import RSA

publicKey = open("keys/public.crt", 'r')
publicKey = publicKey.read()
RSAkey = RSA.importKey(publicKey)