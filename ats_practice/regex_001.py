import pdfplumber 
import re 

def info_extraction(pdf_path):

    text = " (999)-456-678"
    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            text += page.extract_text()

    return text

def phone_number_extraction(text):
    pattern = ('\d{10}|\+\d{2}\s\d{10}|\(\d{3}\)\-\d{3}\-\d{3}')
    
    match = re.search(pattern, text)

    return match

def name_extraction(text):
    pattern = ('[A-Z][^a-z].* [A-Z][^a-z].*[^\n]+|[A-Z][^a-z].*[^\n]+')
    
    match = re.search(pattern, text )
    all = re.findall(pattern, text)

    return all




        

text = info_extraction('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_06.pdf')
phone = phone_number_extraction(text)
name = name_extraction(text)
print(name)





















