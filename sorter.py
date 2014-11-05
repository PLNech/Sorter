#!/usr/bin/python
import sys, os, fileinput
import subprocess

defaultCriteria = "a profanity"
inputLang  = "DE"
outputLang = "EN"

def init():
    loop = 1
    if (len(sys.argv) != 2):
        usage()
    filename = sys.argv[1]
    print "Processing", filename

    print "What is the language code of input language? (default DE)"
    userInput = raw_input("code:")
    if userInput != "":
        inputLang = userInput

    print "What is the language code of the output language? (default EN)"
    userInput = raw_input("code:")
    if userInput != "":
        inputLang = userInput

    while loop == 1:
        print """What is the name of the valid output file?
        (default out.valid.txt)"""
        userInput = raw_input("path: ")
        if userInput == "":
            userInput = "out.valid.txt"
        loop, yesFile = try_open(userInput)
    loop = 1

    while loop == 1:
        print """What is the name of the invalid output file?
        (default out.invalid.txt)"""
        userInput = raw_input("path: ")
        if userInput == "":
            userInput = "out.invalid.txt"
        loop, noFile = try_open(userInput)

    loop = 1
    while loop == 1:
        print """What is the name of the unsure output file?
            (default out.maybe.txt)"""
        userInput = raw_input("path: ")
        if userInput == "":
            userInput = "out.maybe.txt"
        loop, maybeFile = try_open(userInput)

    files = [yesFile, noFile, maybeFile]
    print "What is the selection criteria? (default: a profanity)"
    criteria = raw_input("a world is valid if it is ")
    if criteria is "":
        criteria = defaultCriteria

    print "A word will be kept in", yesFile.name, "if it is", criteria + "."
    sort(filename, files, criteria)

def usage():
    print "Usage:", sys.argv[0], "filename"
    sys.exit()

def try_open(filename):
    try:
        fp = open(filename, 'a+')
        fp.write(" ")
        fp.seek(-1, os.SEEK_END)
        fp.truncate()
        return (0, fp)
    except IOError, e:
        print "The file requested could not be opened:"
        print e.errno, e
        return (1, None)


def sort(filename, files, criteria = defaultCriteria):
    for each_line in fileinput.input(filename):
        process(each_line, criteria, files)

def process(word, criteria, files):
    yesFile = files[0]
    noFile = files[1]
    maybeFile = files[2]
    value = 42

    while (value > 2):
        value = queryWord(word, criteria)
        if (value == 0):
            print word, "is", criteria + "."
            yesFile.write(word)
            yesFile.flush()
        elif(value == 1):
            print word, "is not", criteria + "."
            noFile.write(word)
            noFile.flush()
        elif(value == 2):
            print word, "is maybe", criteria + "."
            maybeFile.write(word)
        else:
            define(word)

def queryWord(word, criteria):
    #Answers:
    #0: Yes
    #1: No
    #2: Definition
    default = "def";
    choice = "todo";
    valid = {"y":0, "ye":0,          "yes"   :0,
            "n":1,                  "no"    :1,
            "m":2, "ma":2, "may":2, "maybe" :2,
            "d":3, "de":3, "def":3, "define":3}
    print "Is " + word.replace("\n",""), criteria + "?"
    while choice not in valid:
        choice = raw_input().lower()
        if choice is not None and choice == '':
            if default in valid:
                return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stderr.write("Please answer with yes (y), no (n), def (d) or maybe (m).\n")

def define(word):
    print "Let's define", word
    subprocess.call("./dict.cc.py " + inputLang + " "
            + outputLang + " " + word, shell="True")
    print "\n"



if __name__ == '__main__':
    init()
