import os.path
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

if os.path.isfile('../embeddings_df.pkl'):
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    documents_df = pd.read_pickle('../embeddings_df.pkl')
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