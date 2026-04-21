# from src.parser.a_text_extractor_code import column_resume_text_ext
from src.parser.a_text_extractor_code import ResumeParser
from src.parser.b_resume_segment_engin import ResumeTextNormalizedandSegmentationEngine
# from src.parser.b_text_cleaning import clean_text

from src.parser.c_text_section_extraction import extract_sections
from src.parser.d_skills_db import SKILL_DATABASE
from src.parser.e_text_skills_extraction import get_skills_text
from src.parser.f_resume_skill_weight import weight_resume_skills
from src.parser.g_jd_text_extraction import text_extraction_from_files
from src.parser.h_jd_section_extraction import jd_sections_ext
from src.parser.i_jd_skills_ext import jd_extract_skills
from src.parser.j_jd_skill_weight import jd_skill_weight_ext
from src.parser.j_jd_skill_weight import to_flat_skill_weights
from src.parser.k_skills_matching_scoring import resume_scoring
from src.parser.m_jd_quatification_gate_info_ext import qualification_requirements_for_resume
from src.parser.o_candidate_attribute_ext import candidate_info_ext_for_eligibility_gate
# printing two times 

resume_parser = ResumeParser(r'C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_01.pdf')
raw_resume_text = resume_parser.resume_text_extractor() 
# cleaned_text = clean_text(raw_text)
# resume_sections = extract_sections(cleaned_text)
# skills = get_skills_text(resume_sections)
# res_skl_weight = weight_resume_skills(skills,resume_sections)
# jd_text = text_extraction_from_files('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/job_descriptions/a_paste_job_description.txt')
# jd_sections = jd_sections_ext(jd_text)
# jd_skills = jd_extract_skills(jd_text,SKILL_DATABASE)
# jd_skill_weight_debug = jd_skill_weight_ext(SKILL_DATABASE, jd_sections)
# jd_skill_weight = to_flat_skill_weights(jd_skill_weight_debug)
# resume_score = resume_scoring(res_skl_weight,jd_skill_weight,SKILL_DATABASE)
# job_requirements_info_extraction = qualification_requirements_for_resume(jd_sections, SKILL_DATABASE, jd_text)
# candidate_attribute_ext = candidate_info_ext_for_eligibility_gate(resume_sections, raw_text , SKILL_DATABASE)

def main(resume_path,section_keywords_path,extra_headers_path):
    resume_parser = ResumeParser(resume_path)
    raw_resume_text = resume_parser.resume_text_extractor() 
    resume_segmentation_engin = ResumeTextNormalizedandSegmentationEngine(raw_resume_text,section_keywords_path,extra_headers_path)
    resume_norm_text_n_segments = resume_segmentation_engin.main_resume_segmentation_engin()
    


main(resume_path = r'C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_01.pdf',
    section_keywords_path = r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\resume_sections.json",
    extra_headers_path = r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\resume_extra_section.json")