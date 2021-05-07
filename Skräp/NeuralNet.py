from text_cleaning import clean_string
import pandas as pd
df = pd.read_pickle('../Pickles/trolley.pkl')
print(df.head(15))
claims = df['claim']
print(claims)