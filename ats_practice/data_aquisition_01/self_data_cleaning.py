import re 


def cleaning_data(text):
    text = text.lower()
    text = re.sub(r"[•▪▫★|—–]"," ",text)  
    text = re.sub(r"\S+@\S+", " ", text)   
    text = re.sub(r"\+?\d[\d\s\-]{8,}"," ",text)   
    text = re.sub(r"http\S+|www\S+"," ", text) 
    text = re.sub(r"[^a-z\s]"," ", text)  
    text = re.sub(r"\s+", " ", text) 

    return text




