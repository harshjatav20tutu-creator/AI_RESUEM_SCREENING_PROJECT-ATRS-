from typing import List , Dict , Any
import re




def section_light_cleaning(text:str)->str:
    text = re.sub(r"[(),]"," ",text)
    text = re.sub(r"[•▪▫★|]"," ",text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[’`]", "'", text)
    text = text.lower().split()
    return " ".join(text)

def cleaning_for_raw_text(text:str)->str:
    text = text.replace("\r\n"," ").replace("\r"," ").replace("\n", " ")
    text = re.sub(r"[•▪▫★|]"," ",text)
    text = re.sub(r"[(),]"," ",text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower().split()
    return " ".join(text)

def resume_sections_cleaning(res_sections:Dict[str,List[str]])-> Dict[str,str] :  

    normal_jd_sections:Dict[str,str] = {}

    for section , sec_text_tokens in res_sections.items():
        section_all_tokens = []
        if sec_text_tokens:
            for tokens in sec_text_tokens:
                tokens = tokens.lower().strip()
                section_all_tokens.append(tokens)
            
            normal_jd_sections[section] = section_light_cleaning(" ".join(section_all_tokens))
        else:
            normal_jd_sections[section] = ""

    return normal_jd_sections
    

def candidate_skill_attribute_ext(resume_sections:Dict[str,List[str]],raw_text:str, skill_db:Dict[str,List[str]])->Dict[str,List[str]]:

    normal_res_sec = resume_sections_cleaning(resume_sections)
    normal_raw_res_text = cleaning_for_raw_text(raw_text)

    combine_section_tokens = []
    for section , section_text in normal_res_sec.items():
        if section and section in ("skills","experience","projects"):
            combine_section_tokens.append(section_text)

    combine_section_text = " ".join(combine_section_tokens)


    skills_alias_to_canonical:Dict[str,str] = {}
    all_skills = []
    for canonical , alias in skill_db.items():
        if alias:
            for skill in alias:
                s = skill.lower().strip()
                all_skills.append(s)
                skills_alias_to_canonical[s] = canonical

    all_skills = sorted(all_skills, key= len, reverse= True)
    all_skills_patt = "|".join(re.escape(s) for s in all_skills)
    skill_pattern = re.compile(rf"(?<![a-z0-9])({all_skills_patt})(?![a-z0-9])",re.IGNORECASE)

    candidate_skills1 = set()
    for m in skill_pattern.finditer(combine_section_text):
        if m :
            norm_m = m.group(1).lower().strip()
            candidate_skills1.add(skills_alias_to_canonical.get(norm_m))

    # extraction skills from raw resume text 

    candidate_skills2 = set()
    for m in skill_pattern.finditer(normal_raw_res_text):
        if m :
            norm_m = m.group(1).lower().strip()
            candidate_skills2.add(skills_alias_to_canonical.get(norm_m))

    candidate_combined_skills = candidate_skills1.union(candidate_skills2)

    return {"candidate_skills":list(candidate_combined_skills)}

def candidate_experience_extraction(raw_text:str, resume_sections:Dict[str,str])->Dict[str,float|None]:
    normal_res_sec = resume_sections_cleaning(resume_sections)

    if normal_res_sec.get("experience") :
        resume_exp_text = normal_res_sec.get("experience")
    else:
        resume_exp_text = cleaning_for_raw_text(raw_text)

    # this pattern is used to handle these experience pattern (5 years of experience , years experience: 4 years)
    years_pattern = re.compile(
    r"(?i)(?:(?P<years_front>\d+)\+?\s*\b(?:years?|yrs?|yr)\b(?:\s+of)?\s+\b(?:experience|exps?|exp)\b|"
    r"\b(?:experience|exps?|exp)\b\s+(?P<years_back>\d+)\+?\s*\b(?:years?|yrs?|yr)\b)"
    )

    max_experience = 0.0 
    total_experience = 0.0
    for year in years_pattern.finditer(resume_exp_text):

        extracted_experience = year.group('years_front') or year.group('years_back')
        if extracted_experience :
            total_experience += float(extracted_experience)
            if float(extracted_experience) > max_experience:
                max_experience = float(extracted_experience)

    if max_experience == 0.0:
        # this pattern is used to handle these experience pattern (5 months of experience , months experience: 8 months)
        months_pattern = re.compile(
        r"(?:(?P<months_front>\d+)\+?\s*\b(?:months?|mos?|mo)\b(?:\s+of)?\s+\b(?:experience|exps?|exp)\b|"
        r"\b(?:experience|exps?|exp)\b\s+(?P<months_back>\d+)\+?\s*\b(?:months?|mos?|mo)\b)",
        re.IGNORECASE
        )

        for months in months_pattern.finditer(resume_exp_text):

            extracted_experience = months.group('months_front') or months.group('months_back')
            if extracted_experience :
                total_experience += float(extracted_experience)
                if float(extracted_experience)/12 > max_experience:
                    max_experience = float(extracted_experience)/12

    if max_experience == 0.0:

        date_range_pattern = re.compile(
        r"(?i)\b(?P<start_month>0?[1-9]|1[0-2]|[a-z]{3,9})[\s/\-]+(?P<start_year>\d{4})"
        r"\s*(?:to|-)\s*"
        r"(?P<end_month>0?[1-9]|1[0-2]|[a-z]{3,9})[\s/\-]+(?P<end_year>\d{4})\b"
        )

        month_to_float = {
        "january": 1.0, "jan": 1.0, "1": 1.0, "01": 1.0,
        "february": 2.0, "feb": 2.0, "2": 2.0, "02": 2.0,
        "march": 3.0, "mar": 3.0, "3": 3.0, "03": 3.0,
        "april": 4.0, "apr": 4.0, "4": 4.0, "04": 4.0,
        "may": 5.0, "5": 5.0, "05": 5.0,
        "june": 6.0, "jun": 6.0, "6": 6.0, "06": 6.0,
        "july": 7.0, "jul": 7.0, "7": 7.0, "07": 7.0,
        "august": 8.0, "aug": 8.0, "8": 8.0, "08": 8.0,
        "september": 9.0, "sep": 9.0, "sept": 9.0, "9": 9.0, "09": 9.0,
        "october": 10.0, "oct": 10.0, "10": 10.0,
        "november": 11.0, "nov": 11.0, "11": 11.0,
        "december": 12.0, "dec": 12.0, "12": 12.0
        }
        
        for data_range in date_range_pattern.finditer(resume_exp_text):

            st_year = data_range.group('start_year').lower().strip()
            ed_year = data_range.group('end_year').lower().strip()
            st_month = month_to_float.get(data_range.group('start_month').lower().strip())
            ed_month = month_to_float.get(data_range.group('end_month').lower().strip())

            year_exp = float(ed_year) - float(st_year)
            month_exp = (abs(st_month - ed_month))/12

            total_experience += float(year_exp + month_exp)
            if float(year_exp + month_exp) > max_experience:
                max_experience = (year_exp + month_exp)

    return {"total_experience": float(f"{total_experience:.1f}"),
            "max_experience": float(f"{max_experience:.1f}")}


def candidate_degree_level_n_field_extraction(raw_text:str, resume_sections:Dict[str,str])->Dict[str,List[str]]: 

    degree_levels = {
    "bachelor": ["bachelor", "bachelors", "b.s", "bs", "b.a", "ba", "b.tech", "btech", "b.e", "be", "b.sc", "bsc", "undergrad"],
    "master": ["master", "masters", "m.s", "ms", "m.a", "ma", "m.tech", "mtech", "m.e", "me", "m.sc", "msc", "mba", "grad"],
    "doctorate": ["phd", "ph.d", "doctorate", "doctoral", "d.phil"],
    "diploma": ["diploma", "associate", "a.s", "a.a", "certification", "cert"]
    }

    degree_fields = {
    "computer_science": ["computer science", "cs", "compsci", "computer engineering", "software engineering"],
    "artificial_intelligence": ["artificial intelligence", "ai", "machine learning", "ml", "deep learning", "nlp", "natural language processing"],
    "data_science": ["data science", "ds", "data analytics", "data engineering", "big data"],
    "information_technology": ["information technology", "it", "information systems", "mis"]
    }

    candidate_resume_sections = resume_sections_cleaning(resume_sections)
    normal_raw_res_text = cleaning_for_raw_text(raw_text)

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

    degree_level_ext = set()
    degree_fields_ext = set()
    if candidate_resume_sections.get("education"):

        for m in degree_level_pattern.finditer(candidate_resume_sections.get("education")):
            if m:
                m_norm = m.group(1).lower().strip()
                degree_level_ext.add(to_canon_d_level.get(m_norm))

        if degree_level_ext:
            for m in degree_fields_pattern.finditer(candidate_resume_sections.get("education")):
                if m:
                    m_norm = m.group(1).lower().strip()
                    degree_fields_ext.add(to_canon_d_fields.get(m_norm))

        return {"degree_levels":list(degree_level_ext),
                "degree_fields":list(degree_fields_ext)}
    
    else: 

        tech_token_pattern = re.compile(
        r"(?i)\.net|\b\w+(?:\.\w+)+\b|\b\w+(?:\+\+|#)|\b\w+\b"
        )

        clean_tokens = [m.group(0).lower() for m in tech_token_pattern.finditer(normal_raw_res_text)]

        for i , word in enumerate(clean_tokens):
            if word in all_degree_level:
                degree_level_ext.add(to_canon_d_level.get(word.lower().strip()))
                window_tokens = clean_tokens[i:i+7]
                sliced_window = " ".join(window_tokens)
                for m in degree_fields_pattern.finditer(sliced_window):
                    m_norm = m.group(1).lower().strip()
                    degree_fields_ext.add(to_canon_d_fields.get(m_norm))

    return {"degree_levels":list(degree_level_ext),
            "degree_fields":list(degree_fields_ext)}

def candidate_location_extraction(raw_text:str)->str:
    indian_states = {
    "andhra pradesh": "Andhra Pradesh", "ap": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh", "ar": "Arunachal Pradesh",
    "assam": "Assam", "as": "Assam",
    "bihar": "Bihar", "br": "Bihar",
    "chhattisgarh": "Chhattisgarh", "cg": "Chhattisgarh",
    "goa": "Goa", "ga": "Goa",
    "gujarat": "Gujarat", "gj": "Gujarat", "guj": "Gujarat",
    "haryana": "Haryana", "hr": "Haryana",
    "himachal pradesh": "Himachal Pradesh", "hp": "Himachal Pradesh",
    "jharkhand": "Jharkhand", "jh": "Jharkhand",
    "karnataka": "Karnataka", "ka": "Karnataka",
    "kerala": "Kerala", "kl": "Kerala",
    "madhya pradesh": "Madhya Pradesh", "mp": "Madhya Pradesh",
    "maharashtra": "Maharashtra", "mh": "Maharashtra", "mah": "Maharashtra",
    "manipur": "Manipur", "mn": "Manipur",
    "meghalaya": "Meghalaya", "ml": "Meghalaya",
    "mizoram": "Mizoram", "mz": "Mizoram",
    "nagaland": "Nagaland", "nl": "Nagaland",
    "odisha": "Odisha", "orissa": "Odisha", "or": "Odisha", "od": "Odisha",
    "punjab": "Punjab", "pb": "Punjab",
    "rajasthan": "Rajasthan", "rj": "Rajasthan", "raj": "Rajasthan",
    "sikkim": "Sikkim", "sk": "Sikkim",
    "tamil nadu": "Tamil Nadu", "tn": "Tamil Nadu",
    "telangana": "Telangana", "ts": "Telangana", "tg": "Telangana",
    "tripura": "Tripura", "tr": "Tripura",
    "uttar pradesh": "Uttar Pradesh", "up": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand", "uk": "Uttarakhand", "ut": "Uttarakhand",
    "west bengal": "West Bengal", "wb": "West Bengal",
    "delhi": "Delhi", "dl": "Delhi", "ncr": "Delhi", "new delhi": "Delhi",
    "chandigarh": "Chandigarh", "ch": "Chandigarh",
    "jammu and kashmir": "Jammu and Kashmir", "jk": "Jammu and Kashmir", "j&k": "Jammu and Kashmir",
    "ladakh": "Ladakh", "la": "Ladakh"
    }

    normal_raw_res_text = cleaning_for_raw_text(raw_text)

    tech_token_pattern = re.compile(
        r"(?i)\.net|\b\w+(?:\.\w+)+\b|\b\w+(?:\+\+|#)|\b\w+\b"
    )
    token_array = [m.group(0).lower() for m in tech_token_pattern.finditer(normal_raw_res_text)]

    header_tokens = token_array[:150]
    header_text = " ".join(header_tokens).lower()
    
    sorted_state_keys = sorted(indian_states.keys(), key=len, reverse=True)
    
    high_risk_codes = {"as", "or", "up", "am", "in", "me", "go", "an", "is"}
    
    for key in sorted_state_keys:
        if key in high_risk_codes:

            pattern = rf"(?:location|state|address|city)\s*(?::|-)?\s*\b{key}\b"
            if re.search(pattern, header_text):
                return {"current_location": indian_states[key]}
        else:

            if re.search(rf"\b{re.escape(key)}\b", header_text):
                return {"current location": indian_states[key]}
                
    return {"current_location": "unknown"}

def candidate_work_authorization_extraction(res_text:str):
    normal_raw_res_text = cleaning_for_raw_text(res_text)

    work_authorization_tiers = {
    "authorized": [
        "citizen", "permanent resident", "pr", "green card", 
        "passport holder", "authorized to work", "no sponsorship"
    ],
    "temporary_authorized": [
        "f1", "opt", "cpt", "tn visa", "dependent visa"
    ],
    "requires_sponsorship": [
        "h1b", "h-1b", "requires sponsorship", "need sponsorship", 
        "visa transfer", "seeking sponsorship"
    ]
    }

    tech_token_pattern = re.compile(
        r"(?i)\.net|\b\w+(?:\.\w+)+\b|\b\w+(?:\+\+|#)|\b\w+\b"
    )
    token_array = [m.group(0).lower() for m in tech_token_pattern.finditer(normal_raw_res_text)]


    header_text = " ".join(token_array[:150]).lower()
    footer_text = " ".join(token_array[-150:]).lower()
    full_search_text = header_text + " " + footer_text
    
    for tier, keywords in work_authorization_tiers.items():
        for keyword in keywords:

            if re.search(rf"\b{re.escape(keyword)}\b", full_search_text):
                return {"work_authorization": tier}
                

    return {"work_authorization": "unknown"}

def candidate_info_ext_for_eligibility_gate(resume_sections:Dict[str,List[str]], raw_text:str , skill_db:Dict[str,List[str]]):
    candidate_skills = candidate_skill_attribute_ext(resume_sections, raw_text, skill_db)
    candidate_experience = candidate_experience_extraction(raw_text , resume_sections)
    candidate_degree_ext = candidate_degree_level_n_field_extraction(raw_text, resume_sections)
    candidate_location = candidate_location_extraction(raw_text)
    candidate_work_authorization = candidate_work_authorization_extraction(raw_text)

    return {"candidate_skills":candidate_skills.get("candidate_skills"),
            "candidate_total_experience":candidate_experience.get("total_experience"),
            "candidate_maximum_experience":candidate_experience.get("max_experience"),
            "candidates_degree_levels":candidate_degree_ext.get("degree_levels"),
            "candidates_degree_fields":candidate_degree_ext.get("degree_fields"),
            "candidates_location":candidate_location.get("current_location"),
            "candidates_work_authorization":candidate_work_authorization.get("work_authorization")}

