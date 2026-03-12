import pdfplumber 



def data_extraction(file_path):


    with pdfplumber.open(file_path) as pdf :

        combined_text = []

        for page in pdf.pages:

            words = page.extract_words()

            if not words :
                return combined_text.append(" ".join(page.extract_text().replace("\n"," ").split()))
                
            
            else:

                x_position = sorted(w["x0"] for w in words)

                max_gap = 0 
                x_split = page.width/2

                for i in range(len(x_position)-1):
                    gap = x_position[i+1] - x_position[i]
                    if gap > max_gap :
                        max_gap = gap
                        x_split = x_position[i] + gap/2
                

            if max_gap < page.width * 0.06:
                return " ".join((page.extract_text() or "").replace("\n"," ").split())


            left_bbox = (0,0,x_split,page.height)
            right_bbox = (x_split,0,page.width,page.height)

            left_text = page.crop(left_bbox).extract_text() or ""
            right_text = page.crop(right_bbox).extract_text() or ""

            all_text = " ".join(left_text.replace("\n"," ").split()) + " " + " ".join(right_text.replace("\n"," ").split())
        
            combined_text.append(" "+all_text)


    return " ".join(combined_text)



text = data_extraction('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_03.pdf')
print(text)

        






