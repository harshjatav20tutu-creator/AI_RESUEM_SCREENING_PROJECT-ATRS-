from data_aquisition_01.self_data_extraction import data_extraction
from data_aquisition_01.self_data_cleaning import cleaning_data
from data_aquisition_01.self_section_extraction import self_section_extraction


text = data_extraction('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_01.pdf')
cleaning = cleaning_data(text)
sections = self_section_extraction(cleaning)
print(sections)