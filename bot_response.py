import gensim
import pandas as pd
import numpy as np
import os.path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def counter_argument(input, dataframe):
    # TODO, make bot smarter...

    # Use by google pretrained BERT-model to get similarity scores from all arguments...
    document_embeddings = np.array(dataframe['bert_encoding'].to_list())
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    # Create new column with similarity-to-input-score for each argument.
    input_enbedding = sbert_model.encode(input)
    sim = cosine_similarity(document_embeddings, np.transpose(input_enbedding.reshape(-1, 1)))
    dataframe['input_similarity'] = np.concatenate(sim).tolist()

    #Find index of argument most similar to input...
    maxid = dataframe['input_similarity'].idxmax()

    #Return its argument...
    return dataframe.iloc[maxid]['con_arguments'] + " [Similarity score]" + str(dataframe.iloc[maxid]['input_similarity'])
