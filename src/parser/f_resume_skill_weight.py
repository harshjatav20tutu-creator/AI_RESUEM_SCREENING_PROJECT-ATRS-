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

        







    
        














