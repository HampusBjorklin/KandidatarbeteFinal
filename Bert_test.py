from sentence_transformers import SentenceTransformer
import re
import pandas as pd
import numpy as np
import os.path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

def argument_list(text_file):
    # Imported text-file sometimes splits long arguments to multiple lines...
    arguments_list = text_file.splitlines()
    for i, line in enumerate(arguments_list):
        arguments_list[i] = re.sub('http://\S+|https://\S+', '.', line)
        arguments_list[i] = re.sub("[^a-zA-Z '.,:;/]+", '', arguments_list[i])
        arguments_list[i] = re.sub(r'^.*?:', '', arguments_list[i])
        arguments_list[i] = re.sub(' +', ' ', arguments_list[i])

    return arguments_list

# Import all arguments from trolley problem text-file...
f = open('trolley.txt', 'r', encoding='UTF-8')
arguments = f.read()
f.close()

if os.path.isfile('embeddings_df.pkl'):
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    documents_df = pd.read_pickle('embeddings_df.pkl')
    document_embeddings = np.array(documents_df['embeddings'].to_list())

else:
    arguments_list = argument_list(arguments)
    documents_df=pd.DataFrame(arguments_list,columns=['arguments'])
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    document_embeddings = sbert_model.encode(documents_df['arguments'])
    print(document_embeddings)
    print(type(document_embeddings))
    document_embeddings_list = document_embeddings.tolist()
    documents_df['embeddings'] = document_embeddings_list
    documents_df.to_pickle('embeddings_df.pkl')


test_input = 'Less pain is felt by a fast death'
test_embedding = (sbert_model.encode(test_input))
test_embedding2 = document_embeddings[:1]
sim = cosine_similarity(document_embeddings, np.transpose(test_embedding.reshape(-1,1)))
documents_df['input_similarity'] = np.concatenate(sim).tolist()
maxid = documents_df['input_similarity'].idxmax()
print(documents_df.iloc[maxid])
print(documents_df.iloc[maxid]['arguments'])

