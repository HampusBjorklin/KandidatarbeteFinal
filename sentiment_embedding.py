import nltk
import pandas as pd
from textblob import Blobber
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def sentiment_embedding(dataframe):
    claims = dataframe['claim']
    sentiments = []
    for i in claims:
        blob = TextBlob(i)
        sentiment = []
        sentiment.append(blob.sentiment[0])
        sentiment.append(blob.sentiment[1])
        sentiments.append(sentiment)
    dataframe['sentiment'] = sentiments


    return
