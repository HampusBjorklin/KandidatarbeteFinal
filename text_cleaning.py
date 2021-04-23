import re
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
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
        # arguments_list[i] = word_tokenize(arguments_list[i])
        # arguments_list[i] = [word for word in arguments_list[i] if not word in stopwords.words()]
        # arguments_list[i] = ' '.join(word[0] for word in arguments_list[i])
        if i%100 == 0:
            print(i)
    return arguments_list


def clean_string(txt):
    clean_string = txt
    clean_string = re.sub('http://\S+|https://\S+', '', clean_string)
    clean_string = re.sub(r'^.*?:', '', clean_string)
    clean_string = re.sub("[^a-zA-Z '.,:;/]+", '', clean_string)
    clean_string = re.sub(' +', ' ', clean_string)
    return clean_string

def informative_words_list(txt):
    text = clean_string(txt)
    text = re.sub('[.,:;]','',text)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words_list = []
    for w in words:
        if w not in stop_words:
            words_list.append(w)
    return words_list