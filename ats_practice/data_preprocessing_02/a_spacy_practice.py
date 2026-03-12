import spacy 
nlp = spacy.blank("en")

doc = nlp.add_pipe('sentencizer')
doc = nlp("Dr. strange loves pav bhaji of mumbai as it cost only $2 per palte. He also loves python")

for sentences in doc.sents:
    print(sentences)

