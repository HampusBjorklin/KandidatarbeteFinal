import gensim
import pandas as pd
import numpy as np
import os.path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sentence_transformers import SentenceTransformer
from text_cleaning import informative_words_list, word_triplet_list
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

agree_list = ['I agree! ', 'That\'s a good point... ', 'Touché! ', 'Yes! ', 'You\'re right. ', 'Correct, ']
disagree_list = ['Well yes, but ', '', 'Yes, however, ' '','', '', 'Ok Ok! but ']
unsure_list = ["I'm sorry but i don't understand that", 'Please rephrase that', "I'm unsure what you mean by that"]

def counter_argument(user_input, dataframe):
    if len(user_input)<3:
        return 'Im sorry but i dont really understand', 'No argument given'

    simliarity_scores(user_input, dataframe)
    #Find index of argument most similar to input...
    maxid = dataframe['total_similarity_score'].idxmax()
    ran = random.randint(0, 5)
    ran2 = random.randint(0,2)

    print(dataframe.iloc[maxid], '\n')

    if dataframe.iloc[maxid]['total_similarity_score'] < 2.7:
        return (unsure_list[ran2], " \n Identified parent claim: (unsure) " + \
        dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))


    if dataframe.iloc[maxid]['pro_arguments'] == "" and dataframe.iloc[maxid]['con_arguments'] == "":
        return (agree_list[ran] + dataframe.iloc[maxid]['claim'].lower(), " \n Identified parent claim: (No pro/con arg) " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))

    # Return its argument...
    if dataframe.iloc[maxid]['input_bert_similarity'] <= 0.6:
        if dataframe.iloc[maxid]['pro_arguments'] == "":
            return (agree_list[ran] + dataframe.iloc[maxid]['con_arguments'].lower(), " \n Identified parent claim: " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))
        else:
            return (disagree_list[ran] + dataframe.iloc[maxid]['pro_arguments'].lower(), " \n Identified parent claim: " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))
    else:
        if dataframe.iloc[maxid]['con_arguments'] == "":
            return (agree_list[ran] + dataframe.iloc[maxid]['pro_arguments'].lower(), " \n Identified parent claim: " + dataframe.iloc[maxid][
                'claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))
        else:
            return (disagree_list[ran] + dataframe.iloc[maxid]['con_arguments'].lower(),  " \n Identified parent claim: " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(
                dataframe.iloc[maxid]['total_similarity_score']))


def counter_argument_testing(user_input, dataframe) -> int:
    simliarity_scores(user_input, dataframe)
    # Find index of argument most similar to input...
    maxid = dataframe['total_similarity_score'].idxmax()
    return maxid


def simliarity_scores(user_input, dataframe):
    # TODO, make bot smarter...

    # Use by google pretrained BERT-model to get similarity scores from all arguments...
    claim_embeddings = np.array(dataframe['bert_encoding'].to_list())
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    # Create new column with similarity-to-input-score for each argument.
    input_embedding = sbert_model.encode(user_input)
    bert_sim = cosine_similarity(claim_embeddings, np.transpose(input_embedding.reshape(-1, 1)))
    dataframe['input_bert_similarity'] = np.concatenate(bert_sim).tolist()

    claim_sentiment = np.array(dataframe['sentiment'].to_list())
    input_sentiment = [TextBlob(user_input).sentiment[0], TextBlob(user_input).sentiment[1]]
    sentiment_sim = euclidean_distances(claim_sentiment, np.transpose(np.array(input_sentiment).reshape(-1, 1)))
    dataframe['input_sentiment_distance'] = np.concatenate(sentiment_sim).tolist()

    tokens = informative_words_list(user_input)
    input_words = tokens[0]
    claim_words = dataframe['word_tokens']
    claim_synonyms = dataframe['synonym_tokens']
    word_similarities = []
    for n, words in enumerate(claim_synonyms):
        sim = 0
        for w in words:
            if w in input_words:
                sim += 1
        sim = sim / len(claim_words[n])
        word_similarities.append(sim)

    triplet_similarities = []
    triplets = word_triplet_list(user_input.lower())
    print(triplets)
    claim_triplets = dataframe['word_triplets']
    for c in claim_triplets:
        sim = 0
        for i in c:
            if i in triplets:
                sim += 1
        sim = sim/len(c)
        triplet_similarities.append(sim)

    dataframe['input_triplet_similarity'] = triplet_similarities
    dataframe['input_word_similarity'] = word_similarities
    dataframe['total_similarity_score'] = 4*dataframe['input_bert_similarity'] + 2*dataframe['input_word_similarity'] -\
        - dataframe['input_sentiment_distance'] + 5*dataframe['input_triplet_similarity']

    return dataframe


def eval_counter_argument(user_input, dataframe):
    simliarity_scores(user_input, dataframe)
    #Find index of argument most similar to input...
    maxid = dataframe['total_similarity_score'].idxmax()
    return maxid





