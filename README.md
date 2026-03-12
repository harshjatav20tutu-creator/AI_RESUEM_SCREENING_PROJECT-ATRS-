project Title : AI-Based Resume Screening & Job Matching System
This is now your final-semester flagship project.
________________________________________
🎯 PROJECT GOAL (KEEP THIS CLEAR)
Build an end-to-end ML system that:
•	Reads resumes (PDF)
•	Extracts skills & experience
•	Matches them with job descriptions
•	Ranks candidates
•	Explains why a candidate is suitable
•	Runs as a usable web app
If you can do this → you are placement-ready.
________________________________________
🧭 FULL ROADMAP (3–4 MONTHS)
I’m assuming ~6–8 hours/day 
________________________________________
🔹 PHASE 0 (Week 0) – Foundation Reset (3–4 days) 
What you do
•	Revise Python (strings, lists, dicts)
•	Learn:
o	Pandas
o	Regex (important for resumes)
•	Understand how resumes are structured
Output
•	Small script that reads PDF and prints text
Reality check
This phase removes fear. No ML yet.
________________________________________
🔹 PHASE 1 (Week 1–2) – Resume Parsing & Data Preparation
What you learn
•	PDF parsing (pdfplumber, PyMuPDF)
•	Text cleaning
•	Removing noise
•	Tokenization
What you build
•	Upload resume → extract raw text
•	Clean text → store structured data
Deliverable
Resume → Cleaned Text → Structured Fields
(Name, Skills, Experience, Education)
Why this matters
This is where 80% real-world ML happens.
________________________________________
🔹 PHASE 2 (Week 3–4) – Skill Extraction (CORE ML SKILL)
What you learn
•	Keyword matching
•	Skill dictionaries
•	TF-IDF basics
•	N-grams
What you build
•	Extract skills from resume
•	Normalize skills (e.g., “ML” → “Machine Learning”)
Deliverable
{
  "skills": ["Python", "Machine Learning", "SQL"]
}
Interview gold
You’ll explain:
“Why naive keyword matching fails and how I improved it.”
________________________________________
🔹 PHASE 3 (Week 5–6) – Job Description Processing
What you learn
•	Text similarity
•	Vectorization
•	Cosine similarity
What you build
•	JD → skill extraction
•	Resume ↔ JD similarity score
Deliverable
Resume Score: 78%
Reason: 6/8 required skills matched
🔥 This is REAL ML
Not deep learning — but useful ML.
________________________________________
🔹 PHASE 4 (Week 7–8) – Ranking & Matching System
What you learn
•	Ranking logic
•	Weighted scoring
•	Threshold tuning
What you build
•	Rank 100 resumes for 1 JD
•	Show top N candidates
Deliverable
Rank	Candidate	Match %
1	Resume_23	91%
2	Resume_11	88%
________________________________________
🔹 PHASE 5 (Week 9–10) – Model Upgrade (NLP POWER)
What you learn
•	Sentence embeddings (Sentence-BERT)
•	Semantic similarity
What you improve
•	Catch synonyms (“NLP” vs “Text Mining”)
•	Reduce false negatives
Why this matters
This is where your project becomes “AI”, not just rules.
________________________________________
🔹 PHASE 6 (Week 11–12) – Web App + API (CRITICAL)
What you learn
•	Streamlit OR FastAPI
•	File upload
•	UI basics
What you build
•	HR uploads JD
•	Upload multiple resumes
•	See ranked results
Deliverable
A working product, not a notebook.
________________________________________
🔹 PHASE 7 (Week 13) – Explainability & Logging
What you add
•	“Why this resume was selected”
•	Skill gap explanation
•	Logs for decisions
Interview killer line
“I focused on explainability to avoid black-box hiring.”
________________________________________
🔹 PHASE 8 (Week 14–15) – Testing, Optimization & Polish
What you do
•	Test edge cases
•	Improve speed
•	Clean UI
•	Write documentation
Final outputs
•	GitHub repo
•	Demo video
•	PPT for college
•	README like a company project


here is the progress and the code we wrote 

Phase 1  Resume Parsing & Data Preparation: completed.

code 1: the below code is extracting text from resumes it can handle both single and double columns resumes and give and output of chunk of the resume text.

```python
import pdfplumber 

def column_resume_text_ext(pdf_path):

    with pdfplumber.open(pdf_path) as pdf:

        # for all text in resume including multiple page in single resume 
        combined_text = [] 

        # basic celaning function to get chunk of words 
        def clean(t):
            return " ".join(t.replace("\n"," ").replace("\t"," ").split())
          
        # looping through all pages 
        for page in pdf.pages: 

            # extracting every word form a page 
            words = page.extract_words()

            # handeling words error if extract_words fails
            if words is None or len(words) == 0:
                return combined_text.append(clean(page.extract_text() or ""))   
                continue

            # getting position of every word in resume
            x_positions = sorted(w["x0"] for w in words) 

            # identifying columns resumes by finding middle white space and spliting page into half
            max_gap = 0  
            split_x = page.width/2

            # looping through each position of word to get maximum position jump, it helps in finding off centered columns
            for i in range(len(x_positions) -1):
                gap = x_positions[i+1] - x_positions[i] 
                if gap > max_gap:
                    max_gap = gap
                    split_x = x_positions[i] + gap/2   # getting the middle part of the gap 

            # handelling the resumes without columns, if the max_gap is less than 6% of the page width than resume doesn't have column  
            if max_gap < page.width * 0.06: 
                combined_text.append(clean(page.extract_text() or ""))
                continue

            # setting boundaries for columns 
            left_bbox = (0,0,split_x,page.height)
            right_bbox = (split_x,0,page.width,page.height)

            # ignoring every thing outside the boundaries and extracting text from each columns 
            left_text = page.crop(left_bbox).extract_text() or ""
            right_text = page.crop(right_bbox).extract_text() or ""

            # combining text of both boundaries 
            combined_text.append(clean(left_text) + " " + clean(right_text))

        # joining text of all pages 
        return " ".join(combined_text)
```


sample output of code 1:
AIDEN WILLIAMS CORE COMPETENCIES Cloud & System Architecture Distributed Systems Design, Microservices Architecture, Cloud-Native Infrastructure (AWS/Azure), Kubernetes & Docker, Infrastructure as Code (Terraform). Full-Stack Development Modern JavaScript.


code 2: cleaning and normalizing the extracted chunk of text 

```python
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
```
sample output of code 2:
aiden williams core competencies cloud system architecture distributed systems design microservices architecture cloud native.


code 3: below code is to sections extraction from resume text , it uses regex to detect the keywords for section keyword and extract text tokens from the section and stored it in the dectionary with its section name.

```python
import re 


SECTION_KEYWORDS = {
    "education": ["education", "academic background", "academics", "qualification"],
    "skills": ["skills", "technical skills", "core skills", "technologies","key achievements"],
    "experience": ["experience", "work experience", "employment", "internship"],
    "projects": ["projects", "personal projects", "academic projects"]
}

def extract_sections(text: str) -> dict:

    extracted_sections = {}
    text.lower()

    for section , keywords in SECTION_KEYWORDS.items():

        keyword_pattern = "|".join(keywords)

        stoping_keywords = []
        for other_section , other_keywords in SECTION_KEYWORDS.items():
            if other_section != section:
                other_keywords.extend(stoping_keywords)
        
        stoping_pattern = "|".join(stoping_keywords)

        pattern = rf"({keyword_pattern})\s*(.*?)(?=\n\s*(?:{stoping_pattern})\b|$)"

        match = re.search(pattern, text, re.DOTALL)

        if match:
            extracted_sections[section] = match.group(2).split()
        else:
            extracted_sections[section] = ""

    return extracted_sections
```
code 3 sample output:
{'education': ['master', 'of', 'science', 'in', 'austin', 'austin', 'texas'], 'skills': ['enhanced', 'system', 'performance', ]}


Phase 2 Skill Extraction from resumes : completed. 

code 1: skill database it just contain canonical skill and its aliases , the sample of database is given below.

```python
SKILL_DATABASE = {
    # Programming Languages
    "python": ["python", "python3"],
    "java": ["java"],
    "c": ["c"],
    "c++": ["c++", "cpp","c#"],
    "javascript": ["javascript", "js"],
    "node.js":["node.js", "node js", "node javascript"],
    "react.js":["react.js","react js","react javascript"],}
```

code 2: the below code is used to extract skill form the resume extracted section , it gives the list of skill 

```python
import re 
from src.parser.d_skills_db import SKILL_DATABASE


def get_skills_text(sections):
    skill_db = SKILL_DATABASE

    text_parts = []

    for key in ("skills","experience","projects"):
        if key in sections and sections[key]:
            text_parts.extend(sections[key])

    combined_text = " ".join(text_parts)

    found = set()

    for skill, skill_list in skill_db.items():
        combine_list = [re.escape(a.lower()) for a in skill_list]
        one_of = "|".join(combine_list)

        pattern = rf"\b(?:{one_of})\b"

        if re.search(pattern,combined_text):
            found.add(skill)

    return list(found)
```
code 2 sample output :
["python","java","java script"]


code 3: below code is used to weight skills based on section it appear and add some bonus for appearing in multiple sections. 

```python
import re
from typing import Dict , List , Union

TextBlock = Union[str ,List[str] ]

def _to_text(content:TextBlock)->str:

    if content is None:
        return ""
    if isinstance(content,list):
        return " ".join(str(x) for x in content if x is not None).lower()
    return str(content).lower()

def _get_pattern(skill: List[str])->re.Pattern:

    s = re.escape(skill.strip().lower())
    return re.compile(rf"\b{s}\b")

def weight_resume_skills(skills : list[str],
                         sections: Dict[str,TextBlock],
                         w_skills : float = 1.0,
                         w_exp_pro: float = 2.0,
                         w_other : float = 0.5,
                         w_multisection_bonus :float = 0.5)->Dict[str,float]:
    
    normalized_section : Dict[str,str] = {}
    for sec ,content in sections.items():
        normalized_section[sec] = _to_text(content)

    weight_skills: Dict[str,float] = {}

    for sk in skills:

        pat = _get_pattern(sk)
        score = 0.0

        matched_section = set()

        skills_text = normalized_section.get("skills","")
        if skills_text and pat.search(skills_text):
            score += w_skills
            matched_section.add("skills")

        project_text = normalized_section.get("projects","")
        if project_text and pat.search(project_text):
            score += w_exp_pro
            matched_section.add("projects")

        experience_text = normalized_section.get("experience","")
        if experience_text and pat.search(experience_text):
            score += w_exp_pro
            matched_section.add("experience")

        other_text_parts = []
        for sec , sec_text in normalized_section.items():
            if sec not in ("skills","experience","projects"):
                other_text_parts.append(sec_text)

        other_text = " ".join(other_text_parts)

        if other_text and pat.search(other_text):
            score += w_other
            matched_section.add("other")

        if len(matched_section)>= 2:
            score += w_multisection_bonus

        if score > 0.0:
            weight_skills[sk] = score

    return weight_skills
```
code 3 sample output :
{"pyhton":5.0, "java":3.5}

PHASE 3  Job Description Processing : more than half completed 

code 1: extracting text form job description it can handle documents like pdf, docx and we can paste job desctiption text in .txt file , it can handle tables in document or pdf .

```python
import pdfplumber 
import os 
from typing import  List 
from docx import Document 


def extract_text_from_docu(docx_path:str)->str:
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
```

code 1 sample output :
Key Responsibilities

Design and implement AI/ML models leveraging LLMs, SLMs, RAG pipelines, and Agentic AI frameworks.
Develop end-to-end AI workflows, including data ingestion, preprocessing, model training, fine-tuning, and deployment.


code 2: below code is used to extract sections from the job description , it detect the heading and extract the text of that heading and return an dictionary which contain heading as an key and list of heading text tokens as values. 

```python
import re
from typing import Dict , List 


def jd_sections_ext(text:str)->Dict[str,List[str]]:


    job_description_map = {

        "requirements": [
            "requirements", "qualifications", "what you ll need",
            "what you bring", "who you are", "skills & qualifications"
        ],

        "essential_requirements": [
            "required qualifications", "basic qualifications", "minimum qualifications",
            "minimum requirements", "must have", "must-haves", "mandatory","Required Skills & Qualifications"
        ],

        "optional_requirements": [
            "preferred qualifications", "preferred skills", "nice to have",
            "nice-to-have", "good to have", "desired skills", "bonus points for",
            "plus"
        ],

        "technical_stack": [
            "tech stack", "technical stack", "tools & technologies", "technologies",
            "technical skills", "technical requirements", "stack",
            "tools", "platforms", "frameworks", "languages", "databases",
            "cloud", "devops", "ci cd", "infrastructure"
        ],

        "experience": [
            "experience", "professional experience", "work experience",
            "relevant experience", "required experience"
        ],

    }

    t = text.replace("\r\n","\n").replace("\r","\n")

    alias_key_mapping :Dict[str , str] = {}
    all_alias: List[str] = []

    for key , alias in job_description_map.items():
        for a in alias:
            a_norm = a.strip().lower()
            alias_key_mapping[a_norm] = key 
            all_alias.append(a_norm)

    all_alias = sorted(set(all_alias),key=len, reverse=True)
    alias_pattern = "|".join(re.escape(a) for a in all_alias)

    heading_re = re.compile(rf"(?im)(?:^|\n)\s*(?:[-•*]\s*)?(?P<h>{alias_pattern})\s*[:\-]?\s*",flags=re.IGNORECASE)

    hits: List[tuple[int,int,str]] = []
    for m in heading_re.finditer(t):
        headings = m.group("h").strip().lower()
        hits.append((m.start(), m.end(), alias_key_mapping[headings]))

    out: Dict[str,List[str]]= {k:[] for k in job_description_map.keys()}

    for i , (start , end , key) in enumerate(hits):
        next_start = hits[i+1][0] if i+1 < len(hits) else len(t)
        chunk = t[end:next_start]

        if chunk :
            out[key] = chunk.split()
        else:
            out[key] = ""

    return out
```
code 2 sample output :
{'requirements': [], 'essential_requirements': ['Bachelor’s/Master’s', 'degree', 'in', 'Computer', 'Science,', 'Data', 'Science,', 'AI/ML,', 'or', 'related'].....}

code 3: below code is used to extract all skills from the job dectiprtion it returns a dictionary which contain all skills , and the skill category and an key for debug . 

```python
import re
from typing import Dict ,List , Tuple

def categorical_skill_db(skill_db: Dict[str, List[str]]) -> Dict[str, List[str]]:
    categories = {
        "programming": [],
        "cloud": [],
        "data & ml": [],
        "libraries and frameworks": [],
        "databases": [],
        "tools": [],
        "web and apis": [],
        "other": [],
    }

    for canonical, aliases in skill_db.items():
        key = canonical.lower().strip()

        if key in ("python", "java", "c", "c++", "javascript", "node.js", "react.js"):
            categories["programming"].extend(aliases)

        elif key in ("aws", "azure", "gcp"):
            categories["cloud"].extend(aliases)

        elif key in ("machine learning", "deep learning", "data science", "artificial intelligence", "nlp"):
            categories["data & ml"].extend(aliases)

        elif key in ("numpy", "pandas", "scikit-learn", "tensorflow", "pytorch", "keras"):
            categories["libraries and frameworks"].extend(aliases)

        elif key in ("sql", "nosql", "mongodb", "postgresql", "mysql"):
            categories["databases"].extend(aliases)

        elif key in ("git", "docker", "excel", "power bi", "tableau"):
            categories["tools"].extend(aliases)

        elif key in ("html", "css", "flask", "fastapi", "api", "rest"):
            categories["web and apis"].extend(aliases)

        else:
            categories["other"].extend(aliases)

    return {k: v for k, v in categories.items() if v}


def _norm_alias(alias: str) -> str:

    a = alias.lower().strip()
    a = re.sub(r"\s+", " ", a)
    a = a.replace("node js", "node.js")
    a = a.replace("react js", "react.js")
    return a


def normalize_jd(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\r\n|\r|\n", " ", text)
    text = re.sub(r"[•▪▫★]"," ",text)
    text = re.sub(r"[()!]\s*"," ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text 


def build_category_regex_and_map(categories: Dict[str, List[str]]) -> Dict[str, Tuple[re.Pattern, Dict[str, str]]]:

    out: Dict[str,Tuple[re.Pattern,Dict[str,str]]] = {}

    for cate , alias in categories.items():

        alias_map: Dict[str,str] = {}
        all_alias: List[str]= []

        for a in alias:
            na = a.lower().strip()
            na = _norm_alias(na)
            if not na :
                continue 
            alias_map[na] = na 
            all_alias.append(na)

        all_alias = list(dict.fromkeys(all_alias))

        all_alias.sort(key = len, reverse = True)

        alternation = "|".join(re.escape(x) for x in all_alias if x)

        patt = re.compile(rf"(?<![a-z0-9])({alternation})(?![a-z0-9])",re.IGNORECASE)


        out[cate] = (patt, alias_map)

    return out 



def jd_extract_skills(jd_text: str, skill_db: Dict[str, List[str]]) -> Dict[str, object]:

    text = normalize_jd(jd_text)

    categories = categorical_skill_db(skill_db)
    compiled_regex = build_category_regex_and_map(categories)

    by_category:Dict[str,List[str]] = {}
    all_skills: List[str] = []
    found = set()

    for category , (pattern, skill_map) in compiled_regex.items():
        found_cate:List[str] = []

        for m in pattern.finditer(text):
            s_nor = m.group(1).lower().strip()
            s_nor = _norm_alias(s_nor)
            ext_skill = skill_map.get(s_nor,s_nor) 

            if ext_skill not in found:
                found.add(ext_skill)
                all_skills.append(ext_skill)

            if ext_skill not in found_cate:

                found_cate.append(ext_skill)

        if found_cate:
            by_category[category] = found_cate

    return {"all_skills" :all_skills,
            "by_category": by_category,
            "debug":{"total_unique":len(all_skills),
                     "category_matched":list(by_category.keys())
                     }
            }
```

code 3 sample output :
{'all_skills': ['python', 'aws', 'azure', 'ai', 'ml', 'data science', 'deep learning', 'tensorflow', 'pytorch', 'docker'], 'by_category': {'programming': ['python'], 'cloud': ['aws', 'azure'], 'data & ml': ['ai', 'ml', 'data science', 'deep learning'], 'libraries and frameworks': ['tensorflow', 'pytorch'], 'tools': ['docker']}, 'debug': {'total_unique': 10, 'category_matched': ['programming', 'cloud', 'data & ml', 'libraries and frameworks', 'tools']}}

code 4 : below code is used to weight the skills according to the sections it gives two output one debug and other for cosine similarity . 

```python
import re
from typing import Dict , List , Any, Tuple
from collections import Counter

def jd_section_text_cleaning(text:str)->str:
    text  = text.lower().strip()
    text = re.sub(r"[()!.,/]", " ",text)
    return " ".join(text.split())

def normalizing_jd_sections(jd_sections:Dict[str,List[str]])->Dict[str,str]:

    output:Dict[str,str] = {}
    for section, tokens in jd_sections.items():
        if not tokens:
            output[section] = ""
        else:
            output[section] = " ".join(a.strip().lower() for a in tokens if a )

    return output

  

def build_alias_to_canonical_and_patt(skills_db:Dict[str, List[str]])->Tuple[Dict[str,str], re.Pattern]:

    alias_to_canonical :Dict[str,str] = {}

    for canonical , alias in skills_db.items():
        c = canonical.lower().strip()
        for a in (alias or []):
            a = a.lower().strip()
            if a :
                alias_to_canonical[a] = c

    all_alias = sorted(alias_to_canonical.keys() , key=len , reverse= True)
    patt = "|".join(re.escape(a) for a in all_alias)
    pattern = re.compile(rf"(?<![a-z0-9])({patt})(?![a-z0-9])",re.IGNORECASE)
    return (alias_to_canonical, pattern)


def jd_skill_weight_ext(skill_db:Dict[str, List[str]],jd_sections:Dict[str, List[str]])->Dict[str,Any]:

    section_weights = {
        "essential_requirements": 3.0,
        "experience": 2.5,
        "technical_stack": 2.0,
        "optional_requirements": 1.5,
        "requirements": 0.0,
    }
    count_weight = {1: 1.0, 2: 1.4, 3: 1.7}
    cap = 3 

    normalized_jd_sections = normalizing_jd_sections(jd_sections)
    alias_to_canon , big_pattern = build_alias_to_canonical_and_patt(skill_db)

    result:Dict[str, Any] = {}

    for section , text in normalized_jd_sections.items():

        if not text :
            continue 

        aliases = [m.group(1).lower() for m in big_pattern.finditer(text)]
        if not aliases :
            continue

        canon_list = [alias_to_canon[a] for a in aliases if a in alias_to_canon]
        counts = Counter(canon_list)

        for canon_skill , skill_count in counts.items():

            capped = min(skill_count, cap)

            if canon_skill  not in result.keys():
                result[canon_skill] = {
                    "score":0.0,
                    "by_section":{},
                    "hits":{},
                    "capped_count":{}
                }

            result[canon_skill]["hits"][section] = {"aliases":[a for a in aliases if alias_to_canon.get(a) == canon_skill],
                                                    "count" : capped}
            
            result[canon_skill]["capped_count"][section] = capped

            multi = section_weights.get(section,0.0)
            if multi >0:
                score = multi * count_weight.get(capped,0.0)
                result[canon_skill]["by_section"][section] = score
            
    for skill, dbg in result.items():
        scores = list(dbg["by_section"].values())
        if not scores :
            continue 

        base = max(scores)
        bonus = 0.2 * (sum(scores) - base)          # Essential presence dominates.
        final = base + bonus                        # Cross-section repetition increases confidence.
        final = min(final, 1.6 * base)              # But repetition cannot explode score.
        dbg["score"] = round(final , 4)

    return result 


def to_flat_skill_weights(jd_debug: Dict[str, Any]) -> Dict[str, float]:
    return {k:v["score"] for k,v in jd_debug.items() if v.get("score",0)>0}
```
code 4 sample outputs:
debug output :
{'data science': {'score': 3.0, 'by_section': {'essential_requirements': 3.0}, 'hits': {'essential_requirements': {'aliases': ['data science'], 'count': 1}}, 'capped_count': {'essential_requirements': 1}}, 'artificial intelligence': {'score': 5.61, 'by_section': {'essential_requirements': 5.1, 'optional_requirements': 2.55}, 'hits': {'essential_requirements': {'aliases': ['ai', 'ai', 'ai'], 'count': 3}, 'optional_requirements': {'aliases': ['ai', 'ai', 'ai', 'ai', 'ai'], 'count': 3}}, 'capped_count': {'essential_requirements': 3, 'optional_requirements': 3}}...}

main output :
{'data science': 3.0, 'artificial intelligence': 5.61, 'machine learning': 3.42, 'python': 3.0, 'tensorflow': 3.0, 'pytorch': 3.0, 'aws': 3.3, 'azure': 3.0, 'docker': 3.0, 'deep learning': 1.5}