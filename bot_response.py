import gensim
import pandas as pd
import numpy as np
import os.path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def counter_argument(model, user_input, arguments_list):
    # TODO, make bot smarter...

    # Use by google pretrained BERT-model to get similarity scores from all arguments...
    # Try load pickle with already encoded arguments...
    if os.path.isfile('embeddings_df.pkl'):
        sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
        documents_df = pd.read_pickle('embeddings_df.pkl')
        document_embeddings = np.array(documents_df['embeddings'].to_list())

    # If not, encode and pickle
    else:
        documents_df = pd.DataFrame(arguments_list, columns=['arguments'])
        sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
        document_embeddings = sbert_model.encode(documents_df['arguments'])
        print(document_embeddings)
        print(type(document_embeddings))
        document_embeddings_list = document_embeddings.tolist()
        documents_df['embeddings'] = document_embeddings_list
        documents_df.to_pickle('embeddings_df.pkl')

    # Create new column with similarity-to-input-score for each argument.
    input_enbedding = sbert_model.encode(user_input)
    sim = cosine_similarity(document_embeddings, np.transpose(input_enbedding.reshape(-1, 1)))
    documents_df['input_similarity'] = np.concatenate(sim).tolist()

    #Find index of argument most similar to input...
    maxid = documents_df['input_similarity'].idxmax()

    #Return its argument...
    return documents_df.iloc[maxid]['arguments']
