import gensim
def counter_argument(model, user_input, arguments_list):
    # TODO, make bot smarter...

    # Probably needs more cleaning...
    input_sentence = user_input.lower().split(' ')

    similar_sentences = model.dv.most_similar(positive=[model.infer_vector(input_sentence)], topn=1)
    index = similar_sentences[0][0]
    claim = arguments_list[int(index)]
    return claim
