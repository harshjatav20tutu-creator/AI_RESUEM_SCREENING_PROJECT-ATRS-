from typing import Dict, List ,Any


def normalizing_skills_to_canonical(skills_db:Dict[str,List[str]])->Dict[str,str]:
    alias_to_canonical :Dict[str,str] = {}

    for canonical , alias in skills_db.items():
        c = canonical.lower().strip()
        for a in (alias or []):
            a = a.lower().strip()
            if a :
                alias_to_canonical[a] = c
        
    return alias_to_canonical


def resume_scoring(resume_skills:Dict[str,float],job_description_skills:Dict[str,float],skill_db:Dict)-> Dict[str,Any]:
    alias_to_canonical = normalizing_skills_to_canonical(skill_db)

    normalized_r = {}
    normalized_d = {}
    for skill , score in resume_skills.items():
        s = skill.lower().strip()
        if s in alias_to_canonical.keys():
            normalized_r[alias_to_canonical.get(s)] = score
        else:
            normalized_r[s] = score
    for skill , score in job_description_skills.items():
        s = skill.lower().strip()
        if s in alias_to_canonical.keys():
            normalized_d[alias_to_canonical.get(s)] = score
        else:
            normalized_d[s] = score

    penalty_map = {0:1.10, 1:0.90, 2:0.85, 3:0.80}

    extracting_resume_skills = [r for r in normalized_r.keys() if r ]
    extracting_job_des_skills = [d for d in normalized_d.keys() if d]

    # matching 
    matched_skills = set(extracting_job_des_skills).intersection(set(extracting_resume_skills))
    matched_skills = list(matched_skills)

    # missing 
    missing_skills = [skill for skill in extracting_job_des_skills if skill not in matched_skills]

    # extra skills
    extra_skills = [skill for skill in extracting_resume_skills if skill not in matched_skills]

    jd_skill_total_score = sum(normalized_d.values())

    resume_skill_sum_capped = sum([min(normalized_r.get(s,0.0),normalized_d.get(s,0.0)) for s in matched_skills])

    if len(missing_skills) in penalty_map.keys():
        factor = penalty_map.get(len(missing_skills))
    else :
        factor = 0.70

    x = (resume_skill_sum_capped/jd_skill_total_score)* factor
    x = max(0.0,min(1.0,x))
    final_score = x * 100

    return {"score":min(float(f"{final_score:.2f}"),100.00),
            "matched skills": matched_skills,
            "missing skills": missing_skills,
            "extra skills":extra_skills
            }