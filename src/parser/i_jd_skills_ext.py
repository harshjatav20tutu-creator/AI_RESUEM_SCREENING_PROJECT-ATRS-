import re
from typing import Dict ,List , Tuple

def categorical_skill_db(skill_db: Dict[str, List[str]]) -> Dict[str, List[str]]:
    categories = {
        "programming": [],
        "cloud": [],
        "data & ml": [],
        "libraries and frameworks": [],
        "databases and server": [],
        "CI/CD and other tools": [],
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

        elif key in ("sql", "nosql", "mongodb", "postgresql", "mysql","sql_server"):
            categories["databases and server"].extend(aliases)

        elif key in ("git", "docker", "excel", "power bi", "tableau","github_actions","gitlab ci","azure devops","kubernetes"):
            categories["CI/CD and other tools"].extend(aliases)

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
    text = re.sub(r"[()!/]\s*"," ", text)  # remember i added / here 
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



