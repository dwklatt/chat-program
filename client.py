#echo client program
import sys
import socket
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Cipher import AES


def findMessage(initVector, decryptedMessageObject):
	message = ""
	
	for i in range(len(initVector), len(decryptedMessageObject)):
		message = message + decryptedMessageObject[i]

	return message
			
def generate_aes(key):
#    secretkey = bytes(key, 'utf-8')
    secretkey = key.encode('utf-8')
#    initVector = Random.new().read(AES.block_size)
    cipher = AES.new(secretkey)
#    msg = message.encode('utf-8')
#    enc_msg = iv + cipher.encrypt(b'Attack at dawn')
#    enc_msg = iv + cipher.encrypt(msg)
    return cipher

#server testing
	
privateKey = "squirrelninjaarm"
HOST = ''
#"128.153.180.30" #"128.153.180.30"    # The remote host
PORT = 50007              # The same port as used by the server

#make the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#making the aesKey
aesKey = generate_aes(privateKey)
#print 'iv is: ' + initVector

#Receiving elGamal keys
data = s.recv(1024)
#g = s.recv(1024)
#y = s.recv(1024)

#p is first string, g is 2nd string, y is 3rd string
keyArray = data.split('\n')
p = int(keyArray[0])
g = int(keyArray[1])
y = int(keyArray[2])

print 'p is: ' + str(p)
print 'g is: ' + str(g)
print 'y is: ' + str(y)

#make an elgamal object
publickey = ElGamal.construct((p,g,y))

#encrypting the privateKey and initVector
elGamalEncryption = publickey.encrypt(privateKey, random.randint(1, p - 2))
#initVectorEncryption = publickey.encrypt(initVector, random.randint(1, p - 2))

#send over the privateKey and initVector with masks
encryptMessage = str(elGamalEncryption[0]) + '\n' + str(elGamalEncryption[1])

#+ '\n' + str(initVectorEncryption[0]) + '\n' + str(initVectorEncryption[1])

#print initVectorEncryption[0]
#print initVectorEncryption[1]

s.sendall(encryptMessage)

#receive cipher back
messageCipher = s.recv(1024)
message = aesKey.decrypt(messageCipher)
#message = findMessage(initVector, aesKey.decrypt(messageCipher))


print 'the message is: ' + message
#s.sendall(aesKey)
#data = s.recv(1024)
message = "It worked       "
messageCipher = aesKey.encrypt(message)
s.sendall(messageCipher)
s.close()
#print 'Received', repr(data)
