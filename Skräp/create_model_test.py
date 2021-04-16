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
import ssl
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from text_cleaning import clean_argument_list

def create_model(arguments_list):

    print('Removing stopwords etc...')
    clean_arguments_list = clean_argument_list(arguments_list)
    print('Finished')
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