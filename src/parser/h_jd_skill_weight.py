
class RankingAndScoringSystem:

    def __init__(self,retrived_candidate_data:list,normalized_job_requirements:dict):
        self.retrived_candidate_data = retrived_candidate_data
        self.job_requirements = normalized_job_requirements
        self.ranked_candidates = []

    def _calculate_skill_match(self, candidate_skills: list, mandatory_skills: list, preferred_skills: list) -> tuple:
        """
        Calculate skill matches and mismatches.
        Returns: (mandatory_matched, mandatory_missing, extra_skills)
        """
        candidate_skills_set = set(candidate_skills) if candidate_skills else set()
        mandatory_set = set(mandatory_skills) if mandatory_skills else set()
        preferred_set = set(preferred_skills) if preferred_skills else set()
        
        # Mandatory skills that candidate has
        mandatory_matched = list(candidate_skills_set & mandatory_set)
        
        # Mandatory skills that candidate is missing
        mandatory_missing = list(mandatory_set - candidate_skills_set)
        
        # Extra skills (candidate has but not in mandatory or preferred)
        combined_job_skills = mandatory_set | preferred_set
        extra_skills = list(candidate_skills_set - combined_job_skills)
        
        return mandatory_matched, mandatory_missing, extra_skills

    def _calculate_score(self, mandatory_matched_count: int, mandatory_total: int, 
                         preferred_matched_count: int, preferred_total: int) -> float:
        """
        Calculate matching score using weighted formula.
        Score = (mandatory_match% × 0.70) + (preferred_match% × 0.30)
        Returns score as a percentage (0-100)
        """
        # Calculate percentages
        mandatory_percentage = (mandatory_matched_count / mandatory_total * 100) if mandatory_total > 0 else 0
        preferred_percentage = (preferred_matched_count / preferred_total * 100) if preferred_total > 0 else 0
        
        # Calculate weighted score
        score = (mandatory_percentage * 0.70) + (preferred_percentage * 0.30)
        return round(score, 2)

    def rank_and_score_candidates(self):
        """
        Rank and score candidates against job requirements.
        - Filters out candidates below minimum experience requirement
        - Calculates skill matches and scoring
        - Returns sorted list (by score descending) with structure:
        [
            {
                'candidate_id': 1,
                'total_years_experience': 7.0,
                'matching_score': '75%',
                'mandatory_matched_skills': [...] or None,
                'mandatory_missing_skills': [...] or None,
                'extra_skills': [...] or None
            },
            ...
        ]
        """
        if not self.retrived_candidate_data or not self.job_requirements:
            return []
        
        min_years_experience = self.job_requirements.get('min_years_experience', 0)
        normalized_mandatory_skills = self.job_requirements.get('normalized_mandatory_skills', [])
        preferred_skills = self.job_requirements.get('preferred_skills', [])
        
        qualified_candidates = []
        
        for candidate in self.retrived_candidate_data:
            candidate_id = candidate.get('candidate_id')
            total_years_experience = candidate.get('total_years_experience', 0)
            candidate_skills = candidate.get('normalized_skills', [])
            
            # Filter: Reject candidates below minimum experience
            if total_years_experience < min_years_experience:
                continue
            
            # Calculate skill matches
            mandatory_matched, mandatory_missing, extra_skills = self._calculate_skill_match(
                candidate_skills, 
                normalized_mandatory_skills, 
                preferred_skills
            )
            
            # Calculate preferred skills match
            preferred_matched = len(set(candidate_skills) & set(preferred_skills)) if candidate_skills and preferred_skills else 0
            
            # Calculate score
            matching_score = self._calculate_score(
                len(mandatory_matched),
                len(normalized_mandatory_skills),
                preferred_matched,
                len(preferred_skills)
            )
            
            # Build candidate record
            candidate_record = {
                'candidate_id': candidate_id,
                'total_years_experience': total_years_experience,
                'matching_score': f"{matching_score}%",
                'mandatory_matched_skills': mandatory_matched if mandatory_matched else None,
                'mandatory_missing_skills': mandatory_missing if mandatory_missing else None,
                'extra_skills': extra_skills if extra_skills else None
            }
            
            qualified_candidates.append(candidate_record)
        
        # Sort by matching_score descending
        self.ranked_candidates = sorted(
            qualified_candidates,
            key=lambda x: float(x['matching_score'].rstrip('%')),
            reverse=True
        )
        
        return self.ranked_candidates

    