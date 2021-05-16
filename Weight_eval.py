from bot_response import eval_counter_argument
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import pandas as pd
tb1 = Blobber(analyzer=NaiveBayesAnalyzer())
f  = open('test_arg.txt', 'r')
test_arg = f.read().splitlines()
dataframe = pd.read_pickle('Pickles/trolley.pkl')
sum = 0
inp = 'Many cops will make loads of choices regarding potential loss of life. If one has the policy of never chasing, it is not guaranteed that some lifes will be lost.'
print(eval_counter_argument(inp, dataframe, tb1))

'''
for n, i in enumerate(test_arg):
    if eval_counter_argument(i,dataframe, tb1) == n:
        print(n, 'Correct')
        sum += 1
        print(sum)

sum = sum/len(test_arg)
print(sum)
'''