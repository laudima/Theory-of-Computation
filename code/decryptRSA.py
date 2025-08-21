# Decrypt RSA

import sys
import os
import base64

def decrypt_rsa(d, n, cipherText):
    message = []
    for i in range(len(cipherText)):
        message.append(pow(cipherText[i], d, n))

    print(message)
    message_string = ''.join([chr(i) for i in message])
    return message_string

cipherText = [138527, 171279, 138664, 242409, 103298, 171279, 27261, 103786, 0, 103298, 0, 103298, 242409, 224525, 188808, 171279, 27261]
d = 13 
n = 256961
e = 59029
phi_n = 255792

message = decrypt_rsa(d, n, cipherText)
print(message)
# [5, 4, 11, 8, 2, 4, 18, 21, 0, 2, 0, 2, 8, 14, 13, 4, 18] list of characters 
