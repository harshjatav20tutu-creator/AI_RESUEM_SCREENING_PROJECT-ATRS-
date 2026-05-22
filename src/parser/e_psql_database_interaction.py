
import psycopg2
from psycopg2 import sql, Error
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_interaction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseInteraction:

    def __init__(self, normalized_candidate_attributes: dict):
        self.normalized_candidate_attributes = normalized_candidate_attributes
        self.connection = None
        self.candidate_id = None
        
        # Database connection parameters
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'resume_screening_db',
            'user': 'postgres',
            'password': 'harsh2022'
        }

    def connect_to_database(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            logger.info("Successfully connected to PostgreSQL database")
            return True
        except Error as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            return False

    def disconnect_database(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def insert_candidate_info(self):
        """Insert candidate basic information"""
        try:
            cursor = self.connection.cursor()
            
            candidate_info = self.normalized_candidate_attributes.get('candidate_info', {})
            summary = self.normalized_candidate_attributes.get('summary', {})
            experience = self.normalized_candidate_attributes.get('experience_metrics', {})
            
            name = candidate_info.get('name', 'Unknown')
            location = candidate_info.get('location', '')
            professional_title = summary.get('professional_title', '')
            short_bio = summary.get('short_bio', '')
            total_years_experience = experience.get('total_years_experience', 0)
            calculated_months = experience.get('calculated_months', 0)
            
            insert_query = """
            INSERT INTO candidates (name, location, professional_title, short_bio, 
                                   total_years_experience, calculated_months)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING candidate_id;
            """
            
            cursor.execute(insert_query, (name, location, professional_title, short_bio, 
                                         total_years_experience, calculated_months))
            
            self.candidate_id = cursor.fetchone()[0]
            self.connection.commit()
            logger.info(f"Candidate '{name}' inserted with ID: {self.candidate_id}")
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Error inserting candidate info: {e}")
            self.connection.rollback()
            return False

    def insert_contact_info(self):
        """Insert contact information (emails and phone numbers)"""
        try:
            if not self.candidate_id:
                logger.warning("Candidate ID not set, skipping contact info insertion")
                return False
            
            cursor = self.connection.cursor()
            candidate_info = self.normalized_candidate_attributes.get('candidate_info', {})
            
            # Insert emails
            emails = candidate_info.get('emails', [])
            if emails:
                for email in emails:
                    if email:  # Skip empty strings
                        insert_query = """
                        INSERT INTO contact_info (candidate_id, email, phone_number)
                        VALUES (%s, %s, NULL);
                        """
                        cursor.execute(insert_query, (self.candidate_id, email))
                        logger.info(f"Email '{email}' inserted for candidate {self.candidate_id}")
            
            # Insert phone numbers
            phone_numbers = candidate_info.get('phone_numbers', [])
            if phone_numbers:
                for phone in phone_numbers:
                    if phone:  # Skip empty strings
                        insert_query = """
                        INSERT INTO contact_info (candidate_id, email, phone_number)
                        VALUES (%s, NULL, %s);
                        """
                        cursor.execute(insert_query, (self.candidate_id, phone))
                        logger.info(f"Phone '{phone}' inserted for candidate {self.candidate_id}")
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Error inserting contact info: {e}")
            self.connection.rollback()
            return False

    def insert_normalized_skills(self):
        """Insert normalized skills"""
        try:
            if not self.candidate_id:
                logger.warning("Candidate ID not set, skipping skills insertion")
                return False
            
            cursor = self.connection.cursor()
            skills = self.normalized_candidate_attributes.get('normalized_skills', [])
            
            if not skills:
                logger.info("No skills to insert")
                return True
            
            for skill in skills:
                if skill:  # Skip empty strings
                    insert_query = """
                    INSERT INTO normalized_skills (candidate_id, skill_name)
                    VALUES (%s, %s);
                    """
                    cursor.execute(insert_query, (self.candidate_id, skill))
            
            self.connection.commit()
            logger.info(f"Inserted {len(skills)} skills for candidate {self.candidate_id}")
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Error inserting skills: {e}")
            self.connection.rollback()
            return False

    def insert_work_history(self):
        """Insert work history and key achievements"""
        try:
            if not self.candidate_id:
                logger.warning("Candidate ID not set, skipping work history insertion")
                return False
            
            cursor = self.connection.cursor()
            work_history = self.normalized_candidate_attributes.get('work_history', [])
            
            if not work_history:
                logger.info("No work history to insert")
                return True
            
            for job in work_history:
                title = job.get('title', '')
                company = job.get('company', '')
                duration = job.get('duration', '')
                is_current = job.get('is_current', False)
                achievements = job.get('key_achievements', [])
                
                # Insert work history record
                work_query = """
                INSERT INTO work_history (candidate_id, title, company, duration, is_current)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING experience_id;
                """
                
                cursor.execute(work_query, (self.candidate_id, title, company, duration, is_current))
                experience_id = cursor.fetchone()[0]
                logger.info(f"Work history '{title}' at '{company}' inserted with ID: {experience_id}")
                
                # Insert key achievements
                if achievements:
                    for achievement in achievements:
                        if achievement:  # Skip empty strings
                            achievement_query = """
                            INSERT INTO key_achievements (experience_id, achievement_text)
                            VALUES (%s, %s);
                            """
                            cursor.execute(achievement_query, (experience_id, achievement))
                    logger.info(f"Inserted {len(achievements)} achievements for job {experience_id}")
            
            self.connection.commit()
            logger.info(f"Inserted {len(work_history)} work history records for candidate {self.candidate_id}")
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Error inserting work history: {e}")
            self.connection.rollback()
            return False

    def insert_education(self):
        """Insert education information"""
        try:
            if not self.candidate_id:
                logger.warning("Candidate ID not set, skipping education insertion")
                return False
            
            cursor = self.connection.cursor()
            education = self.normalized_candidate_attributes.get('education', {})
            
            if not education:
                logger.info("No education info to insert")
                return True
            
            highest_degree = education.get('highest_degree_level', '')
            institution = education.get('institution', '')
            degree_name = education.get('degree_name', '')
            graduation_year = education.get('graduation_year', None)
            
            insert_query = """
            INSERT INTO education (candidate_id, highest_degree_level, institution, 
                                  degree_name, graduation_year)
            VALUES (%s, %s, %s, %s, %s);
            """
            
            cursor.execute(insert_query, (self.candidate_id, highest_degree, institution, 
                                         degree_name, graduation_year))
            
            self.connection.commit()
            logger.info(f"Education '{degree_name}' from '{institution}' inserted for candidate {self.candidate_id}")
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Error inserting education: {e}")
            self.connection.rollback()
            return False

    def insert_quantifiable_achievements(self):
        """Insert quantifiable achievements metadata"""
        try:
            if not self.candidate_id:
                logger.warning("Candidate ID not set, skipping quantifiable achievements insertion")
                return False
            
            cursor = self.connection.cursor()
            metadata = self.normalized_candidate_attributes.get('metadata', {})
            achievements = metadata.get('quantifiable_achievements', [])
            
            if not achievements:
                logger.info("No quantifiable achievements to insert")
                return True
            
            for achievement in achievements:
                if achievement:  # Skip empty strings
                    insert_query = """
                    INSERT INTO quantifiable_achievements (candidate_id, achievement_metric)
                    VALUES (%s, %s);
                    """
                    cursor.execute(insert_query, (self.candidate_id, achievement))
            
            self.connection.commit()
            logger.info(f"Inserted {len(achievements)} quantifiable achievements for candidate {self.candidate_id}")
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Error inserting quantifiable achievements: {e}")
            self.connection.rollback()
            return False

    def store_to_database(self):
        """Main method to store all candidate data to database"""
        try:
            logger.info("Starting database storage process...")
            
            # Connect to database
            if not self.connect_to_database():
                return False
            
            # Insert all data in order
            if not self.insert_candidate_info():
                self.disconnect_database()
                return False
            
            if not self.insert_contact_info():
                logger.warning("Contact info insertion failed, continuing...")
            
            if not self.insert_normalized_skills():
                logger.warning("Skills insertion failed, continuing...")
            
            if not self.insert_work_history():
                logger.warning("Work history insertion failed, continuing...")
            
            if not self.insert_education():
                logger.warning("Education insertion failed, continuing...")
            
            if not self.insert_quantifiable_achievements():
                logger.warning("Quantifiable achievements insertion failed, continuing...")
            
            logger.info(f"Successfully stored all data for candidate {self.candidate_id}")
            self.disconnect_database()
            return True
            
        except Exception as e:
            logger.error(f"Unexpected error in store_to_database: {e}")
            self.disconnect_database()
            return False

    def retrieve_candidates_for_matching(self):
        """
        Retrieve all candidates with their normalized skills and total experience.
        Returns a list of candidates in the format:
        [
            {
                "candidate_id": 1,
                "normalized_skills": ["python", "java", "react"],
                "total_years_experience": 7.0
            },
            ...
        ]
        """
        try:
            if not self.connect_to_database():
                return []
            
            cursor = self.connection.cursor()
            
            # SQL query to retrieve candidates with aggregated skills
            retrieve_query = """
            SELECT 
                c.candidate_id,
                c.total_years_experience,
                ARRAY_AGG(ns.skill_name) FILTER (WHERE ns.skill_name IS NOT NULL) as normalized_skills
            FROM candidates c
            LEFT JOIN normalized_skills ns ON c.candidate_id = ns.candidate_id
            GROUP BY c.candidate_id, c.total_years_experience
            ORDER BY c.candidate_id;
            """
            
            cursor.execute(retrieve_query)
            rows = cursor.fetchall()
            
            candidates_list = []
            for row in rows:
                candidate_id, total_years_experience, skills = row
                
                # Handle NULL skills array
                normalized_skills = skills if skills else []
                
                candidate_record = {
                    "candidate_id": candidate_id,
                    "normalized_skills": normalized_skills,
                    "total_years_experience": total_years_experience
                }
                candidates_list.append(candidate_record)
            
            logger.info(f"Retrieved {len(candidates_list)} candidates for matching")
            cursor.close()
            self.disconnect_database()
            return candidates_list
            
        except Error as e:
            logger.error(f"Error retrieving candidates: {e}")
            self.disconnect_database()
            return []
    



# candidate_data = {
#         "candidate_info": {
#             "name": "Aiden Williams",
#             "location": "Austin, Texas",
#             "emails": [],
#             "phone_numbers": []
#         },
#         "summary": {
#             "professional_title": "principal software engineer",
#             "short_bio": "results-driven principal software engineer with over 9 years of experience designing scalable full-stack architectures and driving cloud adoption."
#         },
#         "normalized_skills": [
#             "full-stack development",
#             "react_js",
#             "vue_js",
#             "cloud & system architecture",
#             "api design",
#             "docker",
#             "relational database modeling",
#             "engineering strategy",
#             "graphql",
#             "agile/scrum management",
#             "aws",
#             "distributed systems design",
#             "code reviews",
#             "nosql database modeling",
#             "secure coding practices",
#             "performance tuning",
#             "infrastructure as code",
#             "node_js",
#             "cloud technologies",
#             "ci/cd pipeline optimization",
#             "azure",
#             "kubernetes",
#             "team mentorship",
#             "rest",
#             "microservices architecture",
#             "technical leadership",
#             "cross-functional collaboration",
#             "javascript",
#             "terraform",
#             "software architecture"
#         ],
#         "experience_metrics": {
#             "total_years_experience": 7.0,
#             "calculated_months": 84
#         },
#         "work_history": [
#             {
#                 "title": "Lead Software Engineer",
#                 "company": "Google LLC",
#                 "duration": "01/2023 - current",
#                 "is_current": True,
#                 "key_achievements": [
#                     "Architected and implemented a new microservices-oriented architecture that improved system resilience and scalability, enabling an annual growth rate of 20%.",
#                     "Collaborated with product management to develop a roadmap that synchronized engineering efforts with business goals, leading to a software delivery cycle 25% faster.",
#                     " Conducted comprehensive code reviews and integrated optimized coding practices which led to a 15% reduction in application defects."
#                 ]
#             },
#             {
#                 "title": "Software Engineer",
#                 "company": "Amazon Web Services",
#                 "duration": "4 years",
#                 "is_current": False,
#                 "key_achievements": []
#             }
#         ],
#         "education": {
#             "highest_degree_level": "Master",
#             "institution": "University of Texas at Austin",
#             "degree_name": "MS in Computer Science",
#             "graduation_year": 2014
#         },
#         "metadata": {
#             "quantifiable_achievements": [
#                 "30% reduction in latency",
#                 "accommodating 1m concurrent users",
#                 "50% increase in customer engagement",
#                 "60% processing time reduction",
#                 "40% team performance increase",
#                 "six-month reduction in project delivery times"
#             ]
#         }
# }

# output = DatabaseInteraction(candidate_data)
# print(output.retrieve_candidates_for_matching())