import json
import re
from typing import List, Dict, Optional
from datetime import date


class SkillNormalizationEngine:

    def __init__(self, canonical_json_path:str, candidate_attributes:dict=None, job_requirements:dict=None):
        self.canonical_json_path = canonical_json_path
        self.canonical_database = self._load_canonical_database(canonical_json_path)
        self.canonical_map = self.canonical_database.get("canonical_map", {})
        self.candidate_attributes = candidate_attributes or {}
        self.job_requirements = job_requirements or {}

    def _load_canonical_database(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Initialization Error: Failed to load canonical database from {path}. Error: {e}")
            return {}
    
    def _normalize_skill(self, skill: str) -> str:
        """
        Normalize a single skill using the canonical map.
        If match found (case-insensitive), return canonical form.
        Otherwise, lowercase and strip whitespace.
        """
        if not skill or not isinstance(skill, str):
            return ""
        
        # Try to match in canonical_map (case-insensitive)
        skill_lower = skill.lower().strip()
        
        for key, value in self.canonical_map.items():
            if key.lower() == skill_lower:
                return value
        
        # If no match, return normalized (lowercase, stripped)
        return skill_lower
    
    def _parse_duration_to_years(self, duration_str: str) -> float:
        """
        Parse duration string and return total years as a float (1 decimal precision).
        Handles formats like:
        - "2021 - Present" or "2021 - Current"
        - "2 years 3 months"
        - "1.5 Years"
        - "Jan 2021 - Dec 2023"
        Uses datetime.date.today() to anchor "Present" to current year dynamically.
        """
        if not duration_str or not isinstance(duration_str, str):
            return 0.0
        
        duration_str = duration_str.strip()
        current_year = date.today().year
        
        # Pattern 1: Handle "X years Y months" format
        years_months_pattern = r'(\d+)\s*years?\s+(\d+)\s*months?'
        years_months_match = re.search(years_months_pattern, duration_str, re.IGNORECASE)
        if years_months_match:
            years = int(years_months_match.group(1))
            months = int(years_months_match.group(2))
            return round(years + (months / 12.0), 1)
        
        # Pattern 2: Handle plain "X years" format
        years_only_pattern = r'(\d+(?:\.\d+)?)\s*years?'
        years_only_match = re.search(years_only_pattern, duration_str, re.IGNORECASE)
        if years_only_match:
            years = float(years_only_match.group(1))
            return round(years, 1)
        
        # Pattern 3: Handle plain "X months" format
        months_only_pattern = r'(\d+(?:\.\d+)?)\s*months?'
        months_only_match = re.search(months_only_pattern, duration_str, re.IGNORECASE)
        if months_only_match:
            months = float(months_only_match.group(1))
            return round(months / 12.0, 1)
        
        # Pattern 4: Handle year ranges like "2021 - Present" or "2021 - 2023"
        duration_lower = duration_str.lower()
        year_pattern = r'\b(19\d{2}|20\d{2})\b'
        years = re.findall(year_pattern, duration_str)
        
        if years:
            start_year = int(years[0])
            
            # Check for "present" or "current" keyword
            if "present" in duration_lower or "current" in duration_lower:
                end_year = current_year
            elif len(years) >= 2:
                end_year = int(years[-1])
            else:
                # Only one year found, assume 1 year duration
                end_year = start_year + 1
            
            duration_years = end_year - start_year
            return round(float(duration_years), 1)
        
        # Default: return 0 if no recognizable pattern found
        return 0.0
    
    def _extract_all_skills(self) -> List[str]:
        """
        Extract skills from ALL sections in candidate_attributes.
        Combines: skills (all categories) + other_attributes.additional_skills + any other skill mentions
        Returns a flat list of all skills.
        """
        all_skills = []
        
        # Extract from skills section (all 5 categories)
        skills_section = self.candidate_attributes.get("skills", {})
        if isinstance(skills_section, dict):
            for category in ["programming_languages", "frameworks", "tools", "soft_skills", "other_skills"]:
                skills_list = skills_section.get(category, [])
                if isinstance(skills_list, list):
                    all_skills.extend(skills_list)
        
        # Extract from other_attributes.additional_skills
        other_attributes = self.candidate_attributes.get("other_attributes", {})
        if isinstance(other_attributes, dict):
            additional_skills = other_attributes.get("additional_skills", [])
            if isinstance(additional_skills, list):
                all_skills.extend(additional_skills)
        
        return all_skills
    
    def _calculate_total_years_experience(self) -> float:
        """
        Calculate total years of experience from current_role and past_roles.
        - current_role: Parse "duration" if available, else use "years_in_role", else 0
        - past_roles: Use "years" field directly (already calculated)
        Uses datetime to anchor "Present"/"Current" to current year dynamically.
        Returns float rounded to 1 decimal place.
        """
        total_years = 0.0
        
        # Get experience section
        experience = self.candidate_attributes.get("experience", {})
        
        # Calculate current_role experience
        current_role = experience.get("current_role", {})
        if isinstance(current_role, dict):
            # Try parsing duration first
            if "duration" in current_role:
                duration = current_role.get("duration", "")
                total_years += self._parse_duration_to_years(str(duration))
            # Fallback to years_in_role if duration not available
            elif "years_in_role" in current_role:
                years_in_role = current_role.get("years_in_role")
                if isinstance(years_in_role, (int, float)):
                    total_years += float(years_in_role)
            # else: current_role contributes 0 years
        
        # Calculate past_roles experience (use "years" field directly)
        past_roles = experience.get("past_roles", [])
        if isinstance(past_roles, list):
            for role in past_roles:
                if isinstance(role, dict) and "years" in role:
                    years = role.get("years")
                    if isinstance(years, (int, float)):
                        total_years += float(years)
        
        # Round to 1 decimal place
        return round(total_years, 1)
    
    def candidate_attributes_normalizer(self) -> Dict:
        """
        Normalize candidate attributes: skills and calculate total years of experience.
        - Extracts skills from ALL sections (skills + other_attributes.additional_skills)
        - Combines, deduplicates, lowercases, and normalizes via canonical_map
        - Calculates experience from current_role and past_roles
        - Stores results in self.normalized_attributes and returns it
        
        Returns:
            {
                "normalized_skills": ["javascript", "python", "react", "aws", ...],
                "total_years_experience": 12.0
            }
        """
        # Extract all skills from multiple sections
        all_skills = self._extract_all_skills()
        
        # Lowercase and deduplicate (case-insensitive)
        lowercased_skills = set()
        for skill in all_skills:
            if skill and isinstance(skill, str):
                lowercased_skills.add(skill.lower().strip())
        
        # Normalize each skill via canonical_map
        normalized_skills = []
        for skill in lowercased_skills:
            normalized = self._normalize_skill(skill)
            if normalized and normalized not in normalized_skills:
                normalized_skills.append(normalized)
        
        # Calculate total years of experience
        total_years_experience = self._calculate_total_years_experience()
        
        # Store in self.normalized_attributes
        self.normalized_attributes = {
            "normalized_skills": normalized_skills,
            "total_years_experience": total_years_experience
        }
        
        return self.normalized_attributes

    # main output for database 
    def final_candidate_attributes_to_database(self) -> Dict:
        """
        Construct the final normalized candidate attributes database entry.
        Combines personal info, normalized skills, experience metrics, work history, education, and metadata.
        Calculates calculated_months from total_years_experience.
        
        Returns the complete candidate profile in standardized format:
        {
            "candidate_info": {...},
            "summary": {...},
            "normalized_skills": [...],
            "experience_metrics": {...},
            "work_history": [...],
            "education": {...},
            "metadata": {...}
        }
        """
        # Get normalized attributes (skills and experience)
        normalized_attrs = self.candidate_attributes_normalizer()
        normalized_skills = normalized_attrs.get("normalized_skills", [])
        total_years_experience = normalized_attrs.get("total_years_experience", 0.0)
        
        # Calculate months from years
        calculated_months = round(total_years_experience * 12)
        
        # Extract candidate info from personal_info
        personal_info = self.candidate_attributes.get("personal_info", {})
        candidate_info = {
            "name": personal_info.get("candidate_name", ""),
            "location": personal_info.get("location", ""),
            "emails": personal_info.get("emails", []),
            "phone_numbers": personal_info.get("phone_numbers", [])
        }
        
        # Extract summary
        summary_section = self.candidate_attributes.get("summary", {})
        summary = {
            "professional_title": summary_section.get("professional_title", ""),
            "short_bio": summary_section.get("short_bio", "")
        }
        
        # Experience metrics
        experience_metrics = {
            "total_years_experience": total_years_experience,
            "calculated_months": calculated_months
        }
        
        # Build work history from current_role and past_roles
        work_history = []
        experience = self.candidate_attributes.get("experience", {})
        
        # Add current role
        current_role = experience.get("current_role", {})
        if isinstance(current_role, dict) and current_role:
            current_role_entry = {
                "title": current_role.get("title", ""),
                "company": current_role.get("company", ""),
                "duration": current_role.get("duration", ""),
                "is_current": True,
                "key_achievements": current_role.get("key_achievements", [])
            }
            work_history.append(current_role_entry)
        
        # Add past roles
        past_roles = experience.get("past_roles", [])
        if isinstance(past_roles, list):
            for role in past_roles:
                if isinstance(role, dict):
                    years = role.get("years")
                    # Format duration string from years
                    duration_str = f"{years} years" if isinstance(years, (int, float)) else str(role.get("duration", ""))
                    
                    past_role_entry = {
                        "title": role.get("title", ""),
                        "company": role.get("company", ""),
                        "duration": duration_str,
                        "is_current": False,
                        "key_achievements": role.get("key_achievements", [])
                    }
                    work_history.append(past_role_entry)
        
        # Extract education
        education_section = self.candidate_attributes.get("education", {})
        education_data = education_section.get("education", {}) if isinstance(education_section, dict) else {}
        education = {
            "highest_degree_level": education_data.get("highest_degree_level", ""),
            "institution": education_data.get("institution", ""),
            "degree_name": education_data.get("degree_name", ""),
            "graduation_year": education_data.get("graduation_year", "")
        }
        
        # Extract metadata with quantifiable achievements
        other_attributes = self.candidate_attributes.get("other_attributes", {})
        metadata = {
            "quantifiable_achievements": other_attributes.get("achievements", []) if isinstance(other_attributes, dict) else []
        }
        
        # Construct final output
        self.normalized_attributes = {
            "candidate_info": candidate_info,
            "summary": summary,
            "normalized_skills": normalized_skills,
            "experience_metrics": experience_metrics,
            "work_history": work_history,
            "education": education,
            "metadata": metadata
        }
        
        return self.normalized_attributes
    
    def job_requirements_normalizer(self):
        """
        Normalize job requirements: normalize mandatory_skills and clean other fields.
        - Normalizes mandatory_skills via canonical_map (rename to normalized_mandatory_skills)
        - For all other fields: lowercase and strip strings, keep other values as is
        - Returns the normalized job requirements in the same structure
        
        Returns:
            {
                "job_title": "ai engineer",
                "min_years_experience": 2,
                "work_mode": "unspecified",
                "location": None,
                "normalized_mandatory_skills": ["python", "tensorflow", ...],
                "preferred_skills": ["prompt engineering", ...],
                "role_responsibilities": "..."
            }
        """
        if not self.job_requirements or not isinstance(self.job_requirements, dict):
            return {}
        
        # Create a copy to avoid modifying the original
        normalized_requirements = {}
        
        for key, value in self.job_requirements.items():
            if key == "mandatory_skills":
                # Normalize mandatory skills and rename to normalized_mandatory_skills
                if isinstance(value, list):
                    normalized_skills = []
                    for skill in value:
                        if skill and isinstance(skill, str):
                            normalized = self._normalize_skill(skill)
                            if normalized and normalized not in normalized_skills:
                                normalized_skills.append(normalized)
                    normalized_requirements["normalized_mandatory_skills"] = normalized_skills
                else:
                    normalized_requirements["normalized_mandatory_skills"] = []
            else:
                # For all other fields: lowercase and strip strings, keep others as is
                if isinstance(value, str):
                    normalized_requirements[key] = value.lower().strip()
                elif isinstance(value, list):
                    # For lists, clean up each string item
                    cleaned_list = []
                    for item in value:
                        if isinstance(item, str):
                            cleaned_list.append(item.lower().strip())
                        else:
                            cleaned_list.append(item)
                    normalized_requirements[key] = cleaned_list
                else:
                    # Keep other types (int, None, dict, etc.) as is
                    normalized_requirements[key] = value
        
        # Store and return
        self.normalized_job_requirements = normalized_requirements
        return self.normalized_job_requirements



