from Crypto.PublicKey import RSA

data = "tis gona beh encrypted message"
privateKey = RSA.generate(1024)
publicKey = privateKey.publickey()

print("Encrypting... %s" % data)
encryptedMessage = publicKey.encrypt(data, 32)
print(encryptedMessage)

print("Decrypting back..")
decryptedMessage = privateKey.decrypt(encryptedMessage)
print(decryptedMessage)