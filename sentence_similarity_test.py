import gensim
from create_model_test import argument_list

model = gensim.models.Doc2Vec.load('Compare_d2v.model')

new_sentence = 'The worth of a life is subjective'.split(' ')
print(model.dv.most_similar(positive=[model.infer_vector(new_sentence)], topn=5))

# Import all arguments
f = open('trolley.txt', 'r', encoding='UTF-8')
arguments = f.read()
f.close()

arguments_list = argument_list(arguments)
print(arguments_list[225])