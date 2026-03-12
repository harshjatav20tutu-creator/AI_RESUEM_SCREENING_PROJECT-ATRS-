import re
from typing import Dict , List 


def jd_sections_ext(text:str)->Dict[str,List[str]]:


    job_description_map = {

        "essential_requirements": [
            "required qualifications", "basic qualifications", "minimum qualifications",
            "minimum requirements", "must have", "must-haves", "mandatory","Required Skills & Qualifications"
        ],

        "requirements": [
            "requirements", "qualifications", "what you ll need",
            "what you bring", "who you are", "skills & qualifications"
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

        "education": [
            "education", "educational background", "academic background",
            "academic requirements", "education & experience", "education and experience",
            "degree", "degrees", "degree requirements", "education qualifications",
            "academics", "university degree", "college degree", "education required",
            "qualifications & education", "educational requirements", "academic qualifications"
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