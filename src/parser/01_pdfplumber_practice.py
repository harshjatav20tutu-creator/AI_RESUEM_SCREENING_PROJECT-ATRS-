import pdfplumber 
import re

# split page by x_coordinates (split page into half )
def column_resume_text_ext(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:

        page = pdf.pages[0]

        page_width = page.width 
        mid_x = page_width /2

        left_bbox = (0, 0, mid_x-80, page.height)
        right_bbox = (mid_x-80, 0, page_width, page.height)

        left_text = page.crop(left_bbox).extract_text().replace("\n"," ").replace("\t"," ")
        right_text = page.crop(right_bbox).extract_text().replace("\n"," ").replace("\t"," ")

        text1 = " ".join(left_text.split())
        text2 = " ".join(right_text.split())

        text = text1 + text2

        return text 


def impinfo_extraction(resume_text):    
    pattern = r"key achievements\s*(.*?)(?=(?:\beducation\b|\bexperience\b))"
    match = re.search(pattern,resume_text,re.IGNORECASE|re.DOTALL)

    if match:
        return match.group(1) 
    return ""

    
text = column_resume_text_ext('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_01.pdf')
skills = impinfo_extraction(text)
print(skills)

# # Dynamic column detection method(detect wide white space) 
# # I used this method because it can handle both off centered and centered column resumes and non column resumes.
# # this combination make this code able to work on more than 95% of resumes 
 
# def column_resume_text_ext(pdf_path):

#     with pdfplumber.open(pdf_path) as pdf:
#         combined_text = []

#         def clean(t):
#             return " ".join(t.replace("\n"," ").replace("\t"," ").split())

#         for page in pdf.pages:

#             words = page.extract_words()
            
#             if words is None or len(words) == 0:
#                 return combined_text.append(clean(page.extract_text() or ""))
#                 continue

#             x_positions = sorted(w["x0"] for w in words)

#             max_gap = 0 
#             split_x = page.width/2

#             for i in range(len(x_positions) -1):
#                 gap = x_positions[i+1] - x_positions[i]
#                 if gap > max_gap:
#                     max_gap = gap
#                     split_x = x_positions[i] + gap/2

#             if max_gap < page.width * 0.06:
#                 combined_text.append(clean(page.extract_text() or ""))
#                 continue

#             left_bbox = (0,0,split_x,page.height)
#             right_bbox = (split_x,0,page.width,page.height)

#             left_text = page.crop(left_bbox).extract_text() or ""
#             right_text = page.crop(right_bbox).extract_text() or ""

#             combined_text.append(clean(left_text) + " " + clean(right_text))
            
#         return " ".join(combined_text)
            


    
# # text = column_resume_text_ext('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_01.pdf')
# text = column_resume_text_ext('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_11.pdf')
# print(text)

