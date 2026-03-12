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
        "education":0.0,
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




    








    
