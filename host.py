# Echo server program
import os, socket, sys
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import SHA
from Crypto.Cipher import AES


CLIENTHOST = ''
#'128.153.180.19'
HOST = ''                 # Symbolic name meaning all available interfaces
#128.153.180.30
PORT = 50007              # Arbitrary non-privileged port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(7)
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "waiting for a connection"
conn, addr = server.accept()
print "connection received"

def send_enc(message, cipher):
    if len(message) % 16 != 0:
        left = 16 - (len(message) % 16)
        for i in range(0,left):
            message = message + ' '

    encmsg = cipher.encrypt(message)
    conn.sendall(encmsg)

def rec_msg():
    while 1:
        data = conn.recv(1024)
        if not data: break
#        conn.sendall(data)
        return data

def generate_elgamal(klength, privatekey):
    key = ElGamal.generate(klength, Random.new().read)
    h = SHA.new(privatekey).digest()
    while 1:
        k = random.StrongRandom().randint(1,key.p-1)
        if GCD(k, key.p-1) == 1: break
    sig = key.sign(h,k)
    if key.verify(h,sig):
        print "OK"
        return key, h , sig
    else:
        print "Incorrect signature"
        return None

def generate_aes(key):
    secretkey = key.encode('utf-8')
#    iv = Random.new().read(AES.block_size)
    cipher = AES.new(secretkey)
#    cipher = AES.new(key)
    return cipher

def startconnection(bitlength):
        elgamalkey = "huehuehue"
        # Generates the elgamal key
        key, h, sig = generate_elgamal(bitlength, elgamalkey)
        #gets the public key to share and then sends it
        publickey = key.publickey()
        data = str(publickey.p) + '\n' + str(publickey.g) + '\n' + str(publickey.y)
        conn.sendall(data)
        # recieves the encrypted key for aes back
        encmsg = rec_msg()
        # splits the message into readable parts
        splitmsg = encmsg.split('\n')
        # decrypts the message to get the key
        AESKEY = str(key.decrypt((splitmsg[0],splitmsg[1])))

        print 'aes key is: ' + AESKEY
        length = len(AESKEY)
        if length % 16 != 0:
            left = 16 - (length % 16)
            for i in range(0,left):
                AESKEY = AESKEY + ' '
        # generates the cipher from the aeskey to send encrypted
        cipher = generate_aes(AESKEY)
        return cipher

def talk():
    print 'to send a message type a * then hit CTRL-D'
    message = ""
    for line in sys.stdin:
        if 'quit()' in line:
            print 'exiting'
            return 'quit()'
        if '*' in line:
            return message + line
        message = message + line
    return message

def listen():
    print 'Their message:'
    while 1:
        data = conn.recv(1024)
        if not data: break
        return data

def chat(cipher):
    while 1:
        message = talk()
        if 'quit()' in message:
            return
        #conn.sendall(message)
        send_enc(message, cipher)
        print cipher.decrypt(listen())

def main():
    options = sys.argv
    bitlength = 256
    
    if '-bitlength' in options:
        i = options.index('-bitlength')
        bitlength = int(options[i+1])

    message = 'testing connection'
    elgamalkey = []
    aeskey = ''
    if '-help' in options:
        print 'type -bitlength to specify the bitlength for ElGamal or the defualt will be 256.'
        return
    
    cipher = startconnection(bitlength)
    send_enc(message, cipher)
    encmsg = rec_msg()
    print 'enc is: ' + encmsg
    theirmessage = cipher.decrypt(encmsg)
    
    print 'their message is: ' + theirmessage
    print 'to quit type quit()'
    chat(cipher)
if __name__ == '__main__':
    main()
    conn.close()
    server.close()
