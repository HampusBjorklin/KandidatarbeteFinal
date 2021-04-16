import nltk

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

text = "The worth of a life is not objective, but determined by the specific norms of a culture or group of people."
blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())

print(blob.sentiment)
