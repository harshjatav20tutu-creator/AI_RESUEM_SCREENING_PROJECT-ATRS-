import re 
from typing import Dict , List ,Any

def clean_token(token):
    return token.strip(',./|()')

def section_light_cleaning(text:str)->str:
    text = re.sub(r"[(),/-]"," ",text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[’`]", "'", text)
    text = text.lower().split()
    return " ".join(text)

def jd_sections_cleaning(jd_sections:Dict[str,List[str]])-> Dict[str,str] :  

    # for job description sections
    normal_jd_sections:Dict[str,str] = {}

    for section , sec_text_tokens in jd_sections.items():
        section_all_tokens = []
        if sec_text_tokens:
            for tokens in sec_text_tokens:
                tokens = tokens.lower().strip()
                section_all_tokens.append(tokens)
            
            normal_jd_sections[section] = section_light_cleaning(" ".join(section_all_tokens))
        else:
            normal_jd_sections[section] = ""

    return normal_jd_sections

def cleaning_for_raw_text(text:str)->str:
    text = text.replace("\r\n","\n").replace("\r","\n")
    text = re.sub(r"[•▪▫★|-]"," ",text)
    text = re.sub(r"[(),/]"," ",text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower().split()
    return " ".join(text)

def extraction_must_skills_for_gate(jd_sections:Dict[str,str],skills_db:Dict[str,List[str]])->Dict[str,List[str]]: # done

    normalized_jd_sections = jd_sections_cleaning(jd_sections)

    # remember technical stack 
    if normalized_jd_sections["essential_requirements"] and normalized_jd_sections["technical_stack"]:
        ess_sec_text = " ".join(normalized_jd_sections.get("essential_requirements"),normalized_jd_sections.get("technical_stack"))
    elif normalized_jd_sections["essential_requirements"]:
        ess_sec_text = normalized_jd_sections.get("essential_requirements")
    elif normalized_jd_sections["technical_stack"]:
        ess_sec_text = normalized_jd_sections.get("technical_stack")
    else:
        ess_sec_text = ""

    alias_to_canonical:Dict[str,str] = {}

    all_skills = []
    for canonical , alias in skills_db.items():
        if alias:
            for skill in alias:
                s = skill.lower().strip()
                all_skills.append(s)
                alias_to_canonical[s] = canonical

    all_skills = sorted(all_skills, key= len, reverse= True)
    all_skills_patt = "|".join(re.escape(s) for s in all_skills)
    skill_pattern = re.compile(rf"(?<![a-z0-9])({all_skills_patt})(?![a-z0-9])",re.IGNORECASE)

    # must skills 
    must_skills = set()
    for s in skill_pattern.finditer(ess_sec_text):
        sk = s.group(1).lower().strip()
        must_skills.add(alias_to_canonical.get(sk))

    return {"must have skills":list(must_skills)}


def extraction_experience_for_gate(raw_text:str)->Dict[str,float]: # done

    normalizing_raw_text = cleaning_for_raw_text(raw_text)

    year_experience_pattern1 = r'(?i)(?:minimum\s+)?experience\s*:\s*(?:(\d+)\s*-\s*)?(\d+)\s*\+?\s*years?'
    year_experience_pattern2 = r'(?i)(?:minimum\s+)?(?:experience\s+)?(\d+)(?:\s*(?:-|to)\s*\d+)?\s*\+?\s*years?(?:\s+of)?(?:\s+experience)?'
    year_type_match1 = re.search(year_experience_pattern1, normalizing_raw_text, re.IGNORECASE)
    year_type_match2 = re.search(year_experience_pattern2, normalizing_raw_text, re.IGNORECASE)

    month_experience_pattern1 = r'(?i)(?:minimum\s+)?experience\s*:\s*(?:(\d+)\s*-\s*)?(\d+)\s*\+?\s*months?'
    month_experience_pattern2 = r'(?i)(?:minimum\s+)?(?:experience\s+)?(\d+)(?:\s*(?:-|to)\s*\d+)?\s*\+?\s*months?(?:\s+of)?(?:\s+experience)?'
    month_type_match1 = re.search(month_experience_pattern1, normalizing_raw_text, re.IGNORECASE)
    month_type_match2 = re.search(month_experience_pattern2, normalizing_raw_text, re.IGNORECASE)

    minimum_experience = 0.0
    if year_type_match1:
        exp = year_type_match1.group(1)
        exp2 = year_type_match1.group(2)
        if exp:
            minimum_experience = float(exp)
        else:
            minimum_experience = float(exp2)
    elif year_type_match2:
        minimum_experience = float(year_type_match2.group(1))
    elif month_type_match1:
        exp = month_type_match1.group(1)
        exp2 = month_type_match1.group(2)
        if exp:
            minimum_experience = float(exp)/12
        else:
            minimum_experience = float(exp2)/12
    elif month_type_match2:
        minimum_experience = float(month_type_match2.group(1))/12

    if minimum_experience != 0.0:
        minimum_experience = float(f"{minimum_experience:.1f}")

    return {"mininum experience in years":minimum_experience}


# not fully tested 
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


# using sliding wondow to extract location if we find work mode , slicing surrounding 15 words 
def extract_work_mode_loc_second_method(raw_jd:str, target_word:set, N:int)->str|None: # done

    words = re.findall(r'\b\w+\b', raw_jd.lower())

    target_indices = [i for i , word in enumerate(words) if word in target_word]
    if not target_indices:
        return None 
    target_index = target_indices[0]

    start_index = max(0,target_index - N)
    end_index = min(len(words), target_index +N +1)

    surrounding_words = words[start_index:end_index]

    result = " ".join(surrounding_words).lower()

    return result 

def extraction_workmode_location_for_gate(raw_jd:str)->Dict[str,str|list]: # flaw in this function
    # header patterns 
    pattern_one = r"(?i)(?:(?:location|job\s*location|office\s*location|base|based\s*in|work\s*model|workplace\s*type|work\s*environment|job\s*type)\s*[:\-]\s*|#LI-)(remote|hybrid|on-?site|wfh)(?:[\s\-(|]+([a-zA-Z\s,]+)[)\n]*)?"
    pattern_two = r"(?i)(?:location|job\s*location|office\s*location|base|based\s*in|work\s*model|workplace\s*type|work\s*environment|job\s*type)\s*[:\-]\s*([a-zA-Z\s,]+?)[\s\-(|]+(remote|hybrid|on-?site|wfh)\b"

    header_match1 = re.search(pattern_one, raw_jd, re.IGNORECASE)
    header_match2 = re.search(pattern_two, raw_jd, re.IGNORECASE)

    work_mode = None
    work_location = set()
    evidence = None
    if header_match1:
        wm = header_match1.group(1).lower().strip() # work mode 
        loc = header_match1.group(2).lower().strip() # location 
        if wm and loc:
            work_mode = wm 
            work_location.add(loc)
            evidence = header_match1.group()

    elif header_match2:
        wm = header_match2.group(2).lower().strip() # work mode 
        loc = header_match2.group(1).lower().strip() # location 
        if wm and loc:
            work_mode = wm 
            work_location.add(loc)
            evidence = header_match2.group()


    it_city_gazetteer = {
    "Bengaluru": ["bengaluru", "bangalore", "blr"],
    "Pune": ["pune", "pnq", "poona"],
    "Hyderabad": ["hyderabad", "hyd", "cyberabad", "hitec city"],
    "Chennai": ["chennai", "madras", "maa"],
    "Mumbai": ["mumbai", "bombay", "bom", "navi mumbai"],
    "Delhi NCR": ["delhi ncr", "delhi", "new delhi", "gurgaon", "gurugram", "noida", "ncr"],
    "Kolkata": ["kolkata", "calcutta", "ccu"],
    "Ahmedabad": ["ahmedabad", "amd", "gandhinagar"],
    "Thiruvananthapuram": ["thiruvananthapuram", "trivandrum", "trv"],
    "Kochi": ["kochi", "cochin", "cok"],
    "Chandigarh": ["chandigarh", "mohali", "tricity"],
    "Indore": ["indore", "ind"],
    "Coimbatore": ["coimbatore", "cjb"]
    }


    alias_to_canonical = {}
    all_alias = []
    for city , alias in it_city_gazetteer.items():
        for a in alias:
            a = a.lower().strip()
            all_alias.append(a)
            alias_to_canonical[a] = city.lower().strip()

    normal_work_location = set()
    if not work_mode or not work_location :

        work_mode_window = extract_work_mode_loc_second_method(raw_jd, {"remote", "hybrid","onsite","on-site"},15)
        if work_mode_window is None:
            return {
            "work mode":work_mode,
            "work location":list(normal_work_location),
            "evidence":evidence
            }

        workmode_pattern = r"(?i)\b(remote|hybrid|on-?site|onsite)\b"
        
        normal_all_alias = set(sorted(all_alias, key=len, reverse=True))
        all_loc = "|".join(re.escape(c) for c in normal_all_alias if c )
        loc_pattern = re.compile(rf"\b({all_loc})\b",re.IGNORECASE)

        work_mode_match = re.search(workmode_pattern , work_mode_window, re.IGNORECASE)
        if work_mode_match:
            work_mode = work_mode_match.group(1).lower().strip()

        for m in loc_pattern.finditer(work_mode_window):
            norm_m = m.group(1).lower().strip()
            work_location.add(norm_m)

        evidence = work_mode_window


    if work_mode == "onsite":
        work_mode.replace("onsite","on-site")

    if work_location:
        for lo in work_location:
            normal_work_location.add(alias_to_canonical.get(lo))
    else:
        normal_work_location = work_location

    return {
        "work mode":work_mode,
        "work location":list(normal_work_location),
        "evidence":evidence
    }


def extraction_work_authorization_for_gate(raw_jd:str)->Dict[str,Any]: # need changes 

    normalized_raw_jd = " ".join(re.findall(r'\b\w+\b', raw_jd.lower()))

    work_authorization_anchors = {
    "work authorization","authorized to work","legally authorized","right to work",
    "work permit","eligible to work","work eligibility","employment authorization","visa status",
    "legal right to work","legally permitted","valid work permit",
    "citizenship","citizen","permanent resident","national","green card",
    "oci cardholder","oci card"
    }

    normalized_work_auth_ancor = set()
    for an in work_authorization_anchors:
        norm = an.lower().strip()
        normalized_work_auth_ancor.add(norm)


    work_auth_window = extract_work_mode_loc_second_method(normalized_raw_jd, normalized_work_auth_ancor,5)
    print(work_auth_window)

    country_gazetteer = {
    "India": ["india", "ind", "indian"],
    "United States": ["united states", "us", "usa", "u.s.", "u.s.a.", "america", "united states of america", "american"],
    "United Kingdom": ["united kingdom", "uk", "u.k.", "britain", "great britain", "england", "uk/eu"],
    "Canada": ["canada", "can", "canadian"],
    "Australia": ["australia", "aus", "australian"],
    "Germany": ["germany", "de", "deutschland", "german"],
    "Singapore": ["singapore", "sg", "singaporean"],
    "United Arab Emirates": ["united arab emirates", "uae", "u.a.e.", "emirati"],
    "New Zealand": ["new zealand", "nz", "kiwi"],
    "Ireland": ["ireland", "ie", "irish"]
    }

    country_norm_dict = {}
    all_contry_alias = set()
    for canonical , alias in country_gazetteer.items():
        for a in alias:
            a_norm = a.lower().strip()
            all_contry_alias.add(a_norm)
            country_norm_dict[a] = canonical.lower().strip()

    all_contry_alias = sorted(list(all_contry_alias), key=len, reverse = True)

    big_patt = "|".join(c for c in all_contry_alias)
    work_authorization = ""
    if work_auth_window:
        match = re.search(rf"\b({big_patt})\b", work_auth_window.lower().strip(), re.IGNORECASE)

        if match :
            work_authorization += country_norm_dict.get(match.group(1).lower().strip(),"unknown")
        else:
            work_authorization += "unknown"


     
    sponsorship_anchors = {
    "sponsorship",
    "sponsor",
    "sponsoring",
    "visa sponsorship",
    "h1b sponsorship",
    "h-1b sponsorship",
    "employment sponsorship"
    }

    sponsorship_negations = {
    "no","not","without","cannot","unable","don't","do not","won't","will not",
    "doesn't","does not","ineligible","unsupported","none"
    }

    sponsorship_window = extract_work_mode_loc_second_method(normalized_raw_jd, sponsorship_anchors,4)
    if sponsorship_window:
        negation_patt = "|".join(n.lower().strip() for n in sponsorship_negations)

        sponsor_match = re.search(rf"\b({negation_patt})\b", sponsorship_window.lower().strip(), re.IGNORECASE)

        if sponsor_match:
            sponsorship = False
        else:
            sponsorship = True 
    else:
        sponsorship = "unknown"

    return {"work authorization":work_authorization,
            "sponsorship":sponsorship
            }

def qualification_requirements_for_resume(jd_sections, skills_db, raw_jd):
    jd_must_skills = extraction_must_skills_for_gate(jd_sections , skills_db)
    mininum_experience = extraction_experience_for_gate(raw_jd)
    degree_requirement = extraction_degree_qualification_for_gate(jd_sections)
    work_mode_n_location = extraction_workmode_location_for_gate(raw_jd)
    work_authorization_n_sponsorship = extraction_work_authorization_for_gate(raw_jd)

    return {"must have skills":jd_must_skills.get("must have skills",[]),
            "minimum experience in years":mininum_experience.get("mininum experience in years"),
            "degree requirement":degree_requirement.get("degree required"),
            "degree levels":degree_requirement.get("degree levels"),
            "degree fields":degree_requirement.get("degree fields"),
            "work mode":work_mode_n_location.get("work mode"),
            "work location":work_mode_n_location.get("work location"),
            "work authorization":work_authorization_n_sponsorship.get("work authorization"),
            "sponsorship":work_authorization_n_sponsorship.get("sponsorship")
            }
