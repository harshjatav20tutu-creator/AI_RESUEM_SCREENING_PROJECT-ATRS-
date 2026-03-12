from typing import List , Dict , Any
import re




def section_light_cleaning(text:str)->str:
    text = re.sub(r"[(),/]"," ",text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[’`]", "'", text)
    text = text.lower().split()
    return " ".join(text)

def cleaning_for_raw_text(text:str)->str:
    text = text.replace("\r\n","\n").replace("\r","\n")
    text = re.sub(r"[•▪▫★|]"," ",text)
    text = re.sub(r"[(),/]"," ",text)
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
