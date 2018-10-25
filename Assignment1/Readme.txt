Readme

Answer 1: Present in the Question 1 folder

Answer 2: Present in the Question 2 folder

Answer 3:

Step 1: Go to folder lm31 
Command is:  cd lm31

Step 2: Run file lm32.py using command
python3 lm32.py <folder-path-to-gutenberg-dataset> <folder-path-to-imdb-dataset> <folder-path-to-news-dataset>

Example: 
python3 lm32.py /Users/aditya1/Desktop/NLP/Assignments/Assignment1/datasets/gutenberg /Users/aditya1/Desktop/NLP/Assignments/Assignment1/datasets/imdb_data /Users/aditya1/Desktop/NLP/Assignments/Assignment1/datasets/news_data
?Ps: Space between folder paths exist

You will find the 4gram count in the lm31 folder named ?dictionary4.txt??It is a Json file, you can format it and view it. 

Or look at reports folder, I have generated a file of 4gram counts.

Average perplexities with dataset name are printed on the console and in a file named "perplexities.txt". 
Running this program takes a while (~20-30 seconds)


Answer 4: 

Step 1: Go to folder hmm4
Command is:  cd hmm4

Step2: Run file hmm41.py using command
python3 hmm41.py <folder path to brown corpus dataset> <file path to science example data set>

Example:
python3 hmm41.py /Users/aditya1/Desktop/NLP/Assignments/Assignment1/datasets/browncopy_2018 /Users/aditya1/Desktop/NLP/Assignments/Assignment1/datasets/science_sample_copy.txt
?Ps: Space between folder paths exist

You will find reports in the hmm4 folder.
Word tag counts as ?word_tag_count.txt?
Tag unigram counts as ?tag_unigram_count.txt?
Tag bigram counts as ?tag_bigram_count.txt?

Random sentences generated file as ?random_sentences.txt?
All sentences with tags file as ?file_with_tags.txt?

All these files are already generated and given in the reports folder

Running this program takes a while (~20-30 min)
