import pdfplumber 

# Dynamic column detection method(detect wide white space) 
# I used this method because it can handle both off centered and centered column resumes and non column resumes.
# this combination make this code able to work on more than 95% of resumes 
 
def column_resume_text_ext(pdf_path):

    with pdfplumber.open(pdf_path) as pdf:

        # for all text in resume including multiple page in single resume 
        combined_text = [] 

        # basic celaning function to get chunk of words 
        def clean(t):
            return " ".join(t.replace("\n"," ").replace("\t"," ").split())
          
        # looping through all pages 
        for page in pdf.pages: 

            # extracting every word form a page 
            words = page.extract_words()

            # handeling words error if extract_words fails
            if words is None or len(words) == 0:
                return combined_text.append(clean(page.extract_text() or ""))   
                continue

            # getting position of every word in resume
            x_positions = sorted(w["x0"] for w in words) 

            # identifying columns resumes by finding middle white space and spliting page into half
            max_gap = 0  
            split_x = page.width/2

            # looping through each position of word to get maximum position jump, it helps in finding off centered columns
            for i in range(len(x_positions) -1):
                gap = x_positions[i+1] - x_positions[i] 
                if gap > max_gap:
                    max_gap = gap
                    split_x = x_positions[i] + gap/2   # getting the middle part of the gap 

            # handelling the resumes without columns, if the max_gap is less than 6% of the page width than resume doesn't have column  
            if max_gap < page.width * 0.06: 
                combined_text.append(clean(page.extract_text() or ""))
                continue

            # setting boundaries for columns 
            left_bbox = (0,0,split_x,page.height)
            right_bbox = (split_x,0,page.width,page.height)

            # ignoring every thing outside the boundaries and extracting text from each columns 
            left_text = page.crop(left_bbox).extract_text() or ""
            right_text = page.crop(right_bbox).extract_text() or ""

            # combining text of both boundaries 
            combined_text.append(clean(left_text) + " " + clean(right_text))

        # joining text of all pages 
        return " ".join(combined_text)
            


    
# text = column_resume_text_ext('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_01.pdf')
# text = column_resume_text_ext('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_11.pdf')
# print(text)
