import re

def clean_text(text):
    text = text.lower() # lowercasing the text 
    text = re.sub(r"[•▪▫★|—–]"," ",text)  # removing bullets 
    text = re.sub(r"\S+@\S+", " ", text)   # removing gmail 
    text = re.sub(r"\+?\d[\d\s\-]{8,}"," ",text)  # removing phone numbers 
    text = re.sub(r"http\S+|www\S+"," ", text)  # removing links 
    text = re.sub(r"[^a-z\s]"," ", text)  # removing everything expect alpabets and spaces 
    text = re.sub(r"\s+", " ", text) # removing extra spaces , newlines , tab spaces
    return text # stripping text 



