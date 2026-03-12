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




    




        




