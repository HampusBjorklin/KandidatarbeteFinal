import os.path
import gensim
import pandas as pd
from text_cleaning import argument_list
from Skräp.create_model_test import create_model
from counterargument_db import create_dataframe
from bert_encoding import bert_encoding
from bot_response import counter_argument

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
        print('BOT: '+ counter_argument(user_input, dataframe))