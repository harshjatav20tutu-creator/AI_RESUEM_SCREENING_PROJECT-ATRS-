import json


class JDRequirementsNormalizer:

    def __init__(self,canonical_json_path:str,job_requirements:dict):
        self.job_requirements = job_requirements or {}
        self.canonical_database = self._load_canonical_database(canonical_json_path)
        self.canonical_map = self.canonical_database.get("canonical_map", {})

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

# jr = {
#         "job_title": "AI Engineer",
#         "min_years_experience": 2,
#         "work_mode": "Unspecified",
#         "location": None,
#         "mandatory_skills": [
#             "Python",
#             "TensorFlow",
#             "PyTorch",
#             "LLMs",
#             "SLMs",
#             "RAG architectures",
#             "Vector databases (Pinecone, FAISS, Weaviate)",
#             "Agentic AI frameworks (LangGraph, AutoGen, CrewAI)",
#             "Cloud platforms (AWS, Azure, GCP)"
#         ],
#         "preferred_skills": [
#             "Prompt engineering",
#             "Fine-tuning",
#             "RAG-enhanced GenAI models",
#             "Agent-based AI solutions",
#             "Banking/financial domain processes (risk, compliance, KYC, lending, fraud detection)",
#             "AI/ML certifications (AWS AI/ML Specialty, Microsoft AI Engineer, NVIDIA Deep Learning, Generative AI certifications)"
#         ],
#         "role_responsibilities": "Design and implement AI/ML models leveraging LLMs, SLMs, RAG pipelines, and Agentic AI frameworks. Develop end-to-end AI workflows, including data ingestion, preprocessing, model training, fine-tuning, and deployment. Collaborate with data engineers to integrate structured and unstructured banking data securely. Implement and optimize vector databases, embeddings, and retrieval mechanisms. Ensure AI model governance, explainability, and compliance with banking regulations. Work with business and domain experts to translate requirements into AI-driven solutions. Monitor model performance, implement feedback loops, and continuously improve AI systems. Stay updated on emerging AI technologies and frameworks relevant to banking use cases."
# }

# # output = JDRequirementsNormalizer(r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\canonicalization_database.json",jr)
# # print(output.job_requirements_normalizer())