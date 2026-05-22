import re
import phonenumbers
import json
import requests
from typing import Dict, Optional

# # ignore its for testing
# raw_header_text = '''AIDEN 
# WILLIAMS
# Principal Software Engineer | Cloud Technologies | Software
# Architecture | Full-Stack Development
# ​Email aidenwilliams403@gmail.com ​LinkedIn ​Austin, Texas
# phone numbers, my phone number: +91 8094766411 , +44 78787-87878 company:
# CORE COMPETENCIES SUMMARY
# Cloud & System Architecture Results-driven Principal Software Engineer with over 9 years of experience designing scalable
# full-stack architectures and driving cloud adoption. Proven expertise in technical leadership,
# Distributed Systems Design,
# demonstrated by spearheading a critical optimization initiative that reduced processing times
# Microservices Architecture, Cloud-Native
# by 60%. Committed to defining technical vision and fostering a culture of innovation to deliver
# Infrastructure (AWS/Azure), Kubernetes &AIDEN Principal Software Engineer | Cloud Technologies | Software
# ''' 
# # ignore its for testing 
# raw_resume_text = '''AIDEN
# WILLIAMS
# ​Email aidenwilliams403@gmail.com
# CORE COMPETENCIES
# Cloud & System Architecture
# Distributed Systems Design,
# Microservices Architecture, Cloud-Native
# Infrastructure (AWS/Azure), Kubernetes &
# Docker, Infrastructure as Code
# (Terraform).
# Full-Stack Development
# Modern JavaScript (React/Node.js), API
# Design (REST & GraphQL), Relational &
# NoSQL Database Modeling, Performance
# Tuning, Secure Coding Practices
# Technical Leadership
# Engineering Strategy, Team Mentorship &
# Code Reviews, Agile/Scrum Management,
# CI/CD Pipeline Optimization, Cross-
# Functional Collaboration
# KEY ACHIEVEMENTS
# Enhanced System Performance
# Redesigned critical streaming service
# infrastructure, achieving 30% reduction in
# latency and accommodating 1M
# concurrent users.
# Successful Project Delivery
# Led a team that delivered a new cloud-
# based analytics platform, which
# increased customer engagement by 50%
# within the first six months.
# Innovative Product Development
# Spearheaded the development of a
# groundbreaking AI tool that reduced
# processing time by 60%, impacting user
# satisfaction ratings positively.
# Team Leadership and Growth
# Mentored junior engineers, resulting in a
# measurable 40% increase in team
# performance and a six-month reduction in
# project delivery times.

# Powered by
# Principal Software Engineer | Cloud Technologies | Software
# Architecture | Full-Stack Development
# ​Email ​LinkedIn ​Austin, Texas
# SUMMARY
# Results-driven Principal Software Engineer with over 9 years of experience designing scalable
# full-stack architectures and driving cloud adoption. Proven expertise in technical leadership,
# demonstrated by spearheading a critical optimization initiative that reduced processing times
# by 60%. Committed to defining technical vision and fostering a culture of innovation to deliver
# high-performance software solutions.
# EXPERIENCE
# Lead Software Engineer 01/2020 - 10/2023
# Google LLC Austin, Texas
# • Architected and implemented a new microservices-oriented architecture that improved
# system resilience and scalability, enabling an annual growth rate of 20%.
# • Collaborated with product management to develop a roadmap that synchronized
# engineering efforts with business goals, leading to a software delivery cycle 25% faster.
# • Conducted comprehensive code reviews and integrated optimized coding practices which
# led to a 15% reduction in application defects.
# • Played a key role in migrating legacy applications to Azure, reducing infrastructure costs by
# 30% while increasing overall system performance.
# • Facilitated knowledge-sharing sessions that enhanced team expertise in cloud
# technologies, resulting in reduced onboarding time for new employees.
# Software Engineer 01/2016 - 12/2019
# Amazon Web Services Austin, Texas
# • Developed scalable back-end services utilizing AWS, decreasing processing times by 50%
# for high-frequency data inputs.
# • Engineered high-availability applications with a 99.99% uptime guarantee, ensuring
# customer satisfaction and retention principles were upheld.
# • Participated in Agile development sprints and improved team productivity through effective
# use of DevOps practices that shortened release timelines.
# • Integrated advanced AI solutions into existing platforms, yielding a 35% improvement in
# data processing efficiency and user engagement metrics.
# • Authored technical documentation and training guides that improved team workflow and
# elevated operational standards across functions.
# Junior Software Developer 01/2014 - 12/2015
# IBM Austin, Texas
# • Assisted in the development of a cross-platform application framework using Java, which
# increased project versatility and reduced deployment errors.
# • Engaged in rigorous testing and quality assurance practices, leading to a documented
# decrease in bugs post-deployment by 20%.
# • Collaborated closely with senior developers to implement user feedback in software
# enhancements, drastically improving the user experience.
# • Executed daily scrums and contributed to sprint planning meetings, resulting in a team
# culture focused on accountability and continuous delivery.
# • Enhanced existing documentation and implementation guides, improving adoption rates
# among internal teams and reducing support queries substantially.
# EDUCATION
# Master of Science in Computer Science 2014
# University of Texas at Austin Austin, Texas
# www.enhancv.com''' 

# # ignore, its for testing
# resume_sections = {'cleaned_resume_text': '', 'resume_sections': {'skills': 'cloud & system architecture distributed systems design, microservices architecture, cloud-native infrastructure aws/azure , kubernetes & docker, infrastructure as code terraform . full-stack development modern javascript react/node.js , api design rest & graphql , relational & nosql database modeling, performance tuning, secure coding practices technical leadership engineering strategy, team mentorship & code reviews, agile/scrum management, ci/cd pipeline optimization, cross- functional collaboration', 'awards_honors': 'enhanced system performance redesigned critical streaming service infrastructure, achieving 30% reduction in latency and accommodating 1m concurrent users. successful project delivery led a team that delivered a new cloud- based analytics platform, which increased customer engagement by 50% within the first six months. innovative product development spearheaded the development of a groundbreaking ai tool that reduced processing time by 60%, impacting user satisfaction ratings positively. team leadership and growth mentored junior engineers, resulting in a measurable 40% increase in team performance and a six-month reduction in project delivery times. \u200b powered by principal software engineer cloud technologies software architecture full-stack development \u200bemail \u200blinkedin \u200baustin, texas', 'summary': 'results-driven principal software engineer with over 9 years of experience designing scalable full-stack architectures and driving cloud adoption. proven expertise in technical leadership, demonstrated by spearheading a critical optimization initiative that reduced processing times by 60%. committed to defining technical vision and fostering a culture of innovation to deliver high-performance software solutions.', 'experience': 'lead software engineer 01/2020 - 10/2023 google llc austin, texas architected and implemented a new microservices-oriented architecture that improved system resilience and scalability, enabling an annual growth rate of 20%. collaborated with product management to develop a roadmap that synchronized engineering efforts with business goals, leading to a software delivery cycle 25% faster. conducted comprehensive code reviews and integrated optimized coding practices which led to a 15% reduction in application defects. played a key role in migrating legacy applications to azure, reducing infrastructure costs by 30% while increasing overall system performance. facilitated knowledge-sharing sessions that enhanced team expertise in cloud technologies, resulting in reduced onboarding time for new employees. software engineer 01/2016 - 12/2019 amazon web services austin, texas developed scalable back-end services utilizing aws, decreasing processing times by 50% for high-frequency data inputs. engineered high-availability applications with a 99.99% uptime guarantee, ensuring customer satisfaction and retention principles were upheld. participated in agile development sprints and improved team productivity through effective use of devops practices that shortened release timelines. integrated advanced ai solutions into existing platforms, yielding a 35% improvement in data processing efficiency and user engagement metrics. authored technical documentation and training guides that improved team workflow and elevated operational standards across functions. junior software developer 01/2014 - 12/2015 ibm austin, texas assisted in the development of a cross-platform application framework using java, which increased project versatility and reduced deployment errors. engaged in rigorous testing and quality assurance practices, leading to a documented decrease in bugs post-deployment by 20%. collaborated closely with senior developers to implement user feedback in software enhancements, drastically improving the user experience. executed daily scrums and contributed to sprint planning meetings, resulting in a team culture focused on accountability and continuous delivery. enhanced existing documentation and implementation guides, improving adoption rates among internal teams and reducing support queries substantially.', 'education': 'master of science in computer science 2014 university of texas at austin austin, texas www.enhancv.com'}}

class CandidateAttributesExtractionEngine:
    
    def __init__(self,raw_header_text:str, raw_resume_text:str,resume_sections:dict,sec_prompt_config_path:str):
        self.resume_sections = resume_sections.get("resume_sections")
        self.raw_header_text = raw_header_text
        self.clean_header_text = self.header_normalizer(self.raw_header_text)
        self.raw_resume_text = raw_resume_text
        self.prompts_config = self._load_prompts(sec_prompt_config_path)

    def header_normalizer(self,text):
        text = re.sub(r'[\(\[\\{]at[\)\]\\}]', '@', text, flags=re.IGNORECASE)
        text = re.sub(r'[\(\[\\{]dot[\)\]\\}]', '.', text, flags=re.IGNORECASE)
        return text
    
    def _load_prompts(self, path):
        """Helper method to safely load the JSON file once."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Initialization Error: Failed to load prompts from {path}. Error: {e}")
            return {}

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
                timeout=180
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
    
    def candidate_attributes_extractions_from_resume_sections(self, ollama_base_url: str = "http://localhost:11434"):
        """
        Extract candidate attributes from resume sections by sending each section to Gemma model.
        
        Process:
        1. Loop through resume sections
        2. Get prompt config for each section (if available)
        3. Send section text to Gemma model one by one
        4. Collect responses in a dictionary
        5. Handle sections not in config by accumulating them
        6. Extract useful info from miscellaneous sections at the end
        
        Args:
            ollama_base_url: URL where Ollama service is running
            
        Returns:
            Dictionary containing extracted attributes for all sections
        """
        extracted_attributes = {}

        candi_personal_info = self.candidate_personal_info()
        extracted_attributes["personal_info"] = candi_personal_info

        other_sections = []  # List to accumulate sections not in config
        
        if not self.resume_sections:
            return extracted_attributes
        
        # Loop through each resume section
        for section_name, section_text in self.resume_sections.items():
            if not section_text or not isinstance(section_text, str):
                continue
            
            # Check if this section has a config/prompt available
            if section_name in self.prompts_config:
                prompt_config = self.prompts_config[section_name]
                
                # Build the prompt for this section
                system_prompt = f"""You are an expert resume parser specialized in extracting structured information.
                Your task is to {prompt_config.get('task', '')}.

                IMPORTANT RULES:
                1. Return ONLY a valid JSON object with NO additional text
                2. Do NOT include markdown formatting, code blocks, or explanations
                3. Follow the provided schema exactly
                4. Use null for missing fields
                5. Respond with ONLY the JSON object, nothing else

                Schema to follow:
                {json.dumps(prompt_config.get('schema', {}), indent=2)}

                Example of expected output format:
                {json.dumps(prompt_config.get('example', {}).get('output', {}), indent=2)}

                Additional instructions:
                {json.dumps(prompt_config.get('instructions', []), indent=2)}"""
                
                user_message = f"Extract information from this {section_name} text:\n\n{section_text}"
                
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
                        timeout=180
                    )
                    response.raise_for_status()
                    
                    result = response.json()
                    model_output = result.get("response", "").strip()
                    
                    # Extract JSON from response
                    extracted_json = self._extract_json_from_response_flexible(model_output)
                    if extracted_json:
                        extracted_attributes[section_name] = extracted_json
                    else:
                        # If JSON extraction fails, store the raw text
                        extracted_attributes[section_name] = {"raw_response": model_output}
                        
                except requests.exceptions.ConnectionError:
                    print(f"Warning: Cannot connect to Ollama service for section '{section_name}'")
                except requests.exceptions.Timeout:
                    print(f"Warning: Ollama API request timed out for section '{section_name}'")
                except Exception as e:
                    print(f"Error processing section '{section_name}': {str(e)}")
            else:
                # Section not in config, accumulate for later processing
                other_sections.append({
                    "section_name": section_name,
                    "section_text": section_text
                })
        
        # Process miscellaneous sections
        if other_sections:
            other_sections_combined = self._process_other_sections(other_sections, ollama_base_url)
            if other_sections_combined:
                extracted_attributes["other_attributes"] = other_sections_combined
        
        return extracted_attributes
    
    def _extract_json_from_response_flexible(self, response_text: str) -> Optional[Dict]:
        """
        Extracts valid JSON from model response flexibly, handling various JSON structures.
        
        Args:
            response_text: Raw text response from the model
        
        Returns:
            Parsed JSON dictionary or None if extraction fails
        """
        if not response_text:
            return None
        
        # Try direct JSON parsing first
        try:
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return data
            except json.JSONDecodeError:
                pass
        
        # If all parsing fails, return None
        return None
    
    def _process_other_sections(self, other_sections: list, ollama_base_url: str) -> Optional[Dict]:
        """
        Process miscellaneous sections not found in config.
        Combines them and extracts useful information using a general prompt.
        
        Args:
            other_sections: List of dictionaries with section_name and section_text
            ollama_base_url: URL where Ollama service is running
        
        Returns:
            Dictionary containing extracted attributes from other sections
        """
        if not other_sections:
            return None
        
        # Combine all other sections
        combined_text = "\n\n".join([
            f"[{section['section_name']}]\n{section['section_text']}"
            for section in other_sections
        ])
        
        # Build a general prompt for miscellaneous sections
        system_prompt = """You are an expert resume parser specialized in extracting useful information from miscellaneous resume sections.
        
        Your task is to extract ANY useful professional attributes from the provided text that could be relevant to understanding the candidate's qualifications.

        IMPORTANT RULES:
        1. Return ONLY a valid JSON object with NO additional text
        2. Do NOT include markdown formatting, code blocks, or explanations
        3. Extract information in relevant categories
        4. Use null for missing fields
        5. Respond with ONLY the JSON object, nothing else

        Try to categorize information into these possible categories (use what's relevant):
        - certifications: List of certifications found
        - achievements: Notable achievements or awards
        - volunteer_work: Volunteer experience
        - languages: Languages spoken
        - publications: Published works or research
        - additional_skills: Any additional skills mentioned
        - professional_memberships: Professional memberships or associations
        - other_details: Any other relevant professional information

        Example output format:
        {
        "achievements": ["Employee of the month", "Led innovation project"],
        "volunteer_work": ["Tech mentor at youth program"],
        "languages": ["English", "Spanish"],
        "publications": ["Published paper on AI"],
        "additional_skills": ["Public speaking", "Project management"],
        "professional_memberships": ["IEEE Member"],
        "other_details": "Any other relevant information"
        }"""
        
        user_message = f"Extract useful professional attributes from these miscellaneous resume sections:\n\n{combined_text}"
        
        try:
            # Call Ollama API with Gemma 2:2B
            response = requests.post(
                f"{ollama_base_url}/api/generate",
                json={
                    "model": "gemma2:2b",
                    "prompt": f"{system_prompt}\n\n{user_message}",
                    "stream": False,
                    "temperature": 0.1,
                },
                timeout=180
            )
            response.raise_for_status()
            
            result = response.json()
            model_output = result.get("response", "").strip()
            
            # Extract JSON from response
            extracted_json = self._extract_json_from_response_flexible(model_output)
            return extracted_json
            
        except requests.exceptions.ConnectionError:
            print("Warning: Cannot connect to Ollama service for processing other sections")
        except requests.exceptions.Timeout:
            print("Warning: Ollama API request timed out for other sections")
        except Exception as e:
            print(f"Error processing other sections: {str(e)}")
        
        return None


        
