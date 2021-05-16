import bot_response
import os
import pandas as pd

from counterargument_db import create_dataframe
from sentiment_embedding import sentiment_model
from main import check_folders


def write_nothing(text):
    pass



input_file = "rewritten_arguments.txt"
print_in_out = True
number_of_lines_to_check = 199
bot_response.print = write_nothing

f  = open('test_arg.txt', 'r')
inputs = f.read().splitlines()

outputs = []
wrongs = []

check_folders()
if os.path.isfile('Pickles/Trolley.pkl'):
    dataframe = pd.read_pickle('Pickles/trolley.pkl')
else:
    create_dataframe()
    dataframe = pd.read_pickle('Pickles/trolley.pkl')
tb = sentiment_model()

for i in range(min(number_of_lines_to_check, len(inputs))):
    outputs.append(bot_response.counter_argument_testing(inputs[i], dataframe, tb))
    if print_in_out:
        print(f'In: {inputs[i].rstrip()}')
        print(f'Out: {dataframe["claim"].iloc[outputs[i]]}\n')
    if i != outputs[i]:
        wrongs.append(i)

print(f"Wrong indexes: {wrongs}")
