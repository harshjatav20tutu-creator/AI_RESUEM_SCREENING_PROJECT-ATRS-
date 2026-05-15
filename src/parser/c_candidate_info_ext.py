import re
import phonenumbers
import json
import requests
from typing import Dict, Optional

raw_header_text = '''AIDEN Principal Software Engineer | Cloud Technologies | Software
WILLIAMS
Architecture | Full-Stack Development
​Email aidenwilliams403@gmail.com ​LinkedIn ​Austin, Texas
phone numbers, my phone number: +91 8094766411 , +44 78787-87878 company:
CORE COMPETENCIES SUMMARY
Cloud & System Architecture Results-driven Principal Software Engineer with over 9 years of experience designing scalable
full-stack architectures and driving cloud adoption. Proven expertise in technical leadership,
Distributed Systems Design,
demonstrated by spearheading a critical optimization initiative that reduced processing times
Microservices Architecture, Cloud-Native
by 60%. Committed to defining technical vision and fostering a culture of innovation to deliver
Infrastructure (AWS/Azure), Kubernetes &'''

raw_resume_text = '''AIDEN
WILLIAMS
CORE COMPETENCIES
Cloud & System Architecture
Distributed Systems Design,
Microservices Architecture, Cloud-Native
Infrastructure (AWS/Azure), Kubernetes &
Docker, Infrastructure as Code
(Terraform).
Full-Stack Development
Modern JavaScript (React/Node.js), API
Design (REST & GraphQL), Relational &
NoSQL Database Modeling, Performance
Tuning, Secure Coding Practices
Technical Leadership
Engineering Strategy, Team Mentorship &
Code Reviews, Agile/Scrum Management,
CI/CD Pipeline Optimization, Cross-
Functional Collaboration
KEY ACHIEVEMENTS
Enhanced System Performance
Redesigned critical streaming service
infrastructure, achieving 30% reduction in
latency and accommodating 1M
concurrent users.
Successful Project Delivery
Led a team that delivered a new cloud-
based analytics platform, which
increased customer engagement by 50%
within the first six months.
Innovative Product Development
Spearheaded the development of a
groundbreaking AI tool that reduced
processing time by 60%, impacting user
satisfaction ratings positively.
Team Leadership and Growth
Mentored junior engineers, resulting in a
measurable 40% increase in team
performance and a six-month reduction in
project delivery times.

Powered by
Principal Software Engineer | Cloud Technologies | Software
Architecture | Full-Stack Development
​Email ​LinkedIn ​Austin, Texas
SUMMARY
Results-driven Principal Software Engineer with over 9 years of experience designing scalable
full-stack architectures and driving cloud adoption. Proven expertise in technical leadership,
demonstrated by spearheading a critical optimization initiative that reduced processing times
by 60%. Committed to defining technical vision and fostering a culture of innovation to deliver
high-performance software solutions.
EXPERIENCE
Lead Software Engineer 01/2020 - 10/2023
Google LLC Austin, Texas
• Architected and implemented a new microservices-oriented architecture that improved
system resilience and scalability, enabling an annual growth rate of 20%.
• Collaborated with product management to develop a roadmap that synchronized
engineering efforts with business goals, leading to a software delivery cycle 25% faster.
• Conducted comprehensive code reviews and integrated optimized coding practices which
led to a 15% reduction in application defects.
• Played a key role in migrating legacy applications to Azure, reducing infrastructure costs by
30% while increasing overall system performance.
• Facilitated knowledge-sharing sessions that enhanced team expertise in cloud
technologies, resulting in reduced onboarding time for new employees.
Software Engineer 01/2016 - 12/2019
Amazon Web Services Austin, Texas
• Developed scalable back-end services utilizing AWS, decreasing processing times by 50%
for high-frequency data inputs.
• Engineered high-availability applications with a 99.99% uptime guarantee, ensuring
customer satisfaction and retention principles were upheld.
• Participated in Agile development sprints and improved team productivity through effective
use of DevOps practices that shortened release timelines.
• Integrated advanced AI solutions into existing platforms, yielding a 35% improvement in
data processing efficiency and user engagement metrics.
• Authored technical documentation and training guides that improved team workflow and
elevated operational standards across functions.
Junior Software Developer 01/2014 - 12/2015
IBM Austin, Texas
• Assisted in the development of a cross-platform application framework using Java, which
increased project versatility and reduced deployment errors.
• Engaged in rigorous testing and quality assurance practices, leading to a documented
decrease in bugs post-deployment by 20%.
• Collaborated closely with senior developers to implement user feedback in software
enhancements, drastically improving the user experience.
• Executed daily scrums and contributed to sprint planning meetings, resulting in a team
culture focused on accountability and continuous delivery.
• Enhanced existing documentation and implementation guides, improving adoption rates
among internal teams and reducing support queries substantially.
EDUCATION
Master of Science in Computer Science 2014
University of Texas at Austin Austin, Texas
www.enhancv.com'''

class CandidateAttributesExtractionEngine:
    
    def __init__(self,raw_header_text, raw_resume_text):
        self.raw_header_text = raw_header_text
        self.clean_header_text = self.header_normalizer(self.raw_header_text)
        self.raw_resume_text = raw_resume_text

    def header_normalizer(self,text):
        text = re.sub(r'[\(\[\\{]at[\)\]\\}]', '@', text, flags=re.IGNORECASE)
        text = re.sub(r'[\(\[\\{]dot[\)\]\\}]', '.', text, flags=re.IGNORECASE)
        return text

    def extract_and_validate_phones(self, text, default_region="IN"):
        """
        Extracts phone numbers and validates them against international standards.
        'default_region' is used if no country code is found (e.g., 'IN' for India, 'US' for USA).
        """
        valid_phones = []
        
        # Use the broad regex to find potential candidates first
        raw_matches = re.findall(r'(?:\+?\d{1,4}[\s.-]?)?\(?\d{2,5}\)?[\s.-]?\d{2,9}[\s.-]?\d{2,9}', text)
        
        for match in raw_matches:
            try:
                # Parse the number using Google's logic
                parsed_num = phonenumbers.parse(match, default_region)
                
                # Check if it's actually a possible/valid number in that region
                if phonenumbers.is_possible_number(parsed_num):
                    # Standardize to E.164 format (+919876543210)
                    formatted = phonenumbers.format_number(
                        parsed_num, phonenumbers.PhoneNumberFormat.E164
                    )
                    valid_phones.append(formatted)
            except Exception:
                continue
                
        return list(set(valid_phones))
    
    def email_n_phone_no_extractor(self):
        if self.clean_header_text :
            text = self.clean_header_text
        else:
            text = self.raw_resume_text

        results = {
        "emails": []
        }

        if not text:
            return results

        phones = self.extract_and_validate_phones(text)
        if not phones:
            phones = self.extract_and_validate_phones(self.raw_resume_text)
        results["phone_numbers"] = phones

        # 1. Email Extraction
        # Handles standard formats and prevents capturing trailing punctuation
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)

        if not emails:
            emails = re.findall(email_pattern, self.raw_resume_text)

        results["emails"] = list(set(email.lower() for email in emails))
         
        return results

    def extract_name_and_location_with_gemma(self,input_text, ollama_base_url: str = "http://localhost:11434") -> Dict[str, Optional[str]]:

        # System prompt to ensure JSON output only
        system_prompt = """You are an expert resume parser. Your task is to extract ONLY the candidate's name and location from the provided header text.

        IMPORTANT RULES:
        1. Return ONLY a valid JSON object with NO additional text
        2. Do NOT include markdown formatting, code blocks, or explanations
        3. The JSON must have exactly these keys: "candidate_name" and "location"
        4. If candidate_name is not found, set it to null
        5. If location is not found, set it to null
        6. candidate_name should be a string like "harsh jatav"
        7. location should be a string like "india, rajasthan"
        8. Respond with ONLY the JSON object, nothing else

        Example response format:
        {"candidate_name": "harsh jatav", "location": "india, rajasthan"}"""

        # Prepare the message
        user_message = f"Extract the candidate's name and location from this header text:\n\n{input_text}"

        try:
            # Call Ollama API with Gemma 2:2B
            response = requests.post(
                f"{ollama_base_url}/api/generate",
                json={
                    "model": "gemma2:2b",
                    "prompt": f"{system_prompt}\n\n{user_message}",
                    "stream": False,
                    "temperature": 0.1,  # Low temperature for consistent JSON output
                },
                timeout=60
            )
            response.raise_for_status()
            
            # Extract the response text
            result = response.json()
            model_output = result.get("response", "").strip()
            
            # Try to extract JSON from the response
            # Sometimes the model might include extra text, so we'll try to find the JSON
            extracted_data = self._extract_json_from_response(model_output)
            
            return extracted_data
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Cannot connect to Ollama service. "
                "Make sure Ollama is running at {} and has gemma2:2b model loaded.".format(ollama_base_url)
            )
        except requests.exceptions.Timeout:
            raise TimeoutError("Ollama API request timed out")
        except Exception as e:
            raise Exception(f"Error calling Gemma model: {str(e)}")

    def _extract_json_from_response(self, response_text: str) -> Dict[str, Optional[str]]:
        """
        Extracts valid JSON from model response, handling cases where extra text is included.
        
        Args:
            response_text: Raw text response from the model
        
        Returns:
            Dictionary with 'candidate_name' and 'location' keys
        """
        # Try direct JSON parsing first
        try:
            data = json.loads(response_text)
            return {
                "candidate_name": data.get("candidate_name"),
                "location": data.get("location")
            }
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response
        import re
        json_match = re.search(r'\{[^{}]*"candidate_name"[^{}]*"location"[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return {
                    "candidate_name": data.get("candidate_name"),
                    "location": data.get("location")
                }
            except json.JSONDecodeError:
                pass
        
        # If all parsing fails, return None values
        return {
            "candidate_name": None,
            "location": None
        }

    def candidate_personal_info(self):

        candidate_name_location = self.extract_name_and_location_with_gemma(self.raw_header_text)
        if not candidate_name_location.get("candidate_name","") or not candidate_name_location.get("location",""):
            candidate_name_location = self.extract_name_and_location_with_gemma(self.raw_resume_text)
        candidate_name = candidate_name_location.get("candidate_name","")
        candidate_location = candidate_name_location.get("location","")

        candidate_emails_phones = self.email_n_phone_no_extractor()
        candidate_phones = candidate_emails_phones.get("phone_numbers","")
        candidate_emails = candidate_emails_phones.get("emails","")
        return {
            "candidate_name":candidate_name,
            "location":candidate_location,
            "emails":candidate_emails,
            "phone_numbers":candidate_phones
        }
 
# output = CandidateAttributesExtractionEngine(raw_header_text , raw_resume_text)
# print(output.email_n_phone_no_extractor())
# 
# Example usage for name and location extraction:
output = CandidateAttributesExtractionEngine(raw_header_text, raw_resume_text)
personal_info = output.candidate_personal_info()
print(personal_info)
        
