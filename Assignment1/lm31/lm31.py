# load the file
import os
import glob
import re
import nltk
import operator
import json
from collections import Counter
from nltk.util import ngrams
import ntpath
import sys


path = sys.argv[1]
# path = './res/train_data/'

cleanedPath = './res/cleaned/train_data/'
os.makedirs(cleanedPath, mode=0o777, exist_ok=True)

n4gram = []
n3gram = []

# gets all the files in the directory
dir_name = "./"
all_files = os.listdir(dir_name)

# removes all .txt files before starting to run the program
for item in all_files:
    if item.endswith(".txt"):
        os.remove(os.path.join(dir_name, item))

# function to return the file name from the path


def path_leaf(x):
    head, tail = ntpath.split(x)
    return tail or ntpath.basename(head)


all_words = []

# getting all files in single file for words count
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(filename, 'r', encoding='latin-1') as infile, open('allWords.txt', 'a+') as outfile:
        for line in infile:
            if not line.strip():
                continue
            line = line.replace('\n', ' ') + ' '
            outfile.write(re.sub(' +', ' ', line))

#getting a count of all the words in the dataset
with open('allWords.txt') as infile:
    infile.seek(0)
    lines = infile.read()
    words = lines.split()
    # words = nltk.word_tokenize(lines)
    wordCountDictionary = Counter(words)

# replace all UNK in new separate files
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(filename, 'r', encoding='latin-1') as infile, open((cleanedPath+path_leaf(filename)), 'w') as outfile:
        lines = infile.read()
        words = lines.split()
        # words = nltk.word_tokenize(lines)

        for i, w in enumerate(words):
            if wordCountDictionary[w] <= 5:
                words[i] = 'UNK'
            outfile.write(words[i] + ' ')

#
# find 4 grams and 3 grams form all files separately
for filename in glob.glob(os.path.join(cleanedPath, '*.txt')):
    with open(filename, 'r', encoding='latin-1') as infile, open('output.txt', 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue
            outfile.write(re.sub(' +', ' ', line.replace('\n', ' ')))

    with open("output.txt") as infile:
        lines = infile.read()
        # tokens = nltk.word_tokenize(lines)
        tokens = lines.split()

    for x in range(0, len(tokens)-3):
        n4gram.append(tokens[x] + ' ' + tokens[x+1] + ' ' + tokens[x+2] + ' ' + tokens[x+3])

    for x in range(0, len(tokens)-2):
        n3gram.append(tokens[x] + ' ' + tokens[x+1] + ' ' + tokens[x+2])

    outfile.close()

ngram_with_unk = []

dictionary4 = Counter(n4gram)
dictionary3 = Counter(n3gram)

# dump both 3gram and 4 gram dictionaries in files
with open("dictionary4.txt", 'w') as dictFile:
    json.dump(dictionary4, dictFile)

with open("dictionary3.txt", 'w') as dictFile:
    json.dump(dictionary3, dictFile)

