import streamlit as st
import os
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import classes from parser modules
from src.parser.a_text_extractor_code import ResumeParser
from src.parser.b_resume_segment_engin import ResumeTextNormalizedandSegmentationEngine
from src.parser.c_candidate_info_ext import CandidateAttributesExtractionEngine
from src.parser.d_skills_normalization_engine import SkillNormalizationEngine
from src.parser.e_psql_database_interaction import DatabaseInteraction
from src.parser.f_jd_text_requirement_extraction import JDParser
from src.parser.g_jd_requirements_normalizer import JDRequirementsNormalizer
from src.parser.j_jd_skill_weight import RankingAndScoringSystem

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================
# CANONICAL_DB_PATH = "Data/config/canonicalization_database.json"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB for ~3 page resume
SUPPORTED_FILE_TYPES = ["pdf", "docx"]

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Interface",
    ["Candidate Upload", "HR Dashboard"],
    help="Choose between candidate resume upload or HR screening dashboard"
)

# ============================================================================
# CANDIDATE UPLOAD PAGE
# ============================================================================
if page == "Candidate Upload":
    st.title("📄 Resume Upload Portal")
    
    st.markdown("""
    ---
    ### Welcome, Candidate!
    Upload your resume to be considered for our positions. Our AI-powered system will automatically 
    process and analyze your qualifications.
    """)
    
    # Instructions
    with st.expander("📋 Supported File Formats & Requirements", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Supported Formats:**
            - 📄 PDF (.pdf)
            - 📝 Word Document (.docx)
            """)
        with col2:
            st.markdown("""
            **File Requirements:**
            - Maximum file size: 5 MB
            - Recommended: 1-3 pages
            - Clear formatting preferred
            """)
    
    st.markdown("---")
    
    # Form for candidate upload
    with st.form("candidate_upload_form"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            candidate_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                help="Your name will be used in our system"
            )
        
        with col2:
            st.empty()
        
        # File uploader with drag-and-drop
        uploaded_file = st.file_uploader(
            "Upload Your Resume",
            type=SUPPORTED_FILE_TYPES,
            help="Drag and drop your resume or click to browse"
        )
        
        # Submit button
        submit_button = st.form_submit_button(
            "📤 Upload & Process Resume",
            use_container_width=True
        )
    
    # Process upload
    if submit_button:
        # Validation
        if not candidate_name or candidate_name.strip() == "":
            st.error("❌ Please enter your full name")
        elif uploaded_file is None:
            st.error("❌ Please upload a resume file")
        elif uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"❌ File size exceeds {MAX_FILE_SIZE / (1024*1024):.0f}MB limit")
        else:
            # Process the resume
            with st.spinner("🔄 Processing your resume..."):
                try:
                    # Save uploaded file temporarily
                    temp_file_path = f"temp_{uploaded_file.name}"
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Step 1: Extract text from resume
                    resume_parser = ResumeParser(temp_file_path)
                    extracted_resume_text = resume_parser.resume_text_extractor()
                    resume_header_text = resume_parser.main_header_extractor()
                    
                    # Step 2: Normalize and segment resume text
                    segmentation_engine = ResumeTextNormalizedandSegmentationEngine(raw_resume_text=extracted_resume_text,
                                                                                    section_kw_config_path=r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\resume_sections.json",
                                                                                    extra_headers_config_path=r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\resume_extra_section.json")
                    resume_segments = segmentation_engine.main_resume_segmentation_engin()
                    
                    # Step 3: Extract candidate attributes
                    extraction_engine = CandidateAttributesExtractionEngine(raw_header_text=resume_header_text,
                                                                            raw_resume_text=extracted_resume_text,
                                                                            resume_sections=resume_segments,
                                                                            sec_prompt_config_path=r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\prompts.json")
                    candidate_attributes = extraction_engine.candidate_attributes_extractions_from_resume_sections()
                    
                    # Add candidate name from user input
                    if "personal_info" not in candidate_attributes:
                        candidate_attributes["personal_info"] = {}
                    candidate_attributes["personal_info"]["candidate_name"] = candidate_name.strip()

                    # Step 4: Normalize candidate attributes
                    normalizer = SkillNormalizationEngine(
                        canonical_json_path=r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\canonicalization_database.json",
                        candidate_attributes=candidate_attributes
                    )
                    normalized_attributes = normalizer.final_candidate_attributes_to_database()
                    
                    # Step 5: Store to database
                    db_interaction = DatabaseInteraction(normalized_attributes)
                    db_interaction.store_to_database()
                    
                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    
                    # Success message
                    st.success("✅ Upload Successful!")
                    st.markdown(f"""
                    ---
                    ### Thank You, **{candidate_name.strip()}**!
                    
                    Your resume has been successfully uploaded and processed by our AI system.
                    
                    **What happens next?**
                    - Your profile has been added to our candidate database
                    - Our HR team will evaluate your qualifications
                    - You will be contacted if you match our requirements
                    
                    ---
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Error Processing Resume\n\nDetails: {str(e)}")
                    st.markdown("""
                    **Troubleshooting Tips:**
                    - Ensure your resume is in PDF or DOCX format
                    - Check that the file is not corrupted
                    - Try with a different resume format
                    - Contact support if the issue persists
                    """)

# ============================================================================
# HR DASHBOARD PAGE
# ============================================================================
elif page == "HR Dashboard":
    # 1. Initialize the authentication state variable if it doesn't exist yet
    if "hr_authenticated" not in st.session_state:
        st.session_state.hr_authenticated = False

    # 2. Case A: If HR is NOT logged in, intercept them with the login screen
    if not st.session_state.hr_authenticated:
        st.title("🔒 HR Administration Gateway")
        st.write("Please authenticate to unlock the executive recruitment tools.")
        st.markdown("---")
        
        # Create a clean, contained form for credentials
        with st.form("hr_login_form"):
            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter secure key")
            submit_button = st.form_submit_button("Authenticate")
            
            if submit_button:
                # Use these exact hardcoded credentials during your demo tomorrow
                if username == "admin" and password == "tcs_atrs_2026":
                    st.session_state.hr_authenticated = True
                    st.success("Access Granted! Loading system parameters...")
                    st.rerun()  # Forces Streamlit to instantly redraw the screen
                else:
                    st.error("Invalid Administrative Credentials. Access Denied.")

    # 3. Case B: If HR is successfully authenticated, unlock your actual dashboard panel
    # 4. If the credentials are correct, unlock and render the actual HR Dashboard
    if st.session_state.hr_authenticated:
        st.title("📊 HR Screening Dashboard")
        
        # Logout button in the sidebar
        if st.sidebar.button("🔒 Lock Dashboard"):
            st.session_state.hr_authenticated = False
            st.rerun()
            
        st.markdown("""
        ---
        ### AI-Powered Resume Screening & Ranking System
        Ingest job specifications, parse requirements using LLM engines, and cross-reference records against your active candidate database.
        """)

        # Initialize explicit structural session state registers to prevent screen-refresh data drops
        if "jd_text" not in st.session_state:
            st.session_state.jd_text = None
        if "normalized_jd" not in st.session_state:
            st.session_state.normalized_jd = None
        if "ranking_results" not in st.session_state:
            st.session_state.ranking_results = None

        # -------------------------------------------------------------------------
        # STEP 1: JOB DESCRIPTION INPUT LAYER
        # -------------------------------------------------------------------------
        st.subheader("Step 1: Input Job Specifications")
        
        input_mode = st.radio("Choose Input Method:", ["Paste Text Specification", "Upload Document File (PDF/DOCX)"])
        
        raw_input_source = None
        
        if input_mode == "Paste Text Specification":
            raw_input_source = st.text_area("Paste Raw Job Description here:", height=200, placeholder="Looking for a Senior Dev with 5 years experience in React...")
        else:
            raw_input_source = st.file_uploader("Upload Job Specification Document", type=["pdf", "docx"])

        # Trigger Ingestion Routine
        if st.button("Ingest Job Description"):
            if raw_input_source:
                try:
                    with st.spinner("Processing document layout inputs..."):
                        # Your backend component assignment
                        # Note: If your JDParser expects a saved file path for uploaded files instead of bytes,
                        # ensure raw_input_source is written to a temporary local location first.
                        jd_parser = JDParser(raw_input_source)
                        st.session_state.jd_text = jd_parser.jd_text_extractor()
                        
                    st.success("Job description successfully stored in text buffer!")
                    # Flush down-funnel variables on fresh data ingest to maintain system integrity
                    st.session_state.normalized_jd = None
                    st.session_state.ranking_results = None
                except Exception as e:
                    st.error(f"Ingestion Sequence Failed: {str(e)}")
            else:
                st.warning("Please provide a valid text string or document file path before proceeding.")

        st.markdown("---")

        # -------------------------------------------------------------------------
        # STEP 2: LLM PARSING ENGINE LAYER
        # -------------------------------------------------------------------------
        st.subheader("Step 2: Core Attribute Extraction & Normalization")
        
        # Unlock button only if there is valid data populated inside the session state variable
        jd_parse_disabled = st.session_state.jd_text is None
        
        if st.button("Parse Job Requirements", disabled=jd_parse_disabled):
            try:
                with st.spinner("Executing LLM extraction and structural mapping matrices..."):
                    # Using the exact structural calls defined in your backend spec
                    # Note: Based on your code snippet, your jd_requirements_extraction_engine is called via 'jd_text_extractor' variable.
                    # Ensure that 'jd_text_extractor' is initialized or imported into this module.
                    jd_parser = JDParser(path_or_jdtext=None)
                    jd_requirements_extractor = jd_parser.jd_requirements_extraction_engine(st.session_state.jd_text)
                    
                    jd_normalizer = JDRequirementsNormalizer(
                        canonical_json_path=r"C:\Users\HP\OneDrive\Documents\AI_resume_screening_project\Data\config\canonicalization_database.json", 
                        job_requirements=jd_requirements_extractor
                    )
                    st.session_state.normalized_jd = jd_normalizer.job_requirements_normalizer()
                    
                st.success("Job specification successfully parsed and normalized to taxonomy keys!")
                st.json(st.session_state.normalized_jd) # Displays the clear target criteria to the HR agent
            except Exception as e:
                st.error(f"Parsing Sequence Failed: {str(e)}")

        st.markdown("---")

        # -------------------------------------------------------------------------
        # STEP 3: CANDIDATE RANKING & MATCHING ENGINE
        # -------------------------------------------------------------------------
        st.subheader("Step 3: Executive Scoring Matrix & Leaderboard")
        
        # Unlock button only if requirement extraction has executed successfully
        ranking_disabled = st.session_state.normalized_jd is None
        
        if st.button("Rank Candidates", disabled=ranking_disabled):
            try:
                with st.spinner("Querying database pools and running matching equations..."):
                    # Execute backend retrieval and evaluation
                    db_interaction = DatabaseInteraction(normalized_candidate_attributes=None)
                    retrieved_candidate_data_from_database = db_interaction.retrieve_candidates_for_matching()
                    
                    ranking_engine = RankingAndScoringSystem(
                        retrieved_candidate_data_from_database, 
                        st.session_state.normalized_jd
                    )
                    st.session_state.ranking_results = ranking_engine.rank_and_score_candidates()
                    
                st.success("Leaderboard generated successfully!")
            except Exception as e:
                st.error(f"Ranking Pipeline Failed: {str(e)}")

        # Render Leaderboard Output UI Component if results are present in memory
        if st.session_state.ranking_results:
            st.markdown("### 🏆 Candidate Matching Leaderboard")
            
            for index, candidate in enumerate(st.session_state.ranking_results, 1):
                # Clean look using individual expansion metrics
                with st.expander(f"Rank {index}: Candidate ID {candidate['candidate_id']} — Match Score: {candidate['matching_score']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Total Experience Pool", value=f"{candidate['total_years_experience']} Years")
                    
                    st.markdown("#### Skills Matrix Decomposition")
                    st.write(f"✅ **Matched Mandatory Skills:** {', '.join(candidate['mandatory_matched_skills']) if candidate['mandatory_matched_skills'] else 'None'}")
                    st.write(f"❌ **Missing Mandatory Skills:** {', '.join(candidate['mandatory_missing_skills']) if candidate['mandatory_missing_skills'] else 'None'}")
                    st.write(f"💡 **Extra Value-Add Skills:** {', '.join(candidate['extra_skills']) if candidate['extra_skills'] else 'None'}")
