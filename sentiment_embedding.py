import nltk
import pandas as pd
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
tb = Blobber(analyzer=NaiveBayesAnalyzer())

def sentiment_model():
    return Blobber(analyzer=NaiveBayesAnalyzer())


def sentiment_embedding(dataframe):
    claims = dataframe['claim']
    sentiments = []
    for i in claims:
        blob = tb(i)
        sentiment = []
        sentiment.append(blob.sentiment[1])
        sentiment.append(blob.sentiment[2])
        sentiments.append(sentiment)
    dataframe['sentiment'] = sentiments

    return

