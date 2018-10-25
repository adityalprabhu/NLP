import os
import glob
import re
import nltk
import operator
import json
from collections import Counter
import math
import numpy as np
import random
import datetime
import time
import sys
import ntpath

# path = './res/browncopy_2018/'
path = sys.argv[1]
test_file_path = sys.argv[2]

word_tags_pairs = []
tags = []
bigram = []
start_tag = '<start>'
all_words = []

dir_name = "./"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".txt"):
        os.remove(os.path.join(dir_name, item))

cleanedPath = './res/cleaned/browncopy_2018/'
os.makedirs(cleanedPath, mode=0o777, exist_ok=True)


# function to return the file name from the path


def path_leaf(x):
    head, tail = ntpath.split(x)
    return tail or ntpath.basename(head)

# getting all files in single file for words count
for filename in glob.glob(os.path.join(path, '*')):
    with open(filename, 'r', encoding='latin-1') as infile, open('allWords.txt', 'a+') as outfile:
        all_lines = infile.read()
        lines = all_lines.split('\n')
        for line in lines:
            if not line == '':
                tokens = line.split()
                for t in tokens:
                    if not t == ' ':
                        outfile.write(t + ' ')
    infile.close()

with open('allWords.txt') as infile:
    infile.seek(0)
    all_lines = infile.read()
    lines = all_lines.split('\n')
    for line in lines:
        words = line.split()
        for word in words:
            word_tag_tuple = nltk.str2tuple(word, '/')
            all_words.append(word_tag_tuple[0])

wordCountDictionary = Counter(all_words)

# replace all UNK in new separate files
for filename in glob.glob(os.path.join(path, '*')):
    with open(filename, 'r', encoding='latin-1') as infile, open((cleanedPath+path_leaf(filename)), 'w+') as outfile:
        all_lines = infile.read()
        lines = all_lines.split('\n')
        for line in lines:
            if not line == '':
                words = line.split()
                outfile.write('<start> ')
                for i, word in enumerate(words):
                    word_tag_tuple = nltk.str2tuple(word, '/')
                    if wordCountDictionary[word_tag_tuple[0]] <= 5:
                        words[i] = 'UNK/' + str(word_tag_tuple[1])

                for w in words:
                    outfile.write(w + ' ')

                outfile.write('<end>\n')

for filename in glob.glob(os.path.join(cleanedPath, '*')):
    with open(filename, 'r', encoding='latin-1') as infile:
        all_lines = infile.read()
        lines = all_lines.split('\n')
        for line in lines:
            words = line.split()
            for i, word in enumerate(words):
                if word == '<start>':
                    tags.append(word)
                    word_tag_next_tuple = nltk.str2tuple(words[i + 1], '/')
                    bigram.append((word, word_tag_next_tuple[1]))

                elif word == '<end>':
                    tags.append(word)

                else:
                    word_tag_tuple = nltk.str2tuple(word, '/')
                    word_tags_pairs.append(word_tag_tuple)
                    tags.append(word_tag_tuple[1])
                    if not words[i+1] == '<end>':
                        word_tag_next_tuple = nltk.str2tuple(words[i + 1], '/')
                        bigram.append((word_tag_tuple[1], word_tag_next_tuple[1]))
                    else:
                        bigram.append((word_tag_tuple[1], words[i+1]))

word_tag_count = Counter(word_tags_pairs)
tagUnigram = Counter(tags)
tagBigram = Counter(bigram)

##### 4.2 finding the transition probability #######

transition_probability = {}
smoothingV = len(tagUnigram)

for t in tagBigram:
    transition_probability[t] = (tagBigram[t] + 1) / (tagUnigram[t[0]] + smoothingV)


##### 4.3 finding the emission probability ######

emission_probability = {}

for wp in word_tag_count:
    emission_probability[wp] = (word_tag_count[wp] + 1) / (tagUnigram[wp[1]] + smoothingV)

#############to generate 5 random sentences##############

gen_bigrams = []


def random_tag_bigram_probability(gen_tags):
    psum = 0
    for index, tag in enumerate(gen_tags):
        if not index >= len(gen_tags)-1:
            psum = psum + math.log10(transition_probability[(tag, gen_tags[index+1])])
    return 10**psum


def random_word_tag_probability(gen_word_tags):
    psum = 0
    for wt in gen_word_tags:
        psum = psum + math.log10(emission_probability[wt])
    return 10**psum

def generate_sentences():
    previous_tag = start_tag
    next_tag = ''
    pair_tags = []
    generated_strings = []
    y = []
    generated_strings_tprobability = []
    generated_strings_eprobability = []
    generated_sentences = []

    for i in range(5):
        while not next_tag == '<end>':
            y = [k[1] for k, v in tagBigram.items() if k[0] == previous_tag]
            next_tag = random.choice(y)
            previous_tag = next_tag
            if not next_tag == '<end>':
                pair_tags.append(next_tag)
        previous_tag = '<start>'
        next_tag = ''
        generated_strings.append(pair_tags)
        generated_strings_tprobability.append((random_tag_bigram_probability(pair_tags)))
        pair_tags = []

    str1 = ""
    # random_word = ''
    random_word_tag = []

    for j, gs in enumerate(generated_strings):
        for i, t in enumerate(gs):
            y = [k[0] for k, v in word_tag_count.items() if k[1] == t]
            random_word = random.choice(y)
            if not random_word == 'UNK':
                random_word_tag.append((random_word, t))
                str1 = str1 + " " + random_word + "/" + str(t)
        generated_strings_eprobability.append(random_word_tag_probability(random_word_tag))
        generated_sentences.append(str1)
        str1 = ""
    random_word_tag = []


    random_sentences = []
    with open("random_sentences.txt", 'w') as outfile:
        for j, gs in enumerate(generated_sentences):
            random_sentences.append((gs, generated_strings_eprobability[j] * generated_strings_tprobability[j]))
            outfile.write(str(j+1) + " :-- " + random_sentences[j][0] + "       " +  str(random_sentences[j][1]) + "\n")

generate_sentences()

#######################################################################################################################
################### Viterbi algorithm ######################

tags = [k for k, v in tagUnigram.items()]
tags.remove('<start>')
tags.remove('<end>')

outer = []
inner = []
tags_outer = []

with open(test_file_path) as infile:
    words = infile.read().split('\n')
    for word in words:
        if '< sentence ID' in word:
            inner = []
        elif '<EOS>' in word:
            outer.append(inner)
        elif not word == '':
            inner.append(word)

N = len(tags)

def tp(x,y):
    if (x,y) in transition_probability:
        tp = transition_probability[(x,y)]

    else:
        tp = (1 / smoothingV)

    return tp


def ep(x, y):
    if (x, y) in emission_probability:
        ep = emission_probability[(x, y)]

    else:
        ep = (1 / smoothingV)

    return ep


def viterbi_func(sentence):
    T = len(sentence)
    # viterbi and backpointer matrices
    viterbi = np.zeros(shape=(N, T), dtype=np.float32)
    backpointer = np.zeros(shape=(N, T), dtype=np.float32)


    for s in range(0, N):
        viterbi[s, 0] = tp(start_tag, tags[s]) * ep(sentence[0], tags[s])
        backpointer[s, 0] = 0

    max_vab = 0
    max_s1 = 0

    for t in range(1, T):
        for s in range(0, N):
            for s1 in range(0, N):
                vab = viterbi[s1, t-1] * tp(tags[s1],tags[s]) * ep(sentence[t], tags[s])
                if vab >= max_vab:
                    max_vab = vab
                    max_s1 = s1
            viterbi[s,t] = max_vab
            backpointer[s,t] = max_s1
            max_vab = 0
            max_s1 = 0

    max_v = 0
    max_s = 0

    for s in range(0, N):
        v = viterbi[s, T-1]
        if v >= max_v:
            max_v = v
            max_s = s

    bestpathprob = max_v
    bestpathpointer = max_s

    # print(bestpathprob)
    # print(bestpathpointer)

    word_index = len(sentence)-1
    word_tags = [None] * len(sentence)
    while not word_index == -1:
        word_tags[word_index] = tags[bestpathpointer]
        bestpathpointer = int(backpointer[bestpathpointer][word_index])
        word_index = word_index - 1

    return word_tags


start_time = time.time()

for i,o in enumerate(outer):
    tags_outer.append(viterbi_func(o))


with open('file_with_tags.txt', 'w') as outfile:
    for i, o in enumerate(outer):
        outfile.write('< sentence ID =' + str(i+1) + '>\n')
        for j,w in enumerate(o):
            outfile.write(w + ", " + tags_outer[i][j] + '\n')
        outfile.write('<EOS>\n')


# write all counts in separate files
with open('word_tag_count.txt', 'w') as outfile:
    for k, v in word_tag_count.items():
        outfile.write(str(k) + " : " + str(v) + "\n")

with open('tag_unigram_count.txt', 'w') as outfile:
    for k, v in tagUnigram.items():
        outfile.write(str(k) + " : " + str(v) + "\n")

with open('tag_bigram_count.txt', 'w') as outfile:
    for k, v in tagBigram.items():
        outfile.write(str(k) + " : " + str(v) + "\n")

