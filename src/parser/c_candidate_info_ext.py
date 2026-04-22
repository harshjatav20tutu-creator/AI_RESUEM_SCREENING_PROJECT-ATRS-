import re

raw_header_text = '''AIDEN Principal Software Engineer | Cloud Technologies | Software
Architecture | Full-Stack Development
WILLIAMS
​Email harshjatav403@gmail.com ​LinkedIn ​Austin, Texas
phone numbers, my phone number: +91 6496057493 company: +91 5373528823 
CORE COMPETENCIES SUMMARY
Cloud & System Architecture Results-driven Principal Software Engineer with over 9 years of experience designing scalable
full-stack architectures and driving cloud adoption. Proven expertise in technical leadership,
Distributed Systems Design,
demonstrated by spearheading a critical optimization initiative that reduced processing times
Microservices Architecture, Cloud-Native
by 60%. Committed to defining technical vision and fostering a culture of innovation to deliver
Infrastructure (AWS/Azure), Kubernetes &'''

class CandidateAttributesExtractionEngine:
    
    def __init__(self,raw_header_text, raw_resume_text):
        self.raw_header_text = raw_header_text
        self.raw_resume_text = raw_resume_text

    def email_extractor(self):
        if raw_header_text :
            text = self.raw_header_text
        else:
            text = self.raw_resume_text

        clean_text = re.sub(r'[\(\[\\{]at[\)\]\\}]', '@', text, flags=re.IGNORECASE)
        clean_text = re.sub(r'[\(\[\\{]dot[\)\]\\}]', '.', clean_text, flags=re.IGNORECASE)
        
