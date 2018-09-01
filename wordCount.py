 #! /usr/bin/env python3

import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists

# set input and output files method from wordCountTest.py
if len(sys.argv) is not 3:
    print("Correct usage: wordCount.py <input text file> <output file>")
    exit()
 
fin = sys.argv[1]
fout = sys.argv[2]

#make sure text files exist
if not os.path.exists(fin):
    print ("text file input %s doesn't exist! Exiting" % fin)
    exit()

w = 0

dictionary = {} 

#try open fin modified from wordCountTest.py
with open(fin, 'r') as inputFile:
    for line in inputFile:
        #rid newline
        line = line.strip()
        # split on whitespace and punctuation
        words = re.split('[^A-Za-z]', line)
        for word in words:
 #           print(word)
            word = word.lower()
            word = re.sub('[^a-z]', '' , word)
            if word != '':
                if word in dictionary:
                    dictionary[word] +=1

                else:
                    dictionary[word] = 1
#                print(dictionary, '95') print(sorted(dictionary)) print(dictionary)
f = open(fout,'w')
for key,value in sorted(dictionary.items()):
#    print(key,value)
    f.write(key +' '+ str(value) + '\n')