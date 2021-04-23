import os.path
import gensim
import pandas as pd
from text_cleaning import argument_list
from Skräp.create_model_test import create_model
from counterargument_db import create_dataframe
from bert_encoding import bert_encoding
from bot_response import counter_argument
from text_cleaning import informative_words_list


def main():
    # Check if database with claims and counterarguments and bert embeddings already been created, otherwise create.
    if os.path.isfile('embeddings_df.pkl'):
        dataframe = pd.read_pickle('embeddings_df.pkl')
    else:
        if os.path.isfile('Pickles/Trolley.pkl'):
            dataframe = pd.read_pickle('Pickles/trolley.pkl')
        else:
            create_dataframe()
            dataframe = pd.read_pickle('Pickles/trolley.pkl')

        bert_encoding(dataframe)
        embeddings = pd.read_pickle('embeddings_df.pkl')
    if os.path.isfile('embeddings_df2.pkl'):
        dataframe2 = pd.read_pickle('embeddings_df2.pkl')
    else:
        dataframe2 = pd.read_pickle('sentiment_dataframe.pkl')
        claims = dataframe2['claim']
        word_tokens = []
        for c in claims:
            tokens = informative_words_list(c)
            word_tokens.append(tokens)
        dataframe2['word_tokens'] = word_tokens
        pd.to_pickle(dataframe2, 'embeddings_df2.pkl')

    # Start bot conversation...
    print('BOT: As a bot I am a terrible debater and always agree')

    exit_words = ['bye', 'fuckoff', 'quit', 'exit', 'cya', 'goodbye']

    while(True):
        user_input = input()
        user_input = user_input.lower()
        if user_input in exit_words:
            print('BOT: Good talk')
            break
        else:
            print('BOT: '+ counter_argument(user_input, dataframe2))


if __name__ == '__main__':
    main()

# TODO fix pickles.... info words list can be in first pickle etc.