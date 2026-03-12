# Bag of Words(BOF):- bag of word is nothing else bag of uni grams 

import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

df = pd.DataFrame({"Text":["people watch campusx","campusx watch campusx","people write comment","campusx write comment"],"Output":[1,1,0,0]})
cv = CountVectorizer()

bow = cv.fit_transform(df['Text'])
# print(cv.vocabulary_)

# print(bow[0].toarray())
# print(bow[1].toarray())

new = cv.transform(["campusx watch and write comment of campusx"]).toarray()
print(new)