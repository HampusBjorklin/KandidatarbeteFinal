import re
def argument_list(text_file):
    # Imported text-file sometimes splits long arguments to multiple lines...
    arguments_list = text_file.splitlines()
    for i, line in enumerate(arguments_list):
        arguments_list[i] = re.sub('http://\S+|https://\S+', '.', line)
        arguments_list[i] = re.sub("[^a-zA-Z '.,:;/]+", '', arguments_list[i])
        arguments_list[i] = re.sub(r'^.*?:', '', arguments_list[i])
        arguments_list[i] = re.sub(' +', ' ', arguments_list[i])

    return arguments_list

def clean_argument_list(text_file):
    # Imported text-file sometimes splits long arguments to multiple lines...
    arguments_list = text_file.splitlines()
    for i, line in enumerate(arguments_list):
        arguments_list[i] = re.sub('http://\S+|https://\S+', '.', line)
        arguments_list[i] = re.sub("[^a-zA-Z ':;/]+", '', arguments_list[i])
        arguments_list[i] = re.sub(r'^.*?:', '', arguments_list[i])
        arguments_list[i] = re.sub(' +', ' ', arguments_list[i])
        arguments_list[i] = arguments_list[i].lower()

    return arguments_list
