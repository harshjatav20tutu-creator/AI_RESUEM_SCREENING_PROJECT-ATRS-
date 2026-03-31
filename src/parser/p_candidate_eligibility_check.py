from typing import List

class CandidateProfile:

    def __init__(self,candidate_skills:List[str], total_experience:float,
                 maximum_experience:float, candidate_degree_level:List[str],
                 candidate_location:str, candidate_work_authorization:str):
        
        self.candidate_skills = candidate_skills
        self.total_experience = total_experience
        self.maximum_experience = maximum_experience
        self.candidate_degree_level = candidate_degree_level
        self.candidate_location = candidate_location
        self.candidate_work_authorization = candidate_work_authorization

class JDRequirements:

    def __init__(self, must_skills:List[str], minimum_experience:float|None,
                 degree_requirement:bool, degree_levels:List[str],
                 degree_fields:List[str], work_mode:str|None,
                 work_location:List[str] , work_authorization:str , sponsorship:str|bool):
        
        self.must_skills = must_skills
        self.minimum_experience = minimum_experience 
        self.degree_requirement = degree_requirement 
        self.degree_levels = degree_levels 
        self.degree_fields = degree_fields
        self.work_mode = work_mode
        self.work_location = work_location
        self.work_authorization = work_authorization
        self.sponsorship = sponsorship


    
        
  
        

