import gensim
import pandas as pd
import numpy as np
import os.path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sentence_transformers import SentenceTransformer
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def counter_argument(input, dataframe):
    # TODO, make bot smarter...

    # Use by google pretrained BERT-model to get similarity scores from all arguments...
    claim_embeddings = np.array(dataframe['bert_encoding'].to_list())
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    # Create new column with similarity-to-input-score for each argument.
    input_embedding = sbert_model.encode(input)
    bert_sim = cosine_similarity(claim_embeddings, np.transpose(input_embedding.reshape(-1, 1)))
    dataframe['input_bert_similarity'] = np.concatenate(bert_sim).tolist()

    #Find index of argument most similar to input...
    maxid = dataframe['input_bert_similarity'].idxmax()


    claim_sentiment = np.array(dataframe['sentiment'].to_list())
    input_sentiment = []
    input_blob = TextBlob(input, analyzer=NaiveBayesAnalyzer())
    input_sentiment.append(input_blob.sentiment[1])
    input_sentiment.append(input_blob.sentiment[2])

    sentiment_sim = euclidean_distances(claim_sentiment, np.transpose(np.array(input_sentiment).reshape(-1, 1)))
    dataframe['input_sentiment_distance'] = np.concatenate(sentiment_sim).tolist()
    print(dataframe.iloc[maxid])

    # Return its argument...
    if dataframe.iloc[maxid]['con_arguments'] == "":
        return "I agree! " + dataframe.iloc[maxid]['pro_arguments'] + " \n Identified parent claim: " + dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['input_bert_similarity'])
    else:
        return dataframe.iloc[maxid]['con_arguments'] + " \n Identified parent claim: " + dataframe.iloc[maxid]['claim'] + " [Similarity score] " + str(dataframe.iloc[maxid]['input_bert_similarity'])
