from Crypto.PublicKey import RSA

plainText= "tis gona beh encrypted message"
privateKey = RSA.generate(1024)
publicKey = privateKey.publickey()

print("Encrypting... %s" % plainText)
cipherText = publicKey.encrypt(plainText, 32)
print(cipherText)

print("Decrypting back..")
plainText = privateKey.decrypt(cipherText)
print(plainText)
