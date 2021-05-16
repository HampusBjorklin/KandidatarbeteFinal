import re
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
sno = nltk.stem.SnowballStemmer('english')


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
    clean_string = re.sub("[^a-zA-Z0-9 '%.,:;/]+", '', clean_string)
    clean_string = re.sub(' +', ' ', clean_string)
    return clean_string


def cleaner_string(txt):
    clean_string = txt
    clean_string = re.sub('http://\S+|https://\S+', '', clean_string)
    clean_string = re.sub("[^a-zA-Z0-9 '%]+", '', clean_string)
    clean_string = re.sub(' +', ' ', clean_string)
    return clean_string


def synonym_words_list(word_list):
    synonyms = []



def informative_words_list(txt):
    text = clean_string(txt)
    text = re.sub("[.,:;']",'',text)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words_list = []
    stemmed_words_list = []
    synonym_words_list = []

    for w in words:
        if w not in stop_words and w not in words_list:
            words_list.append(w)

    for w in words_list:
        synonym_words_list.append(w)
        for syn in wordnet.synsets(w):
            for word in syn.lemma_names():
                w_stem = sno.stem(word)
                if w_stem not in synonym_words_list and '_' not in word:
                    synonym_words_list.append(w_stem)

    for w in words_list:
        w_stem = sno.stem(w)
        stemmed_words_list.append(w_stem)

    return words_list, synonym_words_list


def word_triplet_list(txt):
    text = txt.lower()
    lst = text.split(' ')
    triplets = []
    for n in range(len(lst)-2):
        trip = []
        trip += lst[n:n+3]
        triplets.append(trip)

    return triplets
