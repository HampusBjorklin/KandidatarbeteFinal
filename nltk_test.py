import random
import re
import string

from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def get_pros_cons():
    input_file = 'trolley_all.txt'

    with open(input_file, 'r', encoding='UTF-8') as file:
        lines = []
        for line in file:
            lines.append(line)

        # list containing each parsed comment
        pros = []
        cons = []

        # we remove the first two lines of the text
        # as we don't need the header
        for line in range(0, 3):
            lines.pop(0)

        for i, line in enumerate(lines):
            if line[0].isnumeric() is not True:
                lines[i - 1] += ", " + line
                lines.pop(i)

        ##                                            ##
        ##                 REGEDITS                   ##
        ##                                            ##
        # iterate every row in the text file
        for line in [line for line in lines if line != "\n"]:

            # find the tree position the comment is in
            tree = re.search(r"^(\d{1,}.)+", line)

            # find if the comment is Pro or Con
            stance = re.search(r"(Con|Pro)(?::)", line).group(0)

            # find the text of the comment
            content = re.search(r"((Con|Pro)(?::\s))(.*)", line).group(0)

            # define the hierarchy of the current comment
            # which is based on the tree structure
            parsed = re.findall(r"(\d{1,}(?=\.))+", tree.group())
            level = len(parsed) - 1

            if stance == "Pro:":
                pros.append(content)
            elif stance == "Con:":
                cons.append(content)
            else:
                print(f"Unrecognised stance '{stance}'\nContents: {line}")

        return pros, cons


def get_tokenized_pros_cons(pros, cons):
    tokenized_pros = [line.split() for line in pros]
    tokenized_cons = [line.split() for line in cons]
    return tokenized_pros, tokenized_cons


if __name__ == "__main__":

    positive_tweets, negative_tweets = get_pros_cons()
    positive_tweet_tokens, negative_tweet_tokens = get_tokenized_pros_cons(positive_tweets, negative_tweets)

    # positive_tweets = twitter_samples.strings('positive_tweets.json')
    # negative_tweets = twitter_samples.strings('negative_tweets.json')
    # text = twitter_samples.strings('tweets.20150430-223406.json')
    # tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    # positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    # negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.seed(15)
    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))
    print(classifier.show_most_informative_features(10))

    custom_tweet = "Pulling the lever saves lives, so it is the moral thing to do"
    custom_tokens = remove_noise(word_tokenize(custom_tweet))

    print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))
