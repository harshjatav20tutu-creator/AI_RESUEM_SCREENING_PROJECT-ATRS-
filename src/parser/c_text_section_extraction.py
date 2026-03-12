import re 


SECTION_KEYWORDS = {
    "education": ["education", "academic background", "academics", "qualification"],
    "skills": ["skills", "technical skills", "core skills", "technologies","key achievements"],
    "experience": ["experience", "work experience", "employment", "internship"],
    "projects": ["projects", "personal projects", "academic projects"]
}

def extract_sections(text: str) -> dict:

    extracted_sections = {}
    text = text.lower().strip()

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




