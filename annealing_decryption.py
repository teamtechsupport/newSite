# http://katrinaeg.com/simulated-annealing.html
# http://www.theprojectspot.com/tutorial-post/simulated-annealing-algorithm-for-beginners/6
import decrypt
import requests
import string
import random
import math
import re


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
        for key in list(self.ngrams.keys()):  # for every three letter pair
            # Take log base 10 of  (value / the total of all values) to get a score
            self.ngrams[key] = math.log10(
                float(self.ngrams[key])/self.valtotal)
            # all scores will be negative but the more often the trigram appears, the less negative it will be

    def cost(self, string):  # string is an uppercase est solution
        cost = 0
        l = len(string)
        for i in range(l-(self.ngramlen+1)):  # for length of string - length of ngrams
            teststr = string[i:i+self.ngramlen]
            if teststr in self.ngrams:  # check if selected ngram is in the dict
                cost += self.ngrams[teststr]  # if yes add that word's score
        return(cost)


def acceptprob(ncost, ocost, temp):
    # equation inspired by metalworking hence the name
    try:
        return(math.exp(ncost-ocost)/temp)
    except:
        pass


def findneighbor(key, keytype, keybreak):
    if keybreak == "":
        keylist = list(key)
    else:
        keylist = key.split(keybreak)

    if keytype == "swap":
        # store the two letters locations being swapped
        # if ciphertype == "transposition":
        # swaploc.append(swaploc[0]+1)
        # else:
        swaploc = [random.randint(0, len(key)-1),
                   random.randint(0, len(key)-1)]

        # store the two letters being swapped
        swaplet = [keylist[swaploc[0]], keylist[swaploc[1]]]
        keylist[swaploc[0]] = swaplet[1]
        keylist[swaploc[1]] = swaplet[0]  # swap the two letters
    elif keytype == "rand":
        keylist[random.randint(0, len(
            keylist)-1)] = string.ascii_uppercase[random.randint(0, len(string.ascii_uppercase)-1)]
    return "".join(keylist)


def anneal(text, key, ciphertype, keytype, keybreak):
    ngram = ngram_obj(
        "https://gist.githubusercontent.com/DomDale/9a582deed33b20bb47e0363301d2c6c4/raw/62e7416f6be95893649398f0470f1dcd2668e608/english_trigrams.txt")
    cost = ngram.cost(decrypt.decrypt(text, key, ciphertype))
    temp = 1.0
    tempmin = 0.0001
    alpha = 0.99  # multiplication factor
    iters = 10  # iterations at each temperature
    acc = 0
    while temp > tempmin:
        for x in range(1, iters):
            newkey = findneighbor(key, keytype, keybreak)
            newcost = ngram.cost(decrypt.decrypt(text, newkey, ciphertype))

            ap = acceptprob(newcost, cost, temp)
            try:
                if ap > random.random():
                    key = newkey
                    cost = newcost
                    acc += 1
            except:
                key = newkey
                cost = newcost
                acc += 1

        temp *= alpha  # slowly reduce temp
    return(decrypt.decrypt(text, key, ciphertype))
