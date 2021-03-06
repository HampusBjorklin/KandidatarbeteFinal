import os.path
import os
import gensim
import pandas as pd
from text_cleaning import argument_list
from Skräp.create_model_test import create_model
from counterargument_db import create_dataframe
from bert_encoding import bert_encoding
from bot_response import counter_argument
from text_cleaning import informative_words_list


def check_folders():
    """
    Checks if necessary folders exists, creates them if they don't
    :return: None
    """

    paths = ['TextFiles', 'TextFiles/text_files', 'TextFiles/prepared_text_files', 'jsonFiles',
             'jsonFiles/original_json_files', 'jsonFiles/prepared_json_files', 'Pickles']
    for p in paths:
        if not os.path.exists(p):
            os.makedirs(p)


def main():
    check_folders()
    # Check if database with claims and counterarguments and bert embeddings already been created, otherwise create.
    if os.path.isfile('Pickles/Trolley.pkl'):
        dataframe = pd.read_pickle('Pickles/trolley.pkl')
    else:
        create_dataframe()
        dataframe = pd.read_pickle('Pickles/trolley.pkl')

    # Start bot conversation...
    print('BOT: As a bot I am a terrible debater and always agree')

    exit_words = ['bye', 'fuckoff', 'quit', 'exit', 'cya', 'goodbye']

    while True:
        user_input = input()
        user_input = user_input.lower()
        if user_input in exit_words:
            print('BOT: Good talk')
            break
        else:
            response = counter_argument(user_input, dataframe)
            print('BOT: ' + response[1] + '\n' + response[0])


if __name__ == '__main__':
    main()

# TODO fix pickles.... info words list can be in first pickle etc.
