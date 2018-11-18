import decrypt
import re
import random
import math
import itertools
import requests
from threading import Thread


class ngram_obj(object):
    def __init__(self, ngrampaste):  # runs on object creation
        self.ngrams = {}  # create the ngram dict
        req = requests.get(ngrampaste)  # get the raw ngram paste
        txt = req.text  # get the text only
        for ln in txt.splitlines():  # for each line in the text
            # split it again, assigning each value on that line a variable
            key, freq = ln.split(" ")
            self.ngramlen = len(key)
            # make a new key-int pair with those two variables log10 to reduce the score's size so it can later be inserted into an exponential function (its relative anyway)
            self.ngrams[key] = int(freq)
        self.valtotal = sum(self.ngrams.values())
        for key in list(self.ngrams.keys()):
            self.ngrams[key] = self.ngrams[key]

    def cost(self, string):  # string is an uppercase est solution
        cost = 0
        l = len(string)
        for i in range(l-(self.ngramlen+1)):  # for length of string - length of ngrams
            teststr = string[i:i+self.ngramlen]
            if teststr in self.ngrams:  # check if selected ngram is in the dict
                cost += self.ngrams[teststr]  # if yes add that word's score
        return(cost)


def transpos(text, colno):
    initkey = list(str(math.floor(1234567890 / (10**(10-colno)))))

    perms = list(itertools.permutations(initkey))

    key = ""
    cost = 0
    ngram = ngram_obj(
        "https://gist.githubusercontent.com/DomDale/9a582deed33b20bb47e0363301d2c6c4/raw/62e7416f6be95893649398f0470f1dcd2668e608/english_trigrams.txt")
    for x in range(len(perms)):
        newcost = ngram.cost(decrypt.decrypt(
            text, "".join((perms[x])), "transposition"))
        if newcost > cost:
            cost = newcost
            key = "".join((perms[x]))

    print(decrypt.decrypt(
        text, key, "transposition"))


regex = re.compile('[^A-Z]')
