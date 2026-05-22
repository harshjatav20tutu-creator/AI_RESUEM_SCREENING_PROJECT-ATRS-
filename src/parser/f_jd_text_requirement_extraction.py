import pdfplumber 
import os 
import json
import re
import requests
from typing import  List 
from docx import Document 
from docx.text.paragraph import Paragraph
from docx.table import Table


class JDParser:

    def __init__(self, path_or_jdtext:str):
        self.path_or_jdtext = path_or_jdtext

    def jd_pdf_parser(self):
        try:
            pdf = pdfplumber.open(self.path_or_jdtext)
        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found at: {self.path_or_jdtext}")
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
        
        document_text = []
        
        try:
            for page in pdf.pages:
                tables = page.find_tables()
                
                # If no tables on page, extract entire page text
                if not tables:
                    page_text = page.extract_text()
                    if page_text:
                        text_content = page_text.strip()
                        if text_content:
                            document_text.append(text_content)
                
                # If tables exist, slice page horizontally
                else:
                    # Track vertical position as we move down the page
                    current_y_top = 0
                    
                    for table in tables:
                        table_bbox = table.bbox  # (x0, top, x1, bottom)
                        table_top = table_bbox[1]
                        table_bottom = table_bbox[3]
                        
                        # Slice 1: Text above the table
                        if current_y_top < table_top:
                            above_crop = (0, current_y_top, page.width, table_top)
                            above_text = page.crop(above_crop).extract_text()
                            if above_text:
                                text_content = above_text.strip()
                                if text_content:
                                    document_text.append(text_content)
                        
                        # Slice 2: The table content as Markdown
                        extracted_table = table.extract()
                        if extracted_table:
                            markdown_lines = []
                            for i, row in enumerate(extracted_table):
                                # Clean cell content
                                cells = [str(cell).strip() if cell else '' for cell in row]
                                row_markdown = "| " + " | ".join(cells) + " |"
                                markdown_lines.append(row_markdown)
                                
                                # Add header separator after first row
                                if i == 0:
                                    sep = "| " + " | ".join(["---"] * len(cells)) + " |"
                                    markdown_lines.append(sep)
                            
                            if markdown_lines:
                                document_text.append("\n".join(markdown_lines))
                        
                        # Update vertical position for next iteration
                        current_y_top = table_bottom
                    
                    # Slice 3: Text below the last table
                    if current_y_top < page.height:
                        below_crop = (0, current_y_top, page.width, page.height)
                        below_text = page.crop(below_crop).extract_text()
                        if below_text:
                            text_content = below_text.strip()
                            if text_content:
                                document_text.append(text_content)
            
            pdf.close()
            return "\n".join(document_text)
        
        except Exception as e:
            if 'pdf' in locals():
                pdf.close()
            raise Exception(f"Error processing PDF content: {str(e)}")
        
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
    
    def jd_text_extractor(self):
        # Clean the input
        cleaned_input = self.path_or_jdtext.strip()
        
        # Define validation thresholds
        min_chars = 400
        min_words = 50
        char_count = len(cleaned_input)
        word_count = len(cleaned_input.split())
        
        # Priority 1: Check for newlines (strong indicator of raw JD text)
        if '\n' in cleaned_input:
            # Treat as raw JD text and validate
            if char_count >= min_chars and word_count >= min_words:
                return cleaned_input
            else:
                raise ValueError(
                    f"Job description text is too short. Minimum required: {min_chars} characters and {min_words} words. "
                    f"Provided: {char_count} characters and {word_count} words."
                )
        
        # Priority 2: Check for sufficient length (fallback for single-line JD)
        if char_count >= min_chars and word_count >= min_words:
            return cleaned_input
        
        # Priority 3: Check if it's a file path
        is_file_path = (
            os.path.sep in cleaned_input or 
            cleaned_input.lower().endswith(('.pdf', '.docx'))
        )
        
        if is_file_path:
            # Extract file extension (case-insensitive)
            _, file_ext = os.path.splitext(cleaned_input)
            file_ext_lower = file_ext.lower()
            
            if file_ext_lower == '.pdf':
                return self.jd_pdf_parser()
            elif file_ext_lower == '.docx':
                return self.jd_docx_parser()
            else:
                raise ValueError(f"Unsupported file format: {file_ext}. Supported formats are .pdf and .docx")
        
        # Priority 4: Invalid input
        raise ValueError(
            f"Invalid input: Could not determine if input is raw JD text or a file path. "
            f"If raw text, minimum required: {min_chars} characters and {min_words} words. "
            f"If file path, only .pdf and .docx formats are supported. "
            f"Provided: {char_count} characters and {word_count} words."
        )


    def jd_requirements_extraction_engine(self, cleaned_jd_text: str) -> dict:

        """Extract job requirements from cleaned JD text using Ollama.
        
        Makes a POST request to a local Ollama instance running gemma2:2b
        to extract structured job description data.
        
        Args:
            cleaned_jd_text (str): The cleaned job description text.
            
        Returns:
            dict: Dictionary with keys: job_title, min_years_experience, work_mode,
                  location, mandatory_skills, preferred_skills, role_responsibilities.
        """
        # System prompt for the model
        system_prompt = """You are an advanced, deterministic information extraction engine specialized in HR and Applicant Tracking Systems. Your job is to analyze the provided Job Description text and extract specific attributes into a valid JSON object.

        ### Rules:
        1. Do not include any conversational text, pleasantries, or markdown formatting (like ```json) outside the JSON object. Return ONLY the raw JSON.
        2. If a field cannot be found in the text, use null (or 0 for integers).
        3. Do not assume or extrapolate information. Only extract what is explicitly stated.

        ### JSON Schema Structure:
        {
        "job_title": "Clean, official title of the role",
        "min_years_experience": Integer (Extract the minimum number of years required. If a range like '3-5 years' is given, extract 3. If not mentioned, return 0),
        "work_mode": "Must be exactly one of these: 'Remote', 'On-site', 'Hybrid', or 'Unspecified'",
        "location": "City, Country if stated, otherwise null",
        "mandatory_skills": ["Array of technical skills, languages, or tools explicitly required to qualify"],
        "preferred_skills": ["Array of nice-to-have frameworks, tools, or soft skills mentioned as a plus"],
        "role_responsibilities": "A concise paragraph summarizing the daily core duties of the hire."
        }"""
        
        full_prompt = f"{system_prompt}\n\n### Job Description:\n{cleaned_jd_text}"
        
        # Prepare the API payload
        payload = {
            "model": "gemma2:2b",
            "prompt": full_prompt,
            "format": "json",
            "stream": False
        }
        
        # Default schema for fallback
        default_response = {
            "job_title": None,
            "min_years_experience": 0,
            "work_mode": "Unspecified",
            "location": None,
            "mandatory_skills": [],
            "preferred_skills": [],
            "role_responsibilities": ""
        }
        
        try:
            # Make the API request
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=180
            )
            response.raise_for_status()
            
            # Extract the response text
            response_data = response.json()
            response_text = response_data.get("response", "")
            
            if not response_text:
                return default_response
            
            # Attempt 1: Direct JSON parsing
            try:
                extracted_data = json.loads(response_text)
                return extracted_data
            except json.JSONDecodeError:
                pass
            
            # Attempt 2: Regex fallback to extract JSON from markdown or text
            try:
                match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    extracted_data = json.loads(json_str)
                    return extracted_data
            except (json.JSONDecodeError, AttributeError):
                pass
            
            # Safety net: return default schema
            return default_response
            
        except requests.RequestException as e:
            print(f"API request error: {str(e)}")
            return default_response
        except Exception as e:
            print(f"Unexpected error in jd_requirements_extraction_engine: {str(e)}")
            return default_response
        
# output = JDParser(path_or_jdtext=None)
# requirements = output.jd_requirements_extraction_engine('''About the job
# Role Overview

# work authorization : US

# We are seeking a skilled AI Engineer to join our AI initiatives team in the IT Department. The role involves designing, developing, and deploying AI/ML solutions with a focus on Generative AI, Retrieval-Augmented Generation (RAG), and Agentic AI frameworks. The candidate will collaborate with cross-functional teams to build scalable and compliant AI solutions that enhance banking operations and customer experience.

# Key Responsibilities

# Design and implement AI/ML models leveraging LLMs, SLMs, RAG pipelines, and Agentic AI frameworks.
# Develop end-to-end AI workflows, including data ingestion, preprocessing, model training, fine-tuning, and deployment.
# Collaborate with data engineers to integrate structured and unstructured banking data securely.
# Implement and optimize vector databases, embeddings, and retrieval mechanisms.
# Ensure AI model governance, explainability, and compliance with banking regulations.
# Work with business and domain experts to translate requirements into AI-driven solutions.
# Monitor model performance, implement feedback loops, and continuously improve AI systems.
# Stay updated on emerging AI technologies and frameworks relevant to banking use cases.

# Required Skills & Qualifications

# Bachelor’s/Master’s degree in Computer Science, Data Science, AI/ML, or related fields.
# Strong programming skills in Python (TensorFlow, PyTorch, LangChain, Hugging Face, etc.).
# 2+ years Experience with Generative AI, LLMs/SLMs, RAG architectures, and vector databases (e.g., Pinecone, FAISS, Weaviate).
# Hands-on knowledge of Agentic AI frameworks (e.g., LangGraph, AutoGen, CrewAI, or similar).
# Familiarity with cloud platforms (AWS, Azure, GCP) and MLOps practices (Docker, Kubernetes, CI/CD).
# Understanding of data security, compliance, and governance frameworks in regulated industries (preferably banking/finance).
# Strong problem-solving skills, analytical mindset, and ability to work in Agile teams.

# Preferred Qualifications

# AI/ML certifications (e.g., AWS AI/ML Specialty, Microsoft AI Engineer, NVIDIA Deep Learning, Generative AI certifications).
# 2+ Experience with prompt engineering, fine-tuning, and RAG-enhanced GenAI models.
# Exposure to agent-based AI solutions in enterprise settings.
# Knowledge of banking/financial domain processes (risk, compliance, KYC, lending, fraud detection).

# if this that :
# 	db_interaction = DatabaseInteraction(normalized_attributes)
#         db_interaction.store_to_database()
# elif this that:
# 	retrieved_candidate_data_from_database = db_interaction.retrieve_candidates_for_matching() # here db_interaction showing "not defined db_interaction"
# tell me how to solve this problem do i have to completely separate candidate portal and HR dashboard backend code?''')

# print(requirements)