import numpy as np
import pdfplumber

def data_extraction(file_path):

    with pdfplumber.open(file_path) as pdf:

        combined_text = []

        for page in pdf.pages:

            words = page.extract_words()

            # Case 1: No words detected → fallback to full page text
            if not words:
                text = page.extract_text() or ""
                combined_text.append(" ".join(text.replace("\n", " ").split()))
                continue

            # Collect x-positions of all words
            x_arr = np.array(sorted(w["x0"] for w in words))

            # --------- DECISION PART: single column vs two column ---------

            # Measure horizontal spread of text
            spread = max(x_arr) - min(x_arr)

            # If spread is small relative to page width → treat as single column
            if spread < page.width * 0.55:
                text = page.extract_text() or ""
                combined_text.append(" ".join(text.replace("\n", " ").split()))
                continue

            # --------- NOW WE SPLIT (only when real two columns exist) ---------

            # Find best split point using largest gap between word clusters
            max_gap = 0
            x_split = page.width / 2  # default

            for i in range(len(x_arr) - 1):
                gap = x_arr[i+1] - x_arr[i]   # correct gap computation

                if gap > max_gap:
                    max_gap = gap
                    x_split = (x_arr[i] + x_arr[i+1]) / 2  # midpoint of biggest gap

            # Define left and right bounding boxes
            left_bbox = (0, 0, x_split, page.height)
            right_bbox = (x_split, 0, page.width, page.height)

            left_text = page.crop(left_bbox).extract_text() or ""
            right_text = page.crop(right_bbox).extract_text() or ""

            clean_left = " ".join(left_text.replace("\n", " ").split())
            clean_right = " ".join(right_text.replace("\n", " ").split())

            combined_text.append(clean_left + " " + clean_right)

        # Return all pages + diagnostic info if needed
        return spread ,x_arr
text = data_extraction('C:/Users/HP/OneDrive/Documents/AI_resume_screening_project/Data/Resumes/resume_01.pdf')
print(text)
