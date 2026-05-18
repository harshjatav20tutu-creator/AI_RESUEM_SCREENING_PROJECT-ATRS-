import pdfplumber 
import os 
from typing import  List 
from docx import Document 
from docx.text.paragraph import Paragraph
from docx.table import Table


class JDParser:

    def __init__(self, path_or_jdtext:str):
        self.path_or_jdtext = self.path_or_jdtext

    def jd_pdf_parser(self):
        pass

    def jd_docx_parser(self):

        try:
            doc = Document(self.path_or_jdtext)
        except FileNotFoundError:
            raise FileNotFoundError(f"DOCX file not found at: {self.path_or_jdtext}")
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")

        document_text = []

        try:
            # Traverse body elements sequentially to maintain reading order
            for element in doc.element.body:
                # Check for paragraph element (CT_P)
                if element.tag.split('}')[-1] == 'p':
                    para = Paragraph(element, doc)
                    text = para.text.strip()
                    if text:  # Skip completely empty paragraphs
                        document_text.append(text)
                
                # Check for table element (CT_Tbl)
                elif element.tag.split('}')[-1] == 'tbl':
                    table = Table(element, doc)
                    # Build Markdown table
                    markdown_lines = []
                    for i, row in enumerate(table.rows):
                        # Extract cell text, preserving structure
                        cells = [cell.text.strip() for cell in row.cells]
                        row_markdown = "| " + " | ".join(cells) + " |"
                        markdown_lines.append(row_markdown)
                        
                        # Add header separator after first row
                        if i == 0:
                            sep = "| " + " | ".join(["---"] * len(cells)) + " |"
                            markdown_lines.append(sep)
                    
                    if markdown_lines:
                        document_text.append("\n".join(markdown_lines))
            
            # Join all sequential elements with newlines
            return "\n".join(document_text)

        except Exception as e:
            raise Exception(f"Error processing DOCX content: {str(e)}")
    






