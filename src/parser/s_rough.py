
import re
from typing import Dict , List , Tuple


# def gate_extraction(jd_sections:Dict[str,List[str]])->Dict[str ,List[str]|str]:

#     requirement_map:Dict[str, List[str]] = {
#         "Bachelor of Technology in Computer Science": ["Bachelor of Technology in Computer Science","B.Tech CSE", "B.Tech in CS", "B.Tech CS", "B.Tech. (Computer Science)"],

#         "Bachelor of Science in Computer Science": ["Bachelor of Science in Computer Science","B.S. CS", "B.Sc. CS", "BSCS", "Bachelor of Computer Science"],

#         "Bachelor of Engineering in Computer Science": ["Bachelor of Engineering in Computer Science","B.E. CSE", "B.E. CS", "B.E. in Computer Science"],

#         "Bachelor of Computer Applications": ["Bachelor of Computer Applications","BCA", "B.C.A.", "Bachelor in Computer Applications"],

#         "Master of Technology in Computer Science": ["Master of Technology in Computer Science","M.Tech CSE", "M.Tech CS", "M.Tech in Computer Science"],

#         "Master of Science in Computer Science": ["Master of Science in Computer Science","M.S. CS", "M.Sc. CS", "MSCS", "Master of Computer Science"],

#         "Master of Computer Applications": ["Master of Computer Applications","MCA", "M.C.A.", "Master in Computer Applications"],

#         "Doctor of Philosophy in Computer Science": ["Doctor of Philosophy in Computer Science","Ph.D. CS", "PhD in Computer Science", "Ph.D. in CSE"],

#         "Bachelor's or Master's degree in Computer Science":[
#             "Bachelor’s/Master’s degree in Computer Science","Bachelor's/Master's degree in Computer Science","Bachelor's/Master's in computer science",
#             "Bachelor’s/Master’s in computer science"
#             ]

#     }


#     req_sections:List[str] = []
#     for section , text_tokens in jd_sections.items():

#         if section and section in ("requirements","essential_requirements","experience"):
#             req_sections.extend(text_tokens)

#         normalized_sections = " ".join(a.lower().strip() for a in req_sections)   

#     qualification_list = []
#     for canonial , alias in requirement_map.items():

#         degree_map = {}
#         all_alias = []
        
#         for a in alias:
#             norm = a.lower().strip()
#             degree_map[norm] = canonial
#             all_alias.append(norm)

#         patt = "|".join(re.escape(a) for a in all_alias if alias)

#         pattern = re.compile(rf"/(\b{patt}\b)",re.IGNORECASE)

#         for m in pattern.finditer(normalized_sections):
#             if m :
#                 degree = m.group(1).lower().strip()
#                 qualification_list.append(degree_map.get(degree))

#     experience_pattern = r"(?i)(\d+(?:\.\d+)?)\s*(\+?)\s*year[s]?"

#     match = re.search(experience_pattern, normalized_sections,re.IGNORECASE)

#     if match :
#         return {"minimum qualification":qualification_list,
#                 "experience":match}
#     return {"minimum qualification":qualification_list,
#                 "experience":"no experience"}



        
raw_text = '''About the job
Role Overview

We are seeking a skilled AI Engineer to join our AI initiatives team in the IT Department. The role involves designing, developing, and deploying AI/ML solutions with a focus on Generative AI, Retrieval-Augmented Generation (RAG), and Agentic AI frameworks. The candidate will collaborate with cross-functional teams to build scalable and compliant AI solutions that enhance banking operations and customer experience.

Key Responsibilities

Design and implement AI/ML models leveraging LLMs, SLMs, RAG pipelines, and Agentic AI frameworks c++ , C , C# .
Develop end-to-end AI workflows, including data ingestion, preprocessing, model training, fine-tuning, and deployment.
Collaborate with data engineers to integrate structured and unstructured banking data securely.
Implement and optimize vector databases, embeddings, and retrieval mechanisms.
Ensure AI model governance, explainability, and compliance with banking regulations.
Work with business and domain experts to translate requirements into AI-driven solutions.
Monitor model performance, implement feedback loops, python and continuously improve AI systems.
Stay updated on emerging AI technologies and frameworks relevant to banking use cases.

Required Skills & Qualifications

Bachelor’s/Master’s degree in Computer Science, Data Science, AI/ML, or related fields.
Strong programming skills in Python (TensorFlow, PyTorch, LangChain, Hugging Face, etc.).
with Generative AI, LLMs/SLMs, RAG architectures, and vector databases (e.g., Pinecone, FAISS, Weaviate). 
Hands-on knowledge of Agentic AI frameworks (e.g., LangGraph, AutoGen, CrewAI, or similar).
Familiarity with cloud platforms (AWS, Azure, GCP) and MLOps practices (Docker, Kubernetes, CI/CD).
Understanding of data security, compliance, and governance python frameworks in regulated industries (preferably banking/finance).
Strong problem-solving skills, analytical mindset, and ability to work in Agile teams.

Preferred Qualifications

AI/ML certifications (e.g., AWS AI/ML Specialty, Microsoft AI python3 Engineer, NVIDIA Deep Learning, Generative AI certifications).
 with prompt engineering, fine-tuning, and RAG-enhanced GenAI models.
Exposure to agent-based AI solutions in enterprise settings.
Knowledge of banking/financial domain processes (risk, compliance, KYC, lending, fraud detection).'''

# passed test cases 
# minimum experience : 3-5 years 
# minimum experience : 3-5 years experience
# experience : 3-5 years experience
# experience : 3-5 years
# experience : 5 years
# experience : 5+ years
# experience : 5+ months
# experience : 6-12 months
# experience : 12 months
# experience : 12 months experience
# experience : 5+ months experience
# experience : 6-12 months experience 
# 3+ years of experience 
# 3 years experience 
# 6 months experience 
# 6+ months experience 
# 3-5 years experience
# 3-5 months of experience

s = '''Implement and optimize vector databases, embeddings,  2022 - 2024 and retrieval mechanisms Ensure AI model governance, explainability, and compliance with banking regulations remote Work with business and domain experts to translate requirements into AI-driven solutions Monitor model performance, implement feedback loops, python and continuously improve AI systems Stay updated on emerging AI technologies and frameworks relevant to banking use cases.'''

t = s.split()
print(t)
    
















    








    





    
        






    







            
            
            



