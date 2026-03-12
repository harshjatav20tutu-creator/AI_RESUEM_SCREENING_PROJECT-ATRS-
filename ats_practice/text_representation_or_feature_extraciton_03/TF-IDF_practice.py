# TF-IDF ;- in tf-idf every word has a frequency (importance of word in the document) , it is calculated by two factor
# 1. how many times it appear in the document . 1. how rare it is in other documents. 
# for example if the word appearance in the document is very high and it is rare in other document that the 
# frequency of the word is high.
# TF = term frequency , IDF - inverse document frequency 


import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.DataFrame({"Text":["people watch campusx","campusx watch campusx","people write comment","campusx write comment"],"Output":[1,1,0,0]})



tfidf = TfidfVectorizer()
arr = tfidf.fit_transform(df['Text']).toarray()

print(arr)
print(tfidf.get_feature_names_out())
