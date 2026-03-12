
import re
from typing import Dict , List , Tuple , Any
from h_jd_section_extraction import jd_sections_ext


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
def clean_token(token):
    return token.strip(',./|()')

section = jd_sections_ext(raw_text)

def extraction_degree_qualification_for_gate(jd_sec:Dict[str,List[str]])->Dict[str,Any]:

    degree_levels = {
    "bachelor": ["bachelor", "bachelor’s","bachelors", "b.s", "bs", "b.a", "ba", "b.tech", "btech", "b.e", "be", "b.sc", "bsc", "undergrad"],
    "master": ["master", "masters", "master’s","m.s", "ms", "m.a", "ma", "m.tech", "mtech", "m.e", "me", "m.sc", "msc", "mba", "grad"],
    "doctorate": ["phd", "ph.d", "doctorate", "doctoral", "d.phil"],
    "diploma": ["diploma", "associate", "a.s", "a.a", "certification", "cert"]
    }

    degree_fields = {
    "computer_science": ["computer science", "cs", "compsci", "computer engineering", "software engineering"],
    "artificial_intelligence": ["artificial intelligence", "ai", "machine learning", "ml", "deep learning", "nlp", "natural language processing"],
    "data_science": ["data science", "ds", "data analytics", "data engineering", "big data"],
    "information_technology": ["information technology", "it", "information systems", "mis"]
    }


    to_canon_d_level = {}
    all_degree_level = set()

    for canon , alias in degree_levels.items():
        if alias:
            for a in alias:
                a_norm = a.lower().strip()
                all_degree_level.add(a_norm)
                to_canon_d_level[a_norm] = canon.lower().strip()
    
    norm_all_degree_level = set(sorted(list(all_degree_level), key=len, reverse=True))
    big_degree_level_patt = "|".join(re.escape(d) for d in norm_all_degree_level if d)
    degree_level_pattern = re.compile(rf"\b({big_degree_level_patt})\b",re.IGNORECASE)


    to_canon_d_fields = {}
    all_degree_fields = set()

    for canon , alias in degree_fields.items():
        if alias:
            for a in alias:
                a_norm = a.lower().strip()
                all_degree_fields.add(a_norm)
                to_canon_d_fields[a_norm] = canon.lower().strip()

    norm_all_degree_fields = set(sorted(list(all_degree_fields), key=len, reverse=True))
    big_degree_fields_patt = "|".join(re.escape(d) for d in norm_all_degree_fields if d)
    degree_fields_pattern = re.compile(rf"\b({big_degree_fields_patt})\b",re.IGNORECASE)

    degree_required = False
    degree_level_ext = set()
    degree_fields_ext = set()

    if jd_sec.get("essential_requirements"):
        jd_sections = []
        for i in jd_sec.get("essential_requirements"):
            jd_sections.append(clean_token(i.lower().strip()))

        for i , word in enumerate(jd_sections):
            if word in all_degree_level:
                degree_level_ext.add(to_canon_d_level.get(word.lower().strip()))
                window_tokens = jd_sections[i:i+15]
                window_text = " ".join(window_tokens).lower().strip()
                for m in degree_fields_pattern.finditer(window_text):
                    nor_m = m.group(1).lower().strip()
                    degree_fields_ext.add(to_canon_d_fields.get(nor_m))

    elif jd_sec.get("education"):

        jd_sections = []
        for i in jd_sec.get("education"):
            jd_sections.append(clean_token(i.lower().strip()))

        for i , word in enumerate(jd_sections):
            if word in all_degree_level:
                degree_level_ext.add(to_canon_d_level.get(word.lower().strip()))
                window_tokens = jd_sections[i:i+15]
                window_text = " ".join(window_tokens).lower().strip()
                for m in degree_fields_pattern.finditer(window_text):
                    nor_m = m.group(1).lower().strip()
                    degree_fields_ext.add(to_canon_d_fields.get(nor_m))

    elif jd_sec.get("requirements"):

        jd_sections = []
        for i in jd_sec.get("requirements"):
            jd_sections.append(clean_token(i.lower().strip()))

        for i , word in enumerate(jd_sections):
            if word in all_degree_level:
                degree_level_ext.add(to_canon_d_level.get(word.lower().strip()))
                window_tokens = jd_sections[i:i+15]
                window_text = " ".join(window_tokens).lower().strip()
                for m in degree_fields_pattern.finditer(window_text):
                    nor_m = m.group(1).lower().strip()
                    degree_fields_ext.add(to_canon_d_fields.get(nor_m))

    if degree_level_ext:
        degree_required = True

    return {"degree required":degree_required,
            "degree levels":list(degree_level_ext),
            "degree fields":list(degree_fields_ext)}

check = extraction_degree_qualification_for_gate(section)
print(check)















    








    





    
        






    







            
            
            



