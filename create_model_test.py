'''
TODO: TEST MULTIPLE WAYS OF FINDING SIMILARITES IN SENTENCES....

WORD TOKENS
CHARACTER n-GRAMS
SEQUENCE SIMILARITY
SEMANTICS SIMILARITY
NAMED ENTITIES

Number of common words in both text, number of words in each argument
cosine similarity on TF-IDF vectors
Glove similarity
longest common subsequence...

SENTENCE VECTORS
'''

# Import libraries...
import pandas as pd
import numpy as np
import nltk

import nltk
import ssl
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import re
# Defining functions used later on...
# Create clean list of arguments
def argument_list(text_file):
    # Imported text-file sometimes splits long arguments to multiple lines...
    arguments_list = text_file.splitlines()
    for i, line in enumerate(arguments_list):
        arguments_list[i] = re.sub('http://\S+|https://\S+', '.', line)
        arguments_list[i] = re.sub("[^a-zA-Z '.,:;/]+", '', arguments_list[i])
        arguments_list[i] = re.sub(r'^.*?:', '', arguments_list[i])
        arguments_list[i] = re.sub(' +', ' ', arguments_list[i])

    return arguments_list

def clean_argument_list(text_file):
    # Imported text-file sometimes splits long arguments to multiple lines...
    arguments_list = text_file.splitlines()
    for i, line in enumerate(arguments_list):
        arguments_list[i] = re.sub('http://\S+|https://\S+', '.', line)
        arguments_list[i] = re.sub("[^a-zA-Z ':;/]+", '', arguments_list[i])
        arguments_list[i] = re.sub(r'^.*?:', '', arguments_list[i])
        arguments_list[i] = re.sub(' +', ' ', arguments_list[i])
        arguments_list[i] = arguments_list[i].lower()

    return arguments_list

if __name__ == '__main__':
    # Import all arguments
    f = open('trolley.txt', 'r')
    arguments = f.read()
    f.close()

    arguments_list = argument_list(arguments)
    clean_arguments_list = clean_argument_list(arguments)

    tagged_data = [TaggedDocument(words=word_tokenize(d), tags=[str(i)]) for i, d in enumerate(clean_arguments_list)]

    max_epochs = 100
    vec_size = 20
    alpha = 0.025

    model = Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm = 1)
    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
        model.alpha -= 0.0002

        model.min_alpha = model.alpha

    model.save("Compare_d2v.model")
    print('Model Saved :-)')