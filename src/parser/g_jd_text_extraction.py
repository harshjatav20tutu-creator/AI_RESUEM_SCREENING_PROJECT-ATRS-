import pdfplumber 
import os 
from typing import  List 
from docx import Document 


def extract_text_from_docu(docx_path:str)->str:
    # it can't handle multiple pages 
    doc = Document(docx_path)
    parts: List[str] = []

    for par in doc.paragraphs:
        t = par.text.strip()
        if t:
            parts.append(t)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                t = cell.text.strip()
                parts.append(t)

    return "\n".join(parts)

def ext_text_from_textfile(text_file_path:str)->str:
    with open(text_file_path,"r",encoding="utf-8", errors= 'ignore') as f:
        return f.read()
    
# below functions is for pdf 

def page_has_tables(page)->bool:
    tables = page.extract_tables()
    if not tables:
        return False
    return bool(tables)
    

def jd_table_extraction(page)->str:

    table_rawtext = []
    tables = page.extract_tables()
    for table in tables:
        for row in table:
            if not row:
                continue

            clean_cells = []
            for cell in row:
                if cell:
                    clean_cells.append(cell.strip())

            if clean_cells:
                table_rawtext.append(" ".join(clean_cells))

    return " ".join(table_rawtext)


def get_jd_text_pdf(pdf_path:str)->str:
    
    page_text = []
    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            if page_has_tables(page):
                text = jd_table_extraction(page)
            else:
                text = page.extract_text()

            if text :
                page_text.append(text)

    return " ".join(page_text)

# main function to extract text from different type of files 

def text_extraction_from_files(jd_input)->str:

    if os.path.isfile(jd_input):
        low = jd_input.lower()

        if low.endswith(".txt"):
            return ext_text_from_textfile(jd_input)
        
        if low.endswith(".docx"):
            return extract_text_from_docu(jd_input)
        
        if low.endswith(".pdf"):
            return get_jd_text_pdf(jd_input)
        
        raise ValueError(f"Unsupported JD file type {jd_input}:")
    
    return jd_input







