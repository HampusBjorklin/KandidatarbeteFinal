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
from text_cleaning import informative_words_list
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
tb1 = Blobber(analyzer=NaiveBayesAnalyzer())

agree_list = ['I agree! ', 'That\'s a good point... ', 'Touché! ', 'Yes! ', 'You\'re right. ']

def counter_argument(user_input, dataframe, tb):
    simliarity_scores(user_input, dataframe, tb)
    #Find index of argument most similar to input...
    maxid = dataframe['total_similarity_score'].idxmax()
    ran = random.randint(0, 4)

    print(dataframe.iloc[maxid].to_string(), '\n')

    if dataframe.iloc[maxid]['pro_arguments'] == "" and dataframe.iloc[maxid]['con_arguments'] == "":
        return (agree_list[ran] + dataframe.iloc[maxid]['claim'], " \n Identified parent claim: (No pro/con arg) " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))

    # Return its argument...
    if dataframe.iloc[maxid]['input_bert_similarity'] <= 0.6:
        if dataframe.iloc[maxid]['pro_arguments'] == "":
            return (agree_list[ran] + dataframe.iloc[maxid]['con_arguments'], " \n Identified parent claim: " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))
        else:
            return (dataframe.iloc[maxid]['pro_arguments'], " \n Identified parent claim: " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))
    else:
        if dataframe.iloc[maxid]['con_arguments'] == "":
            return (agree_list[ran] + dataframe.iloc[maxid]['pro_arguments'], " \n Identified parent claim: " + dataframe.iloc[maxid][
                'claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['total_similarity_score']))
        else:
            return (dataframe.iloc[maxid]['con_arguments'],  " \n Identified parent claim: " + \
                   dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(
                dataframe.iloc[maxid]['total_similarity_score']))


def simliarity_scores(user_input, dataframe, tb):
    # TODO, make bot smarter...

    # Use by google pretrained BERT-model to get similarity scores from all arguments...
    claim_embeddings = np.array(dataframe['bert_encoding'].to_list())
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    # Create new column with similarity-to-input-score for each argument.
    input_embedding = sbert_model.encode(user_input)
    bert_sim = cosine_similarity(claim_embeddings, np.transpose(input_embedding.reshape(-1, 1)))
    dataframe['input_bert_similarity'] = np.concatenate(bert_sim).tolist()

    claim_sentiment = np.array(dataframe['sentiment'].to_list())
    input_sentiment = [tb(user_input).sentiment[1], tb(user_input).sentiment[2]]
    sentiment_sim = euclidean_distances(claim_sentiment, np.transpose(np.array(input_sentiment).reshape(-1, 1)))
    dataframe['input_sentiment_distance'] = np.concatenate(sentiment_sim).tolist()

    input_words = informative_words_list(user_input)
    claim_words = dataframe['word_tokens']
    word_similarities = []
    for words in claim_words:
        sim = 0
        for w in words:
            if w in input_words:
                sim += 1
        sim = sim / len(words)
        word_similarities.append(sim)
    dataframe['input_word_similarity'] = word_similarities
    dataframe['total_similarity_score'] = 4*dataframe['input_bert_similarity'] + 1.5*dataframe['input_word_similarity'] - \
                                          dataframe['input_sentiment_distance']

    return dataframe




