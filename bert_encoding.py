from sentence_transformers import SentenceTransformer
import pandas as pd


def bert_encoding(dataframe):
    claims = dataframe['claim'].to_list()
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    bert_embeddings = sbert_model.encode(claims).tolist()
    dataframe['bert_encoding'] = bert_embeddings
