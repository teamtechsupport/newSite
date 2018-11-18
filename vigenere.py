import annealing_decryption
import re
import random
import math
import string
from threading import Thread

# http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher-part-2/


def vigenere(text, keylen):
    key = "A"*keylen

    print(annealing_decryption.anneal(
        text, key, "vigenere", "rand", ""))


userinput = input("Enter encoded text:\n").upper()
regex = re.compile('[^A-Z]')

try:
    keylen = int(
        input("Enter number of letters in key; if unknown enter '0' to cycle through 2-20: "))
except:
    print("Not an integer, cycling through possibilities 2-20.")
    keylen = 1

if keylen > 1:
    vigenere(regex.sub('', userinput), keylen)

else:
    for x in range(2, 21):
        process = Thread(target=vigenere, args=[
                         regex.sub('', userinput), x])
        process.start()
