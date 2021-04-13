from sentence_transformers import SentenceTransformer
import re
import pandas as pd
import numpy as np
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

def most_similar(doc_id,similarity_matrix,matrix):
    print (f'Document: {documents_df.iloc[doc_id]["arguments"]}')
    print ('\n')
    print ('Similar Documents:')
    if matrix=='Cosine Similarity':
        similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
    elif matrix=='Euclidean Distance':
        similar_ix=np.argsort(similarity_matrix[doc_id])
    for ix in similar_ix:
        if ix==doc_id:
            continue
        print('\n')
        print (f'Document: {documents_df.iloc[ix]["arguments"]}')
        print (f'{matrix} : {similarity_matrix[doc_id][ix]}')


# Import all arguments from trolley problem text-file...
f = open('trolley.txt', 'r', encoding='UTF-8')
arguments = f.read()
f.close()

# Create list of all arguments...
arguments_list = argument_list(arguments)

documents_df=pd.DataFrame(arguments_list,columns=['arguments'])
print(documents_df)

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

document_embeddings = sbert_model.encode(documents_df['arguments'])

pairwise_similarities = cosine_similarity(document_embeddings)
parwise_differences = euclidean_distances(document_embeddings)

most_similar(0, pairwise_similarities, 'Cosine Similarity')