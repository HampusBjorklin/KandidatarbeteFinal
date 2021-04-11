# Import libraries...
import pandas as pd
import numpy as np
import nltk
import random
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Defining functions used later on...
# Create clean list of arguments
def argument_list(text_file):
    # Imported text-file sometimes splits long arguments to multiple lines...
    arguments_list = text_file.splitlines()

    for i, line in enumerate(arguments_list):
        if line[0].isnumeric() is False:
            arguments_list[i - 1] += ", " + line
            arguments_list.pop(i)

        arguments_list[i] = re.sub('http://\S+|https://\S+', '.', line)
        arguments_list[i] = re.sub("[^a-zA-Z '.,:;/]+", '', arguments_list[i])
        arguments_list[i] = re.sub(r'^.*?:', '', arguments_list[i])
        arguments_list[i] = re.sub(' +', ' ', arguments_list[i])

    return arguments_list

def clean_argument_list(text_file):
    # Clean up text...lowercase all, split into array of arguments
    text_file = text_file.lower()
    arguments_list = text_file.splitlines()

    # Imported text-file sometimes splits long arguments to multiple lines...
    for i, line in enumerate(arguments_list):
        if line[0].isnumeric() is False:
            arguments_list[i - 1] += ", " + line
            arguments_list.pop(i)
        # Remove excess characters, links, etc.
        arguments_list[i] = re.sub('http://\S+|https://\S+', '', line)
        arguments_list[i] = re.sub("[^a-zA-Z ]+", '', arguments_list[i])

    return arguments_list

def index_sort(list_input):
    length = len(list_input)
    list_index = list(range(0,length))

    x = list_input
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # Swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

def counter_argument(input_argument, clean_arguments_list, arguments_list):
    input_argument = input_argument.lower()
    clean_arguments_list.append(input_argument)
    argument_response = ''
    cm = CountVectorizer().fit_transform(clean_arguments_list)
    similarity_score_list = cosine_similarity(cm[-1],cm).flatten()
    index = index_sort(similarity_score_list)
    index = index[1:]
    responded = False

    j = 0
    for i in range(len(index)):
        if similarity_score_list[index[i]] > 0.0:
            argument_response = argument_response + ' ' + arguments_list[index[i]]
            responded = True
            j += 1
        if j > 1:
            break

    if not responded:
        argument_response = argument_response+' '+"Pardon but i don't understand"

    clean_arguments_list.remove(input_argument)
    return argument_response

# Import all arguments
f = open('trolley.txt', 'r')
arguments = f.read()
f.close()

arguments_list = argument_list(arguments)
clean_arguments_list = clean_argument_list(arguments)

# Start the chat...

print('BOT: As a bot I am a terrible debater and always agree')

exit_words = ['bye', 'fuckoff', 'quit', 'exit', 'cya', 'goodbye']


while(True):
    user_input = input()
    user_input = user_input.lower()
    if user_input in exit_words:
        print('BOT: Good talk')
        break
    else:
        print('BOT: '+counter_argument(user_input, clean_arguments_list, arguments_list))