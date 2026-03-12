import re

sections_dict = {"Skills":["skills","expertise","competencies","strengths","capabilities","abilities","technical skills", "core skills"],
                "Education":["academic" ,"background", "training", "schooling", "qualifications", "professional development"],
                "Projects":["project","assignments", "personal projects", "academic projects"],
                "Experience":["experience","expertise","proficiency","work experience", "employment", "internship"],
                "Summary":["summary"]

    }
def self_section_extraction(text):
    
    extracted_sections = {}
    text.lower()

    for section, keywords in sections_dict.items():

        first_pattern = "|".join(keywords)

        second_pattern = []
        for other_section , other_keywords in sections_dict.items():
            if section != other_section:
                other_keywords.extend(second_pattern)

        other_patter = "|".join(second_pattern)

        pattern = rf"({first_pattern})\s*(.*?)(?=\n\s*(?:{other_patter})\b|$)"
        match = re.search(pattern,text,re.DOTALL)

        if match :
            extracted_sections[section] = match.group(2).split()
        else:
           extracted_sections[section] = ""

    return extracted_sections

                
