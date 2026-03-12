
import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

df = pd.DataFrame({"Text":["people watch campusx","campusx watch campusx","people write comment","campusx write comment"],"Output":[1,1,0,0]})
cv = CountVectorizer(ngram_range=(1,2))  #(2,2)=bi gram  (1,2)= uni gram + bi gram

n_gram = cv.fit_transform(df['Text'])
print(cv.vocabulary_)