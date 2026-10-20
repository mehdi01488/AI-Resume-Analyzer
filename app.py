from flask import Flask, render_template, request, redirect
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
<<<<<<< HEAD
from werkzeug.utils import secure_filename
import os
import re
import sqlite3


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATABASE_PATH = os.path.join(BASE_DIR, "resume_analyzer.db")

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def ensure_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            match_score REAL,
            skill_gap REAL,
            career_recommendation TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


ensure_database()

=======
import os
import sqlite3


app = Flask(__name__)


# =========================================================
# Upload Folder
# =========================================================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =========================================================
# Job Description
# =========================================================

JOB_DESCRIPTION = """
Data Analyst job requiring Python SQL Excel Power BI
Pandas NumPy Data Analysis Data Science
"""


# =========================================================
# Required Skills
# =========================================================

REQUIRED_SKILLS = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Pandas",
    "NumPy"
]


# =========================================================
# Calculate Overall Score
# =========================================================

def calculate_overall_score(match_score, skill_gap_percentage):

    skill_score = 100 - skill_gap_percentage

    overall_score = (
        (match_score * 0.60) +
        (skill_score * 0.40)
    )

    return round(overall_score, 2)


# =========================================================
# Save Analysis
# =========================================================
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763

def save_analysis(
    resume_name,
    match_score,
    skill_gap,
    career_recommendation,
    matched_skills,
    missing_skills
):
<<<<<<< HEAD
    connection = get_connection()

    connection.execute("""
        INSERT INTO resume_analysis (
=======

    connection = sqlite3.connect("resume_analyzer.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO resume_analysis
        (
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
            resume_name,
            match_score,
            skill_gap,
            career_recommendation,
            matched_skills,
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        resume_name,
        match_score,
        skill_gap,
        career_recommendation,
<<<<<<< HEAD
        ", ".join(matched_skills),
        ", ".join(missing_skills)
    ))

    connection.commit()
    connection.close()


def calculate_overall_score(match_score, skill_gap):
    skill_score = max(0, 100 - skill_gap)
    return round((match_score * 0.60) + (skill_score * 0.40), 2)


# =========================================================
# CAREER PROFILES
# =========================================================

CAREER_PROFILES = {
    "Data Analyst": {
        "skills": [
            "sql", "excel", "power bi", "tableau", "pandas",
            "data analysis", "data visualization", "statistics",
            "matplotlib", "numpy"
        ],
        "education": [
            "data analytics", "data analysis", "statistics"
        ],
        "projects": [
            "Sales Performance Dashboard using Power BI or Excel",
            "SQL Business Data Analysis",
            "Customer Trends Analysis using Python and Pandas"
        ],
        "roadmap": [
            "Improve SQL, Excel and data visualization.",
            "Build end-to-end analytics projects using real datasets.",
            "After gaining strong analytics experience, explore BI Analyst or Data Scientist roles."
        ]
    },

    "BI Analyst": {
        "skills": [
            "power bi", "tableau", "dax", "sql", "dashboard",
            "data modeling", "excel", "power query"
        ],
        "education": ["business intelligence", "data analytics"],
        "projects": [
            "Interactive Power BI Business Dashboard",
            "Executive KPI Reporting System",
            "SQL Database and BI Reporting Project"
        ],
        "roadmap": [
            "Learn advanced dashboards, data modeling and DAX.",
            "Practice SQL and Power Query with business data.",
            "Progress toward Senior BI Analyst or BI Developer."
        ]
    },

    "Data Scientist": {
        "skills": [
            "python", "pandas", "numpy", "statistics",
            "machine learning", "scikit-learn", "sklearn",
            "data science", "matplotlib", "deep learning"
        ],
        "education": [
            "data science", "statistics", "mathematics"
        ],
        "projects": [
            "Customer Churn Prediction Model",
            "Exploratory Data Analysis and Statistical Report",
            "Machine Learning Price Prediction"
        ],
        "roadmap": [
            "Strengthen Python, statistics and data preparation.",
            "Learn machine learning algorithms and model evaluation.",
            "Build practical projects before applying for junior roles."
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "python", "machine learning", "tensorflow", "pytorch",
            "scikit-learn", "deep learning", "mlops", "model deployment"
        ],
        "education": [
            "artificial intelligence", "machine learning", "computer science"
        ],
        "projects": [
            "Machine Learning Prediction API",
            "Image Classification Application",
            "End-to-End ML Model Deployment"
        ],
        "roadmap": [
            "Strengthen Python and machine learning fundamentals.",
            "Learn APIs, model deployment and software engineering.",
            "Explore production ML and MLOps."
        ]
    },

    "Software Developer": {
        "skills": [
            "python", "java", "c++", "c#", "git", "oop",
            "data structures", "algorithms", "api", "testing",
            "software development"
        ],
        "education": [
            "computer science", "software engineering", "computer engineering"
        ],
        "projects": [
            "Student Management System",
            "REST API with Database Integration",
            "Task Management Application"
        ],
        "roadmap": [
            "Practice programming, data structures and algorithms.",
            "Build applications with databases, testing and Git.",
            "Progress toward backend, frontend or full-stack development."
        ]
    },

    "Web Developer": {
        "skills": [
            "html", "css", "javascript", "react", "flask",
            "django", "node.js", "php", "web development"
        ],
        "education": [
            "computer science", "software engineering", "web development"
        ],
        "projects": [
            "Responsive Portfolio Website",
            "Full-Stack Job Portal",
            "E-commerce Website with Database"
        ],
        "roadmap": [
            "Practice HTML, CSS and JavaScript.",
            "Build responsive applications and learn a backend framework.",
            "Progress toward full-stack development."
        ]
    },

        "Cybersecurity Analyst": {
        "skills": [
            "cybersecurity", "network security", "linux",
            "penetration testing", "siem", "incident response",
            "ethical hacking", "wireshark", "security analysis"
        ],
        "education": [
            "cybersecurity", "information security", "computer science"
        ],
        "projects": [
            "Security Log Analysis Dashboard",
            "Network Security Lab Assessment",
            "Phishing Awareness and Detection Demonstration"
        ],
        "roadmap": [
            "Learn networking, Linux and security fundamentals.",
            "Practice defensive security in authorized lab environments.",
            "Develop incident response and security analysis skills."
        ]
    },

    "Network Administrator": {
        "skills": [
            "networking", "tcp/ip", "routing", "switching", "cisco",
            "ccna", "dns", "dhcp", "firewall", "network administration"
        ],
        "education": [
            "networking", "computer networks", "computer science"
        ],
        "projects": [
            "Small Office Network Design",
            "Network Monitoring Lab",
            "VLAN and Firewall Configuration Lab"
        ],
        "roadmap": [
            "Learn networking fundamentals and troubleshooting.",
            "Practice routing and switching in a lab.",
            "Explore network engineering or cloud networking."
        ]
    },

    "Accountant / Finance Analyst": {
        "skills": [
            "accounting", "bookkeeping", "financial analysis",
            "financial reporting", "excel", "budgeting", "quickbooks",
            "taxation", "financial modeling", "accounts"
        ],
        "education": [
            "accounting", "finance", "commerce", "b.com", "acca", "ca"
        ],
        "projects": [
            "Monthly Financial Reporting Workbook",
            "Budget and Cash Flow Analysis",
            "Financial Performance Dashboard"
        ],
        "roadmap": [
            "Strengthen accounting principles and spreadsheet skills.",
            "Practice financial reporting, budgeting and reconciliation.",
            "Explore financial analysis or accounting specialization."
        ]
    },

    "Digital Marketing Specialist": {
        "skills": [
            "digital marketing", "seo", "sem", "google ads",
            "social media marketing", "content marketing",
            "email marketing", "meta ads", "campaign management"
        ],
        "education": [
            "marketing", "business administration", "mass communication"
        ],
        "projects": [
            "SEO Audit and Keyword Research Report",
            "Social Media Campaign Performance Analysis",
            "Digital Marketing Campaign Plan"
        ],
        "roadmap": [
            "Learn SEO, campaign planning and marketing analytics.",
            "Create portfolio reports with measurable campaign results.",
            "Explore performance marketing or marketing strategy."
        ]
    },

    "UI/UX Designer": {
        "skills": [
            "ui design", "ux design", "figma", "wireframes",
            "prototyping", "user research", "usability testing",
            "adobe xd", "graphic design"
        ],
        "education": [
            "design", "graphic design", "interaction design"
        ],
        "projects": [
            "Mobile App Wireframes and Interactive Prototype",
            "Website Usability Review and Redesign",
            "User Research and Journey Mapping Case Study"
        ],
        "roadmap": [
            "Practice user research, wireframing and prototyping.",
            "Document design decisions in portfolio case studies.",
            "Explore product design or UX research."
        ]
    },

    "Teacher / Educator": {
        "skills": [
            "teaching", "lesson planning", "classroom management",
            "curriculum development", "assessment", "tutoring",
            "educational technology"
        ],
        "education": [
            "education", "b.ed", "m.ed", "teaching", "teacher training"
        ],
        "projects": [
            "Lesson Plan and Learning Outcome Portfolio",
            "Student Assessment and Progress Tracker",
            "Digital Learning Resource for a Subject"
        ],
        "roadmap": [
            "Strengthen subject knowledge and teaching methods.",
            "Prepare lesson plans and assessment samples.",
            "Explore subject specialization or academic coordination."
        ]
    },

    "Healthcare Professional": {
        "skills": [
            "medicine", "patient care", "clinical practice", "nursing",
            "pharmacy", "diagnosis", "public health", "healthcare",
            "physiotherapy", "clinical research"
        ],
        "education": [
            "medicine", "mbbs", "nursing", "pharmacy", "physiotherapy",
            "public health", "health sciences"
        ],
        "projects": [
            "Healthcare Education Resource for Patients",
            "Public Health Awareness Campaign",
            "De-identified Healthcare Data Summary"
        ],
        "roadmap": [
            "Build on your recognized qualification and supervised training.",
            "Document relevant clinical placements and certifications.",
            "Explore a specialization suitable for your qualification and local licensing requirements."
        ]
    },

    "Laboratory Technician": {
        "skills": [
            "laboratory", "lab technician", "sample preparation",
            "microscopy", "quality control", "specimen handling",
            "laboratory safety", "medical laboratory"
        ],
        "education": [
            "medical laboratory technology", "laboratory science",
            "biology", "biotechnology", "chemistry"
        ],
        "projects": [
            "Laboratory Quality Control Checklist",
            "Specimen Tracking Workflow Prototype",
            "Laboratory Safety and SOP Portfolio"
        ],
        "roadmap": [
            "Strengthen laboratory procedures, safety and documentation.",
            "Record supervised practical training and relevant certifications.",
            "Explore specialized laboratory roles appropriate to your qualification."
        ]
    },

    "Engineer": {
        "skills": [
            "engineering", "autocad", "solidworks", "matlab",
            "circuit design", "plc", "cad", "simulation",
            "mechanical design", "electrical design"
        ],
        "education": [
            "engineering", "mechanical engineering",
            "electrical engineering", "civil engineering",
            "chemical engineering"
        ],
        "projects": [
            "Engineering Design and Simulation Report",
            "Technical Drawing and CAD Portfolio",
            "Prototype Design with Testing Results"
        ],
        "roadmap": [
            "Identify the engineering discipline matching your degree.",
            "Build discipline-specific projects and technical documentation.",
            "Explore specialist engineering roles or professional registration."
        ]
    },

    "Business Analyst": {
        "skills": [
            "business analysis", "requirements gathering",
            "process mapping", "stakeholder management", "user stories",
            "sql", "excel", "documentation", "business requirements"
        ],
        "education": [
            "business administration", "business analytics",
            "computer science", "information systems"
        ],
        "projects": [
            "Business Requirements Document",
            "Process Improvement Case Study",
            "Business KPI Dashboard"
        ],
        "roadmap": [
            "Learn requirements gathering and process documentation.",
            "Practice user stories, process maps and stakeholder communication.",
            "Build business analysis case studies and KPI reports."
        ]
    },

    "HR / Recruitment Specialist": {
        "skills": [
            "human resources", "recruitment", "talent acquisition",
            "interviewing", "employee relations", "hr management",
            "payroll", "onboarding"
        ],
        "education": [
            "human resources", "business administration", "management"
        ],
        "projects": [
            "Recruitment Tracking Dashboard",
            "Employee Onboarding Checklist",
            "Candidate Screening Workflow"
        ],
        "roadmap": [
            "Learn recruitment processes and HR documentation.",
            "Practice candidate tracking and interview coordination.",
            "Explore talent acquisition or HR operations."
        ]
    },

    
}


# =========================================================
# CAREER MATCHING
# =========================================================

def recommend_careers(resume_text):
    text = resume_text.lower()

    education_keywords = {
        "Data Analyst": ["data analytics", "data analysis", "statistics"],
        "BI Analyst": ["business intelligence", "data analytics"],
        "Data Scientist": ["data science", "statistics", "mathematics"],
        "Machine Learning Engineer": ["artificial intelligence", "machine learning"],
        "Software Developer": ["computer science", "software engineering", "computer engineering"],
        "Web Developer": ["web development", "html", "css", "javascript"],
        "Cybersecurity Analyst": ["cybersecurity", "information security"],
        "Network Administrator": ["networking", "computer networks"],
        "Accountant / Finance Analyst": ["accounting", "finance", "commerce", "acca"],
        "Digital Marketing Specialist": ["digital marketing", "marketing", "seo"],
        "UI/UX Designer": ["ui design", "ux design", "graphic design", "figma"],
        "Teacher / Educator": ["education", "b.ed", "m.ed", "teacher training"],
        "Healthcare Professional": [
            "medicine", "mbbs", "nursing", "pharmacy",
            "physiotherapy", "public health", "health sciences"
        ],
        "Laboratory Technician": [
            "medical laboratory technology", "laboratory science",
            "biotechnology", "clinical laboratory"
        ],
        "Engineer": [
            "mechanical engineering", "electrical engineering",
            "civil engineering", "chemical engineering"
        ],
        "Business Analyst": [
            "business administration", "management",
            "business analysis", "information systems"
        ],
        "HR / Recruitment Specialist": [
            "human resources", "hr management", "recruitment"
        ]
    }

    def contains_term(term):
        pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"
        return bool(re.search(pattern, text))

    scores = {}
    evidence = {}

    for career, profile in CAREER_PROFILES.items():
        matched_skills = []

        for skill in profile.get("skills", []):
            if contains_term(skill):
                matched_skills.append(skill)

        education_hits = [
            term for term in education_keywords.get(career, [])
            if contains_term(term)
        ]

        # Skills are the main factor; education is supporting evidence.
        score = (len(matched_skills) * 3) + (len(education_hits) * 2)

        if matched_skills and any(
            term in text for term in [
                "internship", "work experience",
                "professional experience", "worked as"
            ]
        ):
            score += 1

        if matched_skills and any(
            term in text for term in ["projects", "project experience", "portfolio"]
        ):
            score += 1

        # Do not recommend a career without relevant evidence.
        if score > 0:
            scores[career] = score
            evidence[career] = {
                "matched_skills": matched_skills,
                "education_evidence": education_hits
            }

    # Highest score first; skill matches break ties.
    ranked = sorted(
        scores.items(),
        key=lambda item: (
            item[1],
            len(evidence[item[0]]["matched_skills"]),
            len(evidence[item[0]]["education_evidence"])
        ),
        reverse=True
    )

    selected = ranked[:2]

    if not selected:
        return {
            "top_careers": [],
            "career_recommendation": "Insufficient evidence for a reliable match",
            "career_roadmap": [
                "Add your degree and field of study.",
                "Mention relevant technical or professional skills.",
                "Include work experience, internships and projects."
            ],
            "career_project_ideas": [
                "Complete a practical project related to your field.",
                "Add the tools used and results achieved to your resume."
            ]
        }

    top_careers = []

    for career, score in selected:
        profile = CAREER_PROFILES[career]

        top_careers.append({
            "name": career,
            "score": score,
            "matched_skills": evidence[career]["matched_skills"],
            "education_evidence": evidence[career]["education_evidence"],
            "projects": profile.get("projects", [])
        })

    primary_career = selected[0][0]
    primary_profile = CAREER_PROFILES[primary_career]

    return {
        "top_careers": top_careers,
        "career_recommendation": primary_career,
        "career_roadmap": primary_profile.get("roadmap", []),
        "career_project_ideas": primary_profile.get("projects", [])
    }



def detect_resume_skills(resume_text):
    text = resume_text.lower()

    all_skills = sorted({
        skill
        for profile in CAREER_PROFILES.values()
        for skill in profile["skills"]
    }, key=len, reverse=True)

    found = []

    for skill in all_skills:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return found


# =========================================================
# JOB MATCHING
# =========================================================

def get_job_requirements(career):
    return JOB_PROFILES.get(career, [])


def analyze_job_match(resume_text, requirements):
    text = resume_text.lower()

    matched = []
    missing = []

    for skill in requirements:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            matched.append(skill)
        else:
            missing.append(skill)

    skill_coverage = (
        len(matched) / len(requirements) * 100
        if requirements else 0
    )

    description = " ".join(requirements)

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform([
            resume_text,
            description
        ])

        similarity = (
            cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100
        )

    except (ValueError, IndexError):
        similarity = 0

    match_score = round(
        skill_coverage * 0.70 + similarity * 0.30,
        2
    )

    skill_gap = round(
        len(missing) / len(requirements) * 100,
        2
    ) if requirements else 0

    return match_score, skill_gap, matched, missing


# =========================================================
# PROJECT IDEA GENERATOR
# =========================================================

def generate_project_ideas(top_careers, fallback_projects):
    project_ideas = []

    if top_careers:
        for career_info in top_careers[:2]:

            career_name = career_info["name"]
            career_profile = CAREER_PROFILES.get(career_name, {})

            project_list = career_profile.get("projects", [])
            career_skills = career_profile.get("skills", [])

            for index, project_title in enumerate(project_list[:2]):

                if index == 0:
                    difficulty = "Beginner"
                else:
                    difficulty = "Intermediate"

                project_ideas.append({
                    "title": project_title,
                    "description": (
                        f"Build this project to practise skills relevant "
                        f"to the {career_name} career path. Document your "
                        f"approach, tools, and results."
                    ),
                    "career": career_name,
                    "level": difficulty,
                    "skills": career_skills[:5]
                })

    else:
        for project_title in fallback_projects[:3]:
            project_ideas.append({
                "title": project_title,
                "description": (
                    "Complete this practice project in your area of study "
                    "and document your work and results."
                ),
                "career": "Explore your field",
                "level": "Beginner",
                "skills": [
                    "Relevant subject knowledge",
                    "Documentation"
                ]
            })

    return project_ideas

# =========================================================
# HOME
=======
        matched_skills,
        missing_skills
    ))

    connection.commit()

    connection.close()


# =========================================================
# Home Page
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/")
def home():
<<<<<<< HEAD
=======

>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
    return render_template("index.html")


# =========================================================
<<<<<<< HEAD
# UPLOAD AND ANALYZE RESUME
=======
# Upload Resume
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
<<<<<<< HEAD
        return "No resume uploaded.", 400

    file = request.files["resume"]

    if not file.filename:
        return "No file selected.", 400

    original_name = secure_filename(file.filename)

    if not original_name.lower().endswith(".pdf"):
        return "Please upload a PDF file.", 400

    base, extension = os.path.splitext(original_name)

    resume_name = original_name
    file_path = os.path.join(UPLOAD_FOLDER, resume_name)
    counter = 1

    while os.path.exists(file_path):
        resume_name = f"{base}_{counter}{extension}"
        file_path = os.path.join(UPLOAD_FOLDER, resume_name)
        counter += 1

    file.save(file_path)

    try:
        reader = PdfReader(file_path)
        pages_text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                pages_text.append(page_text)

        resume_text = "\n".join(pages_text).strip()

    except Exception:
        try:
            os.remove(file_path)
        except OSError:
            pass

        return (
            "Could not read this PDF. Please upload a valid text-based PDF.",
            400
        )

    if not resume_text:
        try:
            os.remove(file_path)
        except OSError:
            pass

        return "No extractable text was found in this PDF.", 400

    # -----------------------------------------------------
    # CAREER RECOMMENDATIONS
    # -----------------------------------------------------

    career_result = recommend_careers(resume_text)

    career_recommendation = career_result["career_recommendation"]
    top_careers = career_result["top_careers"]
    career_roadmap = career_result["career_roadmap"]
    career_project_ideas = career_result["career_project_ideas"]

    # Generate projects for the top two recommended careers.
    project_ideas = generate_project_ideas(
        top_careers,
        career_project_ideas
    )

    # -----------------------------------------------------
    # JOB MATCHING
    # -----------------------------------------------------

    requirements = get_job_requirements(career_recommendation)

    match_score, skill_gap_percentage, matched_skills, missing_skills = (
        analyze_job_match(resume_text, requirements)
    )

    found_skills = detect_resume_skills(resume_text)
=======

        return "No resume uploaded."

    file = request.files["resume"]

    if file.filename == "":

        return "No file selected."

    resume_name = file.filename

    file_path = os.path.join(
        UPLOAD_FOLDER,
        resume_name
    )

    file.save(file_path)


    # =====================================================
    # Extract PDF Text
    # =====================================================

    try:

        reader = PdfReader(file_path)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text + "\n"

    except Exception as e:

        return f"Error reading PDF: {e}"


    # =====================================================
    # AI Match Score
    # =====================================================

    documents = [
        resume_text,
        JOB_DESCRIPTION
    ]

    try:

        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )

        match_score = round(
            similarity[0][0] * 100,
            2
        )

    except Exception:

        match_score = 0


    # =====================================================
    # Normalize Resume Text
    # =====================================================

    resume_lower = resume_text.lower()


    # =====================================================
    # Skill Detection
    # =====================================================

    matched_skills = []

    missing_skills = []

    found_skills = []


    for skill in REQUIRED_SKILLS:

        if skill.lower() in resume_lower:

            matched_skills.append(skill)
            found_skills.append(skill)

        else:

            missing_skills.append(skill)


    # =====================================================
    # Skill Gap Percentage
    # =====================================================

    total_skills = len(REQUIRED_SKILLS)

    missing_count = len(missing_skills)

    if total_skills > 0:

        skill_gap_percentage = round(
            (missing_count / total_skills) * 100,
            2
        )

    else:

        skill_gap_percentage = 0


    # =====================================================
    # AI CAREER RECOMMENDATION
    # =====================================================

    career_scores = {

        "Data Analyst": 0,

        "Data Scientist": 0,

        "Machine Learning Engineer": 0,

        "BI / Data Analyst": 0,

        "Web Developer": 0

    }


    # -----------------------------
    # Data Analyst
    # -----------------------------

    if "python" in resume_lower:
        career_scores["Data Analyst"] += 15

    if "sql" in resume_lower:
        career_scores["Data Analyst"] += 20

    if "excel" in resume_lower:
        career_scores["Data Analyst"] += 15

    if "power bi" in resume_lower:
        career_scores["Data Analyst"] += 15

    if "pandas" in resume_lower:
        career_scores["Data Analyst"] += 10

    if "data analysis" in resume_lower:
        career_scores["Data Analyst"] += 20


    # -----------------------------
    # Data Scientist
    # -----------------------------

    if "python" in resume_lower:
        career_scores["Data Scientist"] += 15

    if "pandas" in resume_lower:
        career_scores["Data Scientist"] += 15

    if "numpy" in resume_lower:
        career_scores["Data Scientist"] += 10

    if "data science" in resume_lower:
        career_scores["Data Scientist"] += 25

    if "machine learning" in resume_lower:
        career_scores["Data Scientist"] += 25

    if "scikit-learn" in resume_lower or "sklearn" in resume_lower:
        career_scores["Data Scientist"] += 10


    # -----------------------------
    # Machine Learning Engineer
    # -----------------------------

    if "python" in resume_lower:
        career_scores["Machine Learning Engineer"] += 20

    if "machine learning" in resume_lower:
        career_scores["Machine Learning Engineer"] += 35

    if "tensorflow" in resume_lower:
        career_scores["Machine Learning Engineer"] += 20

    if "pytorch" in resume_lower:
        career_scores["Machine Learning Engineer"] += 20

    if "scikit-learn" in resume_lower or "sklearn" in resume_lower:
        career_scores["Machine Learning Engineer"] += 15


    # -----------------------------
    # BI / Data Analyst
    # -----------------------------

    if "sql" in resume_lower:
        career_scores["BI / Data Analyst"] += 20

    if "power bi" in resume_lower:
        career_scores["BI / Data Analyst"] += 30

    if "excel" in resume_lower:
        career_scores["BI / Data Analyst"] += 20

    if "dashboard" in resume_lower:
        career_scores["BI / Data Analyst"] += 20

    if "dax" in resume_lower:
        career_scores["BI / Data Analyst"] += 10


    # -----------------------------
    # Web Developer
    # -----------------------------

    if "html" in resume_lower:
        career_scores["Web Developer"] += 20

    if "css" in resume_lower:
        career_scores["Web Developer"] += 20

    if "javascript" in resume_lower:
        career_scores["Web Developer"] += 25

    if "react" in resume_lower:
        career_scores["Web Developer"] += 20

    if "flask" in resume_lower:
        career_scores["Web Developer"] += 15


    # =====================================================
    # Select Best Career
    # =====================================================

    career_recommendation = max(
        career_scores,
        key=career_scores.get
    )


    # If no strong career signal is found

    if max(career_scores.values()) == 0:

        career_recommendation = "Data Analyst"


    # =====================================================
    # Overall Candidate Score
    # =====================================================
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763

    overall_score = calculate_overall_score(
        match_score,
        skill_gap_percentage
    )

<<<<<<< HEAD
    # -----------------------------------------------------
    # STRENGTHS
    # -----------------------------------------------------

    strengths = []

    if matched_skills:
        strengths.append(
            "Resume contains relevant skill keywords: "
            + ", ".join(matched_skills) + "."
        )

    if any(term in resume_text.lower() for term in [
        "internship",
        "professional experience",
        "work experience",
        "employment history",
        "worked as"
    ]):
        strengths.append(
            "Work or internship experience is mentioned."
        )

    if "project" in resume_text.lower():
        strengths.append(
            "A project section or project experience is mentioned."
        )

    if any(term in resume_text.lower() for term in [
        "bachelor", "b.s.", "bs ", "degree", "university", "college",
        "mbbs", "b.ed", "diploma"
    ]):
        strengths.append(
            "Educational qualification information is present."
        )

    if not strengths:
        strengths.append(
            "The resume has been extracted. Add detailed skills, "
            "education and experience for better matching."
        )

    # -----------------------------------------------------
    # WEAKNESSES
    # -----------------------------------------------------

    weaknesses = []

    if missing_skills:
        weaknesses.append(
            "Skills not detected for the leading career match: "
            + ", ".join(missing_skills) + "."
        )

    if not any(term in resume_text.lower() for term in [
        "project", "portfolio"
    ]):
        weaknesses.append(
            "No clear project or portfolio evidence was detected."
        )

    if not any(term in resume_text.lower() for term in [
        "experience", "internship", "worked as", "employment"
    ]):
        weaknesses.append(
            "Work or internship experience was not clearly detected."
        )

    if not any(term in resume_text.lower() for term in [
        "education", "university", "college", "degree",
        "bachelor", "mbbs", "diploma"
    ]):
        weaknesses.append(
            "Education information was not clearly detected."
        )

    if not weaknesses:
        weaknesses.append(
            "No major keyword-related weakness was detected."
        )


    # -----------------------------------------------------
    # LEARNING RECOMMENDATIONS
    # -----------------------------------------------------

    learning_recommendations = []

    learning_map = {
        "sql": "SQL: Practise queries, joins, grouping and subqueries.",
        "excel": "Excel: Practise formulas, lookup functions, PivotTables and charts.",
        "power bi": "Power BI: Learn data modelling, Power Query and DAX.",
        "python": "Python: Practise functions, data structures and projects.",
        "pandas": "Pandas: Practise cleaning, grouping, merging and analysing datasets.",
        "numpy": "NumPy: Learn arrays, indexing and numerical operations.",
        "machine learning": "Machine learning: Study model training and evaluation.",
        "html": "HTML: Build structured web pages.",
        "css": "CSS: Practise responsive layouts.",
        "javascript": "JavaScript: Practise application logic and DOM manipulation.",
        "figma": "Figma: Practise wireframes and interactive prototypes.",
        "seo": "SEO: Practise keyword research and website audits.",
        "networking": "Networking: Practise IP addressing and troubleshooting.",
        "accounting": "Accounting: Practise financial statements and reporting.",
        "teaching": "Teaching: Develop lesson plans and assessment materials.",
        "patient care": "Healthcare: Follow your qualification and supervised training requirements."
    }

    for skill in missing_skills:
        recommendation = learning_map.get(skill.lower())
        if recommendation:
            learning_recommendations.append(recommendation)

    if not learning_recommendations:
        learning_recommendations.append(
            "Continue improving skills relevant to your career and practise them through projects."
        )

    # -----------------------------------------------------
    # INSIGHTS AND IMPROVEMENTS
    # -----------------------------------------------------

    insights = []

    if match_score >= 70:
        insights.append("Strong keyword coverage for the selected career profile.")
    elif match_score >= 40:
        insights.append("Partial keyword coverage for the selected career profile.")
    else:
        insights.append("Limited keyword coverage. Review the matched and missing skills.")

    if top_careers:
        insights.append("Leading career suggestion: " + career_recommendation + ".")
    else:
        insights.append(
            "Career matching is uncertain because the resume contains limited relevant evidence."
        )

    insights.append(
        "Scores are keyword-based estimates, not proof of ability or a hiring decision."
    )

    improvement_suggestions = []

    if missing_skills:
        improvement_suggestions.append(
            "Develop relevant missing skills and list them on your resume only after gaining practical knowledge."
        )

    if "project" not in resume_text.lower():
        improvement_suggestions.append(
            "Build relevant portfolio projects and describe your actual contribution."
        )

    if not any(term in resume_text.lower() for term in [
        "experience", "internship", "worked as", "employment"
    ]):
        improvement_suggestions.append(
            "Include relevant internships, academic work or practical experience."
        )

    if "github" not in resume_text.lower():
        improvement_suggestions.append(
            "If relevant to your field, add a portfolio or GitHub link containing genuine work."
        )

    if "linkedin" not in resume_text.lower():
=======

    # =====================================================
    # AI STRENGTHS
    # =====================================================

    strengths = []


    if matched_skills:

        strengths.append(
            "Candidate has experience or knowledge of: "
            + ", ".join(matched_skills)
            + "."
        )


    if match_score >= 70:

        strengths.append(
            "Resume has strong alignment with the target job."
        )

    elif match_score >= 40:

        strengths.append(
            "Resume shows moderate alignment with the target role."
        )


    if "project" in resume_lower or "projects" in resume_lower:

        strengths.append(
            "Relevant project experience is mentioned in the resume."
        )


    if "experience" in resume_lower:

        strengths.append(
            "Professional or practical experience is included."
        )


    if "education" in resume_lower:

        strengths.append(
            "Educational background is clearly represented."
        )


    if not strengths:

        strengths.append(
            "Resume contains some information that can be developed further."
        )


    # =====================================================
    # AI WEAKNESSES
    # =====================================================

    weaknesses = []


    if missing_skills:

        weaknesses.append(
            "Missing required skills: "
            + ", ".join(missing_skills)
            + "."
        )


    if match_score < 40:

        weaknesses.append(
            "Resume keyword alignment with the target job is low."
        )

    elif match_score < 70:

        weaknesses.append(
            "Resume keyword alignment can be improved."
        )


    if "project" not in resume_lower:

        weaknesses.append(
            "No clearly mentioned projects were detected."
        )


    if "experience" not in resume_lower:

        weaknesses.append(
            "No clearly mentioned work experience was detected."
        )


    if "education" not in resume_lower:

        weaknesses.append(
            "Education section was not clearly detected."
        )


    if not weaknesses:

        weaknesses.append(
            "No major structural weakness was detected."
        )


    # =====================================================
    # LEARNING RECOMMENDATIONS
    # =====================================================

    learning_recommendations = []


    for skill in missing_skills:

        if skill == "Python":

            learning_recommendations.append(
                "Python: Learn fundamentals, functions, OOP, "
                "file handling and data analysis."
            )


        elif skill == "SQL":

            learning_recommendations.append(
                "SQL: Practice SELECT, WHERE, JOINs, "
                "GROUP BY, subqueries and aggregate functions."
            )


        elif skill == "Excel":

            learning_recommendations.append(
                "Excel: Improve formulas, Pivot Tables, "
                "charts, lookup functions and data cleaning."
            )


        elif skill == "Power BI":

            learning_recommendations.append(
                "Power BI: Learn dashboards, Power Query, "
                "data modeling and basic DAX."
            )


        elif skill == "Pandas":

            learning_recommendations.append(
                "Pandas: Practice data cleaning, filtering, "
                "grouping, merging and analysis."
            )


        elif skill == "NumPy":

            learning_recommendations.append(
                "NumPy: Learn arrays, indexing, slicing "
                "and numerical operations."
            )


    # =====================================================
    # AI RESUME INSIGHTS
    # =====================================================

    insights = []


    if match_score >= 70:

        insights.append(
            "AI analysis indicates strong alignment with the selected job."
        )

    elif match_score >= 40:

        insights.append(
            "AI analysis indicates moderate alignment with the selected job."
        )

    else:

        insights.append(
            "AI analysis indicates low alignment with the selected job."
        )


    if skill_gap_percentage <= 20:

        insights.append(
            "Candidate has most of the required technical skills."
        )

    elif skill_gap_percentage <= 50:

        insights.append(
            "Candidate has several required skills but needs further improvement."
        )

    else:

        insights.append(
            "Candidate has a significant technical skill gap."
        )


    if overall_score >= 70:

        insights.append(
            "Overall candidate profile is highly suitable for the target role."
        )

    elif overall_score >= 40:

        insights.append(
            "Candidate could become suitable after improving the missing skills."
        )

    else:

        insights.append(
            "Candidate requires significant improvement before applying."
        )


    # Career insight

    insights.append(
        "AI career analysis recommends: "
        + career_recommendation
        + "."
    )


    # =====================================================
    # IMPROVEMENT SUGGESTIONS
    # =====================================================

    improvement_suggestions = []


    if match_score < 50:

        improvement_suggestions.append(
            "Add relevant keywords from the target job description "
            "to improve resume-job alignment."
        )


    if missing_skills:

        improvement_suggestions.append(
            "Learn the missing technical skills and add them to the "
            "resume only after gaining practical knowledge."
        )


    if "project" not in resume_lower:

        improvement_suggestions.append(
            "Add 2-3 relevant academic or personal projects "
            "with technologies and measurable results."
        )


    if "experience" not in resume_lower:

        improvement_suggestions.append(
            "Clearly mention relevant internship, work or practical experience."
        )


    if "education" not in resume_lower:

        improvement_suggestions.append(
            "Add a clear education section containing degree, "
            "university and relevant academic information."
        )


    if "github" not in resume_lower:

        improvement_suggestions.append(
            "Consider adding a GitHub profile containing relevant projects."
        )


    if "linkedin" not in resume_lower:

>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
        improvement_suggestions.append(
            "Consider adding a professional LinkedIn profile."
        )

<<<<<<< HEAD
    if not improvement_suggestions:
        improvement_suggestions.append(
            "Keep your resume updated with verified skills, projects and achievements."
        )

    # -----------------------------------------------------
    # SAVE ANALYSIS
    # -----------------------------------------------------
=======

    # =====================================================
    # Save Analysis
    # =====================================================
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763

    save_analysis(
        resume_name,
        match_score,
        skill_gap_percentage,
        career_recommendation,
<<<<<<< HEAD
        matched_skills,
        missing_skills
    )

    # -----------------------------------------------------
    # RESULT PAGE
    # -----------------------------------------------------

    return render_template(
        "result.html",
        resume_name=resume_name,
        match_score=match_score,
        skill_gap=skill_gap_percentage,
        skill_gap_percentage=skill_gap_percentage,
        overall_score=overall_score,
        career_recommendation=career_recommendation,
        top_careers=top_careers,
        career_roadmap=career_roadmap,
        career_project_ideas=career_project_ideas,
        project_ideas=project_ideas,
        matched_skills=matched_skills,
        matched_job_skills=matched_skills,
        found_skills=found_skills,
        missing_skills=missing_skills,
        strengths=strengths,
        weaknesses=weaknesses,
        insights=insights,
        learning_recommendations=learning_recommendations,
=======
        ", ".join(matched_skills),
        ", ".join(missing_skills)
    )


    # =====================================================
    # Result Page
    # =====================================================

    return render_template(
        "result.html",

        resume_name=resume_name,

        match_score=match_score,

        skill_gap=skill_gap_percentage,

        skill_gap_percentage=skill_gap_percentage,

        overall_score=overall_score,

        career_recommendation=career_recommendation,

        matched_skills=matched_skills,

        found_skills=found_skills,

        missing_skills=missing_skills,

        strengths=strengths,

        weaknesses=weaknesses,

        insights=insights,

        learning_recommendations=learning_recommendations,

>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
        improvement_suggestions=improvement_suggestions
    )


# =========================================================
<<<<<<< HEAD
# JOB PROFILES
# =========================================================

JOB_PROFILES = {
    "Data Analyst": [
        "sql", "excel", "power bi", "tableau", "python",
        "pandas", "numpy", "data analysis", "data visualization",
        "statistics", "matplotlib"
    ],
    "BI Analyst": [
        "power bi", "tableau", "dax", "sql", "dashboard",
        "excel", "power query", "data modeling"
    ],
    "Data Scientist": [
        "python", "pandas", "numpy", "statistics",
        "machine learning", "scikit-learn", "data science"
    ],
    "Machine Learning Engineer": [
        "python", "machine learning", "tensorflow",
        "pytorch", "scikit-learn", "deep learning"
    ],
    "Software Developer": [
        "python", "java", "c++", "c#", "git", "oop",
        "api", "software development", "testing"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "flask",
        "django", "node.js", "php"
    ],
    "Cybersecurity Analyst": [
        "cybersecurity", "network security", "linux",
        "siem", "incident response", "wireshark"
    ],
    "Network Administrator": [
        "networking", "tcp/ip", "routing", "switching",
        "cisco", "dns", "dhcp", "firewall"
    ],
    "Accountant / Finance Analyst": [
        "accounting", "bookkeeping", "financial analysis",
        "financial reporting", "excel", "budgeting", "taxation"
    ],
    "Digital Marketing Specialist": [
        "digital marketing", "seo", "google ads",
        "social media marketing", "content marketing"
    ],
    "UI/UX Designer": [
        "ui design", "ux design", "figma", "wireframes",
        "prototyping", "user research"
    ],
    "Teacher / Educator": [
        "teaching", "lesson planning", "classroom management",
        "curriculum development", "tutoring"
    ],
    "Healthcare Professional": [
        "medicine", "patient care", "clinical practice",
        "nursing", "pharmacy", "public health", "healthcare"
    ],
    "Laboratory Technician": [
        "laboratory", "microscopy", "quality control",
        "specimen handling", "medical laboratory"
    ],
    "Engineer": [
        "engineering", "autocad", "solidworks", "matlab",
        "circuit design", "plc", "cad", "simulation"
    ],
    "Business Analyst": [
        "business analysis", "requirements gathering",
        "process mapping", "user stories", "sql", "excel"
    ],
    "HR / Recruitment Specialist": [
        "human resources", "recruitment", "talent acquisition",
        "payroll", "onboarding", "employee relations"
    ]
}


# =========================================================
# HISTORY
=======
# Resume History
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/history")
def history():
<<<<<<< HEAD
    connection = get_connection()

    analyses = connection.execute("""
        SELECT id, resume_name, match_score, skill_gap,
               career_recommendation, matched_skills,
               missing_skills, analysis_date
        FROM resume_analysis
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template("history.html", analyses=analyses)


# =========================================================
# RANKING
=======

    connection = sqlite3.connect(
        "resume_analyzer.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            resume_name,
            match_score,
            skill_gap,
            career_recommendation,
            analysis_date
        FROM resume_analysis
        ORDER BY id DESC
    """)

    history_data = cursor.fetchall()

    connection.close()


    return render_template(
        "history.html",
        history=history_data
    )


# =========================================================
# AI Resume Ranking
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/ranking")
def ranking():
<<<<<<< HEAD
    connection = get_connection()

    candidates = connection.execute("""
        SELECT id, resume_name, match_score, skill_gap,
               career_recommendation, analysis_date
        FROM resume_analysis
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    ranked_candidates = []

    for candidate in candidates:
        match = candidate["match_score"] or 0
        gap = candidate["skill_gap"] or 0
        career = candidate["career_recommendation"] or "Not determined"

        ranked_candidates.append({
            "id": candidate["id"],
            "resume_name": candidate["resume_name"],
            "filename": candidate["resume_name"],
            "match_score": match,
            "skill_gap": gap,
            "overall_score": calculate_overall_score(match, gap),
            "career": career,
            "recommended_career": career,
            "analysis_date": candidate["analysis_date"]
        })

    ranked_candidates.sort(
        key=lambda item: item["overall_score"],
        reverse=True
    )

    for rank, candidate in enumerate(ranked_candidates, start=1):
        candidate["rank"] = rank
=======

    connection = sqlite3.connect(
        "resume_analyzer.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            resume_name,
            match_score,
            skill_gap,
            career_recommendation,
            analysis_date
        FROM resume_analysis
    """)

    candidates = cursor.fetchall()

    connection.close()


    ranked_candidates = []


    for candidate in candidates:

        candidate_id = candidate[0]

        resume_name = candidate[1]

        match_score = candidate[2]

        skill_gap = candidate[3]

        career = candidate[4]

        analysis_date = candidate[5]


        overall_score = calculate_overall_score(
            match_score,
            skill_gap
        )


        ranked_candidates.append({

            "id": candidate_id,

            "resume_name": resume_name,

            "match_score": match_score,

            "skill_gap": skill_gap,

            "overall_score": overall_score,

            "career": career,

            "analysis_date": analysis_date

        })


    ranked_candidates.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )


    for index, candidate in enumerate(
        ranked_candidates,
        start=1
    ):

        candidate["rank"] = index

>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763

    return render_template(
        "ranking.html",
        candidates=ranked_candidates
    )


# =========================================================
<<<<<<< HEAD
# DASHBOARD
=======
# Dashboard
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/dashboard")
def dashboard():
<<<<<<< HEAD
    connection = get_connection()

    total_resumes = connection.execute(
        "SELECT COUNT(*) FROM resume_analysis"
    ).fetchone()[0]

    averages = connection.execute("""
        SELECT AVG(match_score), AVG(skill_gap)
        FROM resume_analysis
    """).fetchone()

    average_match = round(averages[0] or 0, 2)
    average_skill_gap = round(averages[1] or 0, 2)

    recent_analyses = connection.execute("""
        SELECT resume_name, match_score, skill_gap,
               career_recommendation, analysis_date
        FROM resume_analysis
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()

    chart_data = connection.execute("""
        SELECT resume_name, match_score, skill_gap
        FROM resume_analysis
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()

    connection.close()

    # Convert SQLite Row objects to ordinary dictionaries.
    recent_analyses = [dict(row) for row in recent_analyses]
    chart_data = [dict(row) for row in chart_data]

    return render_template(
        "dashboard.html",
        total_resumes=total_resumes,
        average_match=average_match,
        average_skill_gap=average_skill_gap,
        recent_analyses=recent_analyses,
        chart_data=chart_data
=======

    connection = sqlite3.connect(
        "resume_analyzer.db"
    )

    cursor = connection.cursor()


    # Total Candidates

    cursor.execute("""
        SELECT COUNT(*)
        FROM resume_analysis
    """)

    total_candidates = cursor.fetchone()[0]


    # Average Match Score

    cursor.execute("""
        SELECT AVG(match_score)
        FROM resume_analysis
    """)

    average_match = cursor.fetchone()[0]


    if average_match is None:

        average_match = 0

    else:

        average_match = round(
            average_match,
            2
        )


    # Average Skill Gap

    cursor.execute("""
        SELECT AVG(skill_gap)
        FROM resume_analysis
    """)

    average_gap = cursor.fetchone()[0]


    if average_gap is None:

        average_gap = 0

    else:

        average_gap = round(
            average_gap,
            2
        )


    # Career Distribution

    cursor.execute("""
        SELECT
            career_recommendation,
            COUNT(*)
        FROM resume_analysis
        GROUP BY career_recommendation
    """)

    career_data = cursor.fetchall()


    # Score Data

    cursor.execute("""
        SELECT
            resume_name,
            match_score,
            skill_gap
        FROM resume_analysis
        ORDER BY id DESC
    """)

    score_data = cursor.fetchall()

    connection.close()


    chart_labels = []

    match_scores = []

    skill_gaps = []

    overall_scores = []


    for item in score_data:

        resume_name = item[0]

        match_score = item[1]

        skill_gap = item[2]


        overall_score = calculate_overall_score(
            match_score,
            skill_gap
        )


        chart_labels.append(resume_name)

        match_scores.append(match_score)

        skill_gaps.append(skill_gap)

        overall_scores.append(overall_score)


    # Career Chart

    career_labels = []

    career_counts = []


    for item in career_data:

        career_labels.append(item[0])

        career_counts.append(item[1])


    return render_template(
        "dashboard.html",

        total_candidates=total_candidates,

        average_match=average_match,

        average_gap=average_gap,

        chart_labels=chart_labels,

        match_scores=match_scores,

        skill_gaps=skill_gaps,

        overall_scores=overall_scores,

        career_labels=career_labels,

        career_counts=career_counts
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
    )


# =========================================================
<<<<<<< HEAD
# ADMIN / RECRUITER PANEL
=======
# Admin / Recruiter Panel
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/admin")
def admin():
<<<<<<< HEAD
    connection = get_connection()

    total_candidates = connection.execute(
        "SELECT COUNT(*) FROM resume_analysis"
    ).fetchone()[0]

    candidates = connection.execute("""
        SELECT id, resume_name, match_score, skill_gap,
               career_recommendation, analysis_date
        FROM resume_analysis
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    ranked_candidates = []

    for candidate in candidates:
        match = candidate["match_score"] or 0
        gap = candidate["skill_gap"] or 0
        career = candidate["career_recommendation"] or "Not determined"

        ranked_candidates.append({
            "id": candidate["id"],
            "resume_name": candidate["resume_name"],
            "filename": candidate["resume_name"],
            "match_score": match,
            "skill_gap": gap,
            "overall_score": calculate_overall_score(match, gap),
            "career": career,
            "recommended_career": career,
            "analysis_date": candidate["analysis_date"]
        })

    ranked_candidates.sort(
        key=lambda item: item["overall_score"],
        reverse=True
    )

    average_overall = round(
        sum(item["overall_score"] for item in ranked_candidates)
        / len(ranked_candidates),
        2
    ) if ranked_candidates else 0

    top_candidate = ranked_candidates[0] if ranked_candidates else None

    return render_template(
        "admin.html",
        total_candidates=total_candidates,
        average_overall=average_overall,
        top_candidate=top_candidate,
=======

    connection = sqlite3.connect(
        "resume_analyzer.db"
    )

    cursor = connection.cursor()


    # Total Candidates

    cursor.execute("""
        SELECT COUNT(*)
        FROM resume_analysis
    """)

    total_candidates = cursor.fetchone()[0]


    # Average Overall Score

    cursor.execute("""
        SELECT
            match_score,
            skill_gap
        FROM resume_analysis
    """)

    all_candidates = cursor.fetchall()

    overall_scores = []


    for candidate in all_candidates:

        match_score = candidate[0]

        skill_gap = candidate[1]


        overall_score = calculate_overall_score(
            match_score,
            skill_gap
        )


        overall_scores.append(
            overall_score
        )


    if overall_scores:

        average_overall = round(
            sum(overall_scores)
            / len(overall_scores),
            2
        )

    else:

        average_overall = 0


    # All Candidates

    cursor.execute("""
        SELECT
            id,
            resume_name,
            match_score,
            skill_gap,
            career_recommendation,
            analysis_date
        FROM resume_analysis
        ORDER BY id DESC
    """)

    candidates = cursor.fetchall()

    connection.close()


    ranked_candidates = []


    for candidate in candidates:

        candidate_id = candidate[0]

        resume_name = candidate[1]

        match_score = candidate[2]

        skill_gap = candidate[3]

        career = candidate[4]

        analysis_date = candidate[5]


        overall_score = calculate_overall_score(
            match_score,
            skill_gap
        )


        ranked_candidates.append({

            "id": candidate_id,

            "resume_name": resume_name,

            "match_score": match_score,

            "skill_gap": skill_gap,

            "overall_score": overall_score,

            "career": career,

            "analysis_date": analysis_date

        })


    ranked_candidates.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )


    # Top Candidate

    top_candidate = None


    if ranked_candidates:

        top_candidate = ranked_candidates[0]


    return render_template(
        "admin.html",

        total_candidates=total_candidates,

        average_overall=average_overall,

        top_candidate=top_candidate,

>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
        candidates=ranked_candidates
    )


# =========================================================
<<<<<<< HEAD
# CANDIDATE DETAILS
=======
# Candidate Details
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/candidate/<int:candidate_id>")
def candidate_details(candidate_id):
<<<<<<< HEAD
    connection = get_connection()

    candidate = connection.execute("""
        SELECT id, resume_name, match_score, skill_gap,
               career_recommendation, matched_skills,
               missing_skills, analysis_date
        FROM resume_analysis
        WHERE id = ?
    """, (candidate_id,)).fetchone()

    if not candidate:
        connection.close()
        return "Candidate not found.", 404

    all_candidates = connection.execute("""
        SELECT id, match_score, skill_gap
        FROM resume_analysis
    """).fetchall()

    connection.close()

    ranked = sorted(
        all_candidates,
        key=lambda item: calculate_overall_score(
            item["match_score"] or 0,
            item["skill_gap"] or 0
        ),
        reverse=True
    )

    candidate_rank = next(
        (
            index for index, item in enumerate(ranked, start=1)
            if item["id"] == candidate_id
        ),
        None
    )

    match = candidate["match_score"] or 0
    gap = candidate["skill_gap"] or 0

    return render_template(
        "candidate_details.html",
        candidate_id=candidate_id,
        resume_name=candidate["resume_name"],
        match_score=match,
        skill_gap=gap,
        overall_score=calculate_overall_score(match, gap),
        career=candidate["career_recommendation"],
        matched_skills=candidate["matched_skills"],
        missing_skills=candidate["missing_skills"],
        analysis_date=candidate["analysis_date"],
=======

    connection = sqlite3.connect(
        "resume_analyzer.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            resume_name,
            match_score,
            skill_gap,
            career_recommendation,
            matched_skills,
            missing_skills,
            analysis_date
        FROM resume_analysis
        WHERE id = ?
    """, (candidate_id,))


    candidate = cursor.fetchone()


    if not candidate:

        connection.close()

        return "Candidate not found."


    cursor.execute("""
        SELECT
            id,
            match_score,
            skill_gap
        FROM resume_analysis
    """)

    all_candidates = cursor.fetchall()

    connection.close()


    ranked = []


    for item in all_candidates:

        item_id = item[0]

        match_score = item[1]

        skill_gap = item[2]


        overall_score = calculate_overall_score(
            match_score,
            skill_gap
        )


        ranked.append({

            "id": item_id,

            "overall_score": overall_score

        })


    ranked.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )


    candidate_rank = None


    for index, item in enumerate(
        ranked,
        start=1
    ):

        if item["id"] == candidate_id:

            candidate_rank = index

            break


    resume_name = candidate[1]

    match_score = candidate[2]

    skill_gap = candidate[3]

    career = candidate[4]

    matched_skills = candidate[5]

    missing_skills = candidate[6]

    analysis_date = candidate[7]


    overall_score = calculate_overall_score(
        match_score,
        skill_gap
    )


    return render_template(
        "candidate_details.html",

        candidate_id=candidate_id,

        resume_name=resume_name,

        match_score=match_score,

        skill_gap=skill_gap,

        overall_score=overall_score,

        career=career,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        analysis_date=analysis_date,

>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
        candidate_rank=candidate_rank
    )


# =========================================================
<<<<<<< HEAD
# DELETE CANDIDATE
=======
# Delete Candidate
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
# =========================================================

@app.route("/delete/<int:candidate_id>", methods=["POST"])
def delete_candidate(candidate_id):
<<<<<<< HEAD
    connection = get_connection()

    connection.execute(
        "DELETE FROM resume_analysis WHERE id = ?",
        (candidate_id,)
    )

    connection.commit()
    connection.close()

=======

    connection = sqlite3.connect(
        "resume_analyzer.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM resume_analysis
        WHERE id = ?
    """, (candidate_id,))


    connection.commit()

    connection.close()


>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
    return redirect("/admin")


# =========================================================
<<<<<<< HEAD
# ERROR HANDLER
# =========================================================

@app.errorhandler(413)
def file_too_large(_error):
    return (
        "File too large. Please upload a PDF smaller than 10 MB.",
        413
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
=======
# Run Application
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
