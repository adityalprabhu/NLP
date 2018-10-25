import os
import glob
import re
import nltk
import operator
import json
from collections import Counter
import math
import lm31
import sys
import ntpath

new_cleaned_path = './res/cleaned/'

imdb_path = sys.argv[2]
news_path = sys.argv[3]

all_perplexities = []
avg_perplexities = []
# ##### loads dictionaries created from program lm31 #####

with open("dictionary4.txt") as dictFile:
    dictionary4 = json.load(dictFile)

with open("dictionary3.txt") as dictFile:
    dictionary3 = json.load(dictFile)


def path_leaf1(x):
    head, tail = ntpath.split(x)
    return tail or ntpath.basename(head)

# ################################# perplexity calculation  ####################################

#getting a count of all the words in the dataset
with open('allWords.txt') as infile:
    infile.seek(0)
    lines = infile.read()
    words = lines.split()
    # words = nltk.word_tokenize(lines)

    wordCountDictionary = Counter(words)
    V = len([k for k,v in wordCountDictionary.items() if int(v) > 5]) + 1

def find_average_perplexity(file_path, dataset_name):
    os.makedirs(new_cleaned_path + dataset_name + "/", mode=0o777, exist_ok=True)

    # replace all UNK in new separate files
    for filename in glob.glob(os.path.join(file_path, '*')):
        with open(filename, 'r', encoding='latin-1') as infile, open(
                (new_cleaned_path + dataset_name + "/" + path_leaf1(filename)), 'w') as outfile:
            lines = infile.read()
            words = lines.split()
            # words = nltk.word_tokenize(lines)

            for i, w in enumerate(words):
                if wordCountDictionary[w] <= 5:
                    words[i] = 'UNK'
                outfile.write(words[i] + ' ')

    for filename in glob.glob(os.path.join(new_cleaned_path + dataset_name + "/", '*')):
        with open(filename, 'r', encoding='latin-1') as infile, open('processing.txt', 'w') as outfile:
            for line in infile:
                if not line.strip():
                    continue
                outfile.write(re.sub(' +', ' ', line.replace('\n', ' ')))

        test4grams = []
        test3grams = []

        # creates 4grams and 3grams for test file
        with open('processing.txt') as infile:
            lines = infile.read()
            words = lines.split()
            # words = nltk.word_tokenize(lines)

        for x, token in enumerate(words):
            if not x < 3:
                test4grams.append(words[x-3] + ' ' + words[x-2] + ' ' + words[x-1] + ' ' + words[x])

        for x, token in enumerate(words):
            if not x < 2:
                test3grams.append(words[x-3] + ' ' + words[x-2] + ' ' + words[x-1])

        k = 0.1
        probability = 0
        perplexity = 0
        N = len(words)

        # find the perplexity for each file
        for i, x in enumerate(test4grams):
            if test4grams[i] in dictionary4:
                test4grams_count = dictionary4[test4grams[i]]
            else:
                test4grams_count = 0

            if test3grams[i] in dictionary3:
                test3grams_count = dictionary3[test3grams[i]]
            else:
                test3grams_count = 0

            probability = probability + math.log2((test4grams_count + k) / (test3grams_count + (k*V)))
        perplexity = 2**((-1/N)*probability)

        all_perplexities.append(perplexity)

    total_pp = 0
    for pp in all_perplexities:
        total_pp = total_pp + pp

    average_pp = total_pp / len(all_perplexities)
    print("Dataset Name:", dataset_name,"Average Perplexity:", average_pp)
    avg_perplexities.append("Dataset Name: " + dataset_name + "     Average Perplexity: " +  str(average_pp))

find_average_perplexity(imdb_path, "imdb_data")
all_perplexities = []
find_average_perplexity(news_path, "news_data")

with open('perplexities.txt', 'w') as outfile:
    for ap in avg_perplexities:
        outfile.write(ap + '\n')
outfile.close()


