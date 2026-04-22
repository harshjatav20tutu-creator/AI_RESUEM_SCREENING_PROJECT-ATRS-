import re
import json
from typing import Dict , Union, List
import spacy 
import os 

class ResumeTextNormalizedandSegmentationEngine:
 
    def __init__(self,raw_resume_text:str, section_kw_config_path:str, extra_headers_config_path:str):

        self.raw_resume_text = raw_resume_text
        self.keywords = self._load_config(section_kw_config_path)
        self.section_map , self.alias = self.section_map_and_alias(self.keywords.get("universal_sections"))
        self.nlp = spacy.load("en_core_web_md")
        self.extra_headers_config_path = extra_headers_config_path
        self.normalized_text_and_sections:Dict[str,Union[str,dict]] = {}


    def _load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)
    
    def section_map_and_alias(self,universal_sections_keywords)->tuple:

        alias_to_key_map = {}
        all_alias = set()

        for sec ,alias in universal_sections_keywords.items():
            if alias:
                for a in alias:
                    a_norm = a.lower().strip()
                    alias_to_key_map[a_norm] = sec.lower().strip()
                    all_alias.add(a_norm)

        return (alias_to_key_map , all_alias)
    
    def miner_cleaning_for_segmentation(self)->str:

        # this function is for normalizing text for proper segmentation (normalizes:- \n, \r\n, tabs, extra spaces, bullets)
        text = self.raw_resume_text.replace("\r\n","\n").replace("\r","\n")
        text = re.sub(r'[•▪▫★|]', '', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)

        return text.lower().strip()

    def _text_light_cleaner(self, text):
        text = re.sub(r"[•▪▫★|—–()]"," ",text)
        text = re.sub(r"\s+", " ", text)
        text = text.lower().strip()
        return text
    

    def regex_segmentation_engine(self):

        normalized_text = self.miner_cleaning_for_segmentation() 
        
        sections:Dict[str,str] = {}

        sorted_alias = sorted(self.alias , key= len , reverse= True)
        alias_pattern = "|".join(re.escape(a) for a in sorted_alias)

        heading_pattern = re.compile(rf"(?im)^[ \t]*[-•*]?[ \t]*(?P<h>{alias_pattern})[ \t]*[:\-–—]?[ \t]*(?=\n|\r|$)")

        hits:List[tuple[int , int , str]] = []
        for m in heading_pattern.finditer(normalized_text):
            headings = m.group("h").strip().lower()
            hits.append((m.start(), m.end(), self.section_map[headings]))

        for i , (start , end , key) in enumerate(hits):
            next_start = hits[i+1][0] if i+1 < len(hits) else len(normalized_text)
            chunk = normalized_text[end:next_start]

            if chunk :
                sections[key] = self._text_light_cleaner(chunk)
            else:
                sections[key] = ""

        return sections
    
    # last case if no sections found , extracting section using NLP +

    def get_line_features(self):

        normalized_text = self.raw_resume_text.replace("\r\n","\n").replace("\r","\n")
        resume_lines = normalized_text.split("\n")
        pipes_to_disable = ["parser", "ner", "lemmatizer"]

        features_list = []
    
        # 3. Use nlp.pipe for fast batch processing of all lines at once
        with self.nlp.select_pipes(disable=pipes_to_disable):
            # nlp.pipe yields spaCy 'doc' objects efficiently
            for doc, line in zip(self.nlp.pipe(resume_lines), resume_lines):
                stripped_line = line.strip()
                total_tokens = len(doc)
            
            # Fast list comprehension for POS ratio
                pos_count = sum(1 for token in doc if token.pos_ in ['NOUN', 'PROPN'])
                pos_ratio = pos_count / total_tokens if total_tokens > 0 else 0
            
                features = {
                    "text": stripped_line,
                    "is_upper": stripped_line.isupper(),
                    "word_count": total_tokens,
                    "pos_ratio": pos_ratio,
                    "is_bullet": stripped_line.startswith(('-', '•', '*')),
                }
                features_list.append(features)
            
        return features_list
    
    def is_likely_header(self, feature):

        score = 0
    
        # Rule 1: Keyword Match (The strongest signal)
        if feature["text"].lower() in self.alias:
           score += 50
        
        # Rule 2: All Caps (Headers are often EXPERIENCE vs experience)
        if feature["is_upper"]:
            score += 20
        
        # Rule 3: Short Length (Headers are rarely long sentences)
        if 0 < feature["word_count"] < 7:
            score += 15
        
        # Rule 4: POS Tagging (Headers are rarely Verbs)
        if feature["pos_ratio"] > 0.7:
            score += 15

        # Rule 5: Negative signal (If it's a bullet, it's probably NOT a header)
        if feature["is_bullet"]:
            score -= 30
        
        return score  # Threshold
    
    def nlp_refine_segmentation(self):
        all_line_features = self.get_line_features()
        final_headers = []
        extra_headers = []

        for feature in all_line_features:

            line_score = self.is_likely_header(feature)

            if feature["text"] and line_score >= 60:

                if feature["text"].lower().strip() in self.alias:
                    final_headers.append(feature["text"])
                else:
                    extra_headers.append(feature["text"])

            elif feature["text"] and 30 <= line_score < 60 and feature["text"] not in self.alias:
                extra_headers.append(feature["text"])
           
        return (extra_headers, final_headers)
    
    def extra_headers_function(self,headings:list)->None:

        if os.path.exists(self.extra_headers_config_path) and os.path.getsize(self.extra_headers_config_path) > 0:
            with open(self.extra_headers_config_path, "r") as f:
            # Convert the loaded list into a set immediately
                data_set = set(json.load(f))
        else:
            data_set = set()

        # 2. Add new items (sets automatically ignore duplicates)
        data_set.update(headings)

        # 3. Write back to file (convert set -> list because JSON doesn't support sets)
        with open(self.extra_headers_config_path, "w") as f:
            json.dump(list(data_set), f, indent=4)


    def nlp_segmentation_and_storing_extra_headers(self):
        normalized_text = self.miner_cleaning_for_segmentation()
        extra_headings , resume_headings = self.nlp_refine_segmentation()

        if extra_headings:
            self.extra_headers_function(extra_headings)

        sections:Dict[str,str] = {}

        if not resume_headings:
            return sections
        
        resume_sections_headings = sorted(set(resume_headings),key=len, reverse=True)
        nlp_headings_patt = "|".join(re.escape(a.lower().strip()) for a in resume_sections_headings)

        heading_pattern = re.compile(
            rf"^[ \t]*({nlp_headings_patt})[ \t]*[:\-–—]?[ \t]*(?=\n|\r|$)", 
            re.IGNORECASE | re.MULTILINE
            )

        hits:List[tuple[int , int , str]] = []
        for m in heading_pattern.finditer(normalized_text):
            headings = m.group(1).strip().lower()
            hits.append((m.start(), m.end(), self.section_map[headings]))

        for i , (start , end , key) in enumerate(hits):
            next_start = hits[i+1][0] if i+1 < len(hits) else len(normalized_text)
            chunk = normalized_text[end:next_start]

            if chunk :
                sections[key] = self._text_light_cleaner(chunk)
            else:
                sections[key] = ""

        return sections 
    
    def main_resume_segmentation_engin(self):

        self.normalized_text_and_sections["cleaned_resume_text"] = self._text_light_cleaner(self.raw_resume_text)

        resume_sections = self.regex_segmentation_engine()
        if len(resume_sections)< 3:
            resume_sections = self.nlp_segmentation_and_storing_extra_headers()

        self.normalized_text_and_sections["resume_sections"] = resume_sections

        return self.normalized_text_and_sections

