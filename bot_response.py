import gensim
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
def counter_argument(model, user_input, arguments_list):
    # TODO, make bot smarter...

    # Probably needs more cleaning...
    input_words = word_tokenize(user_input)
    input_words = [word for word in input_words if not word in stopwords.words()]

    similar_sentences = model.dv.most_similar(positive=[model.infer_vector(input_words)], topn=3)
    print(similar_sentences)
    index = similar_sentences[0][0]
    claim = arguments_list[int(index)]
    return claim
