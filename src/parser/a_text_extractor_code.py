from typing import List 
import pdfplumber 
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

# Dynamic column detection method(detect wide white space) 
# I used this method because it can handle both off centered and centered column resumes and non column resumes.
# this combination make this code able to work on more than 95% of resumes 
 
# def column_resume_text_ext(pdf_path):

#     with pdfplumber.open(pdf_path) as pdf:

#         # for all text in resume including multiple page in single resume 
#         combined_text = [] 

#         # basic celaning function to get chunk of words 
#         def clean(t):
#             return " ".join(t.replace("\n"," ").replace("\t"," ").split())
          
#         # looping through all pages 
#         for page in pdf.pages: 

#             # extracting every word form a page 
#             words = page.extract_words()

#             # handeling words error if extract_words fails
#             if words is None or len(words) == 0:
#                 return combined_text.append(clean(page.extract_text() or ""))   
#                 continue

#             # getting position of every word in resume
#             x_positions = sorted(w["x0"] for w in words) 

#             # identifying columns resumes by finding middle white space and spliting page into half
#             max_gap = 0  
#             split_x = page.width/2

#             # looping through each position of word to get maximum position jump, it helps in finding off centered columns
#             for i in range(len(x_positions) -1):
#                 gap = x_positions[i+1] - x_positions[i] 
#                 if gap > max_gap:
#                     max_gap = gap
#                     split_x = x_positions[i] + gap/2   # getting the middle part of the gap 

#             # handelling the resumes without columns, if the max_gap is less than 6% of the page width than resume doesn't have column  
#             if max_gap < page.width * 0.06: 
#                 combined_text.append(clean(page.extract_text() or ""))
#                 continue

#             # setting boundaries for columns 
#             left_bbox = (0,0,split_x,page.height)
#             right_bbox = (split_x,0,page.width,page.height)

#             # ignoring every thing outside the boundaries and extracting text from each columns 
#             left_text = page.crop(left_bbox).extract_text() or ""
#             right_text = page.crop(right_bbox).extract_text() or ""

#             # combining text of both boundaries 
#             combined_text.append(clean(left_text) + " " + clean(right_text))

#         # joining text of all pages 
#         return " ".join(combined_text)
            
class ResumeParser:
    def __init__(self, file_path:str):
        self.file_path = file_path

    def parse_pdf(self) ->str:
        """Logic for coordinate-based PDF density parsing."""

        body_text_segments:List[str] = []

        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                # --- DENSITY LOGIC START ---
                num_slices = 20 
                slice_width = page.width / num_slices
                density_map = []

                for i in range(num_slices):
                    bbox = (i * slice_width, 0, (i + 1) * slice_width, page.height)
                    words = page.crop(bbox).extract_words()
                    density_map.append(sum(len(w["text"]) for w in words))

                mid_start, mid_end = 4, 16
                min_density = min(density_map[mid_start:mid_end])
                min_indices = [i for i, d in enumerate(density_map) if d == min_density and mid_start <= i < mid_end]

                valley_start, valley_end = min_indices[0], min_indices[-1] + 1
                split_x = ((valley_start + valley_end) / 2) * slice_width

                active_slices = [d for d in density_map if d > 0]
                # --- DECISION LOGIC ---
                if active_slices:
                    avg_active = sum(active_slices) / len(active_slices)
                    if min_density < (avg_active * 0.15):
                        left = page.crop((0, 0, split_x, page.height)).extract_text() or ""
                        right = page.crop((split_x, 0, page.width, page.height)).extract_text() or ""
                        body_text_segments.append(f"{left}\n{right}")
                        continue # Move to next page
                
                # Fallback for single column
                # body_text_segments.append(page.extract_text() or "")
        
        return "\n".join(body_text_segments)

    def parse_docx(self) -> str:
        """Logic for structural XML parsing of Word documents."""
        doc = Document(self.file_path)
        combined_data:List[str] = []

        # 1. Main Flow (Paragraphs and Tables)
        # Note: We need to use internal element checks
        for element in doc.element.body:
            # Reconstruct objects from XML elements
            if element.tag.endswith('p'):
                para = Paragraph(element, doc)
                if para.text.strip():
                    combined_data.append(para.text.strip())
            elif element.tag.endswith('tbl'):
                table = Table(element, doc)
                for row in table.rows:
                    row_text = " | ".join(c.text.strip() for c in row.cells if c.text.strip())
                    if row_text:
                        combined_data.append(row_text)

        # 2. Text Box Hunter (The 'Spam' protection)
        seen_texts = set()
        box_texts = []
        for txbx in doc.element.xpath('.//*[local-name()="txbxContent"]'):
            current_box = "\n".join(Paragraph(p, doc).text.strip() for p in txbx.xpath('.//*[local-name()="p"]') if Paragraph(p, doc).text.strip())
            if current_box and current_box not in seen_texts:
                box_texts.append(current_box)
                seen_texts.add(current_box)

        if box_texts:
            combined_data.append("\n--- ADDITIONAL DATA ---")
            combined_data.extend(box_texts)

        return "\n".join(combined_data)

    def resume_text_extractor(self) ->str:
        """The 'Brain' that decides which parser to use."""
        if self.file_path.lower().endswith(".pdf"):
            return self.parse_pdf()
        elif self.file_path.lower().endswith(".docx"):
            return self.parse_docx()
        else:
            return ""



