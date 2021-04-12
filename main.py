import os.path
from text_cleaning import argument_list, clean_argument_list
from create_model_test import create_model
from bot_response import counter_argument
# Import all arguments from trolley problem text-file...
f = open('trolley.txt', 'r', encoding='UTF-8')
arguments = f.read()
f.close()

# Create list of all arguments...
arguments_list = argument_list(arguments)
# Create clean list aswell...
clean_arguments_list = clean_argument_list(arguments)

# Check if model already been trained, otherwise train Doc2Vec model.
if os.path.isfile('Compare_d2v.model'):
    print("File exist")
else:
    create_model(clean_arguments_list)
    print('File created')


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
        print('BOT: '+ counter_argument())
