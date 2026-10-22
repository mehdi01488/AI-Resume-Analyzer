
from flask import Flask, render_template, request, redirect, url_for, flash
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
from pathlib import Path
from collections import Counter
import sqlite3
import os
import re


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)
app.secret_key = "ai-resume-analyzer-local-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATABASE_PATH = os.path.join(BASE_DIR, "resume_analyzer.db")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# CAREER PROFILES
# =========================================================

CAREER_PROFILES = {
    "Data Analyst": {
        "skills": [
            "python", "sql", "excel", "power bi", "tableau",
            "pandas", "numpy", "statistics", "data analysis",
            "data analytics", "data visualization", "matplotlib",
            "seaborn", "data cleaning", "pivot tables"
        ],
        "education": ["data analytics", "data analysis", "statistics"],
        "signals": [
            "data analyst", "data analytics", "reporting analyst",
            "data visualization", "business reporting"
        ],
        "projects": [
            "Sales Performance Dashboard using Power BI or Excel",
            "SQL Business Data Analysis",
            "Customer Trends Analysis using Python and Pandas"
        ],
        "roadmap": [
            "Improve SQL, Excel, Python and data visualization.",
            "Build analytics projects using real datasets.",
            "Practise explaining insights and business recommendations."
        ]
    },
    "BI Analyst": {
        "skills": [
            "power bi", "tableau", "dax", "sql", "dashboard",
            "data modeling", "data modelling", "excel", "power query"
        ],
        "education": ["business intelligence", "data analytics"],
        "signals": ["bi analyst", "business intelligence", "executive dashboard"],
        "projects": [
            "Interactive Power BI Business Dashboard",
            "Executive KPI Reporting System",
            "SQL Database and BI Reporting Project"
        ],
        "roadmap": [
            "Learn dashboards, data modelling and DAX.",
            "Practise SQL and Power Query with business data.",
            "Build a portfolio of interactive reports."
        ]
    },
    "Data Scientist": {
        "skills": [
            "python", "pandas", "numpy", "statistics", "machine learning",
            "scikit-learn", "sklearn", "data science", "matplotlib",
            "deep learning", "seaborn"
        ],
        "education": ["data science", "statistics", "mathematics"],
        "signals": ["data scientist", "predictive modeling", "predictive modelling"],
        "projects": [
            "Customer Churn Prediction Model",
            "Exploratory Data Analysis and Statistical Report",
            "Machine Learning Price Prediction"
        ],
        "roadmap": [
            "Strengthen Python, statistics and data preparation.",
            "Learn machine learning algorithms and model evaluation.",
            "Build practical projects with documented results."
        ]
    },
    "Machine Learning Engineer": {
        "skills": [
            "python", "machine learning", "tensorflow", "pytorch",
            "scikit-learn", "deep learning", "mlops", "model deployment"
        ],
        "education": ["artificial intelligence", "machine learning"],
        "signals": ["machine learning engineer", "ml engineer", "mlops"],
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
            "software development", "flask", "django"
        ],
        "education": ["computer science", "software engineering"],
        "signals": ["software developer", "software engineer", "application development"],
        "projects": [
            "Student Management System",
            "REST API with Database Integration",
            "Task Management Application"
        ],
        "roadmap": [
            "Practise programming, data structures and algorithms.",
            "Build applications with databases, testing and Git.",
            "Create a portfolio of working software projects."
        ]
    },
    "Web Developer": {
        "skills": [
            "html", "css", "javascript", "react", "flask",
            "django", "node.js", "php", "web development"
        ],
        "education": ["web development", "computer science", "software engineering"],
        "signals": ["web developer", "frontend developer", "backend developer"],
        "projects": [
            "Responsive Portfolio Website",
            "Full-Stack Job Portal",
            "E-commerce Website with Database"
        ],
        "roadmap": [
            "Practise HTML, CSS and JavaScript.",
            "Build responsive applications and learn a backend framework.",
            "Create and deploy a portfolio website."
        ]
    },
    "Cybersecurity Analyst": {
        "skills": [
            "cybersecurity", "network security", "linux",
            "penetration testing", "siem", "incident response",
            "ethical hacking", "wireshark", "security analysis"
        ],
        "education": ["cybersecurity", "information security"],
        "signals": ["cybersecurity analyst", "security analyst", "incident response"],
        "projects": [
            "Security Log Analysis Dashboard",
            "Network Security Lab Assessment",
            "Phishing Awareness and Detection Demonstration"
        ],
        "roadmap": [
            "Learn networking, Linux and security fundamentals.",
            "Practise defensive security in authorized lab environments.",
            "Develop incident response and security analysis skills."
        ]
    },
    "Network Administrator": {
        "skills": [
            "networking", "tcp/ip", "routing", "switching", "cisco",
            "ccna", "dns", "dhcp", "firewall", "network administration"
        ],
        "education": ["networking", "computer networks"],
        "signals": ["network administrator", "network engineer"],
        "projects": [
            "Small Office Network Design",
            "Network Monitoring Lab",
            "VLAN and Firewall Configuration Lab"
        ],
        "roadmap": [
            "Learn networking fundamentals and troubleshooting.",
            "Practise routing and switching in a lab.",
            "Explore network engineering or cloud networking."
        ]
    },
    "Accountant / Finance Analyst": {
        "skills": [
            "accounting", "bookkeeping", "financial analysis",
            "financial reporting", "excel", "budgeting", "quickbooks",
            "taxation", "financial modeling", "accounts"
        ],
        "education": ["accounting", "finance", "commerce", "acca"],
        "signals": ["accountant", "finance analyst", "financial analyst"],
        "projects": [
            "Monthly Financial Reporting Workbook",
            "Budget and Cash Flow Analysis",
            "Financial Performance Dashboard"
        ],
        "roadmap": [
            "Strengthen accounting principles and spreadsheet skills.",
            "Practise financial reporting, budgeting and reconciliation.",
            "Explore financial analysis or accounting specialization."
        ]
    },
    "Digital Marketing Specialist": {
        "skills": [
            "digital marketing", "seo", "sem", "google ads",
            "social media marketing", "content marketing",
            "email marketing", "meta ads", "campaign management"
        ],
        "education": ["marketing", "business administration"],
        "signals": ["digital marketing specialist", "seo specialist"],
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
        "education": ["design", "graphic design", "interaction design"],
        "signals": ["ui designer", "ux designer", "ui/ux designer"],
        "projects": [
            "Mobile App Wireframes and Interactive Prototype",
            "Website Usability Review and Redesign",
            "User Research and Journey Mapping Case Study"
        ],
        "roadmap": [
            "Practise user research, wireframing and prototyping.",
            "Document design decisions in portfolio case studies.",
            "Explore product design or UX research."
        ]
    },
    "Teacher / Educator": {
        "skills": [
            "teaching", "lesson planning", "classroom management",
            "curriculum development", "assessment", "tutoring",
            "educational technology", "student assessment",
            "lesson plan", "instruction"
        ],
        "education": [
            "education", "b.ed", "m.ed", "teacher training",
            "education degree", "educational leadership"
        ],
        "signals": [
            "teacher", "teaching", "educator", "lecturer", "professor",
            "instructor", "school teacher", "academic coordinator",
            "lesson planning", "classroom management",
            "curriculum development", "teacher training"
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
            "medicine", "mbbs", "nursing", "pharmacy",
            "physiotherapy", "public health", "health sciences"
        ],
        "signals": ["medical doctor", "registered nurse", "healthcare professional"],
        "projects": [
            "Healthcare Education Resource for Patients",
            "Public Health Awareness Campaign",
            "De-identified Healthcare Data Summary"
        ],
        "roadmap": [
            "Build on your recognized qualification and supervised training.",
            "Document relevant clinical placements and certifications.",
            "Explore specializations suitable for your qualification and licensing."
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
            "biology", "biotechnology", "chemistry", "clinical laboratory"
        ],
        "signals": ["laboratory technician", "lab technician", "medical laboratory technologist"],
        "projects": [
            "Laboratory Quality Control Checklist",
            "Specimen Tracking Workflow Prototype",
            "Laboratory Safety and SOP Portfolio"
        ],
        "roadmap": [
            "Strengthen laboratory procedures, safety and documentation.",
            "Record supervised practical training and relevant certifications.",
            "Explore laboratory roles suitable for your qualification."
        ]
    },
    "Engineer": {
        "skills": [
            "engineering", "autocad", "solidworks", "matlab",
            "circuit design", "plc", "cad", "simulation",
            "mechanical design", "electrical design"
        ],
        "education": [
            "engineering", "mechanical engineering", "electrical engineering",
            "civil engineering", "chemical engineering"
        ],
        "signals": ["mechanical engineer", "electrical engineer", "civil engineer"],
        "projects": [
            "Engineering Design and Simulation Report",
            "Technical Drawing and CAD Portfolio",
            "Prototype Design with Testing Results"
        ],
        "roadmap": [
            "Identify the engineering discipline matching your degree.",
            "Build discipline-specific projects and technical documentation.",
            "Explore specialist engineering roles."
        ]
    },
    "Business Analyst": {
        "skills": [
            "business analysis", "requirements gathering", "process mapping",
            "stakeholder management", "user stories", "sql", "excel",
            "documentation", "business requirements"
        ],
        "education": [
            "business administration", "business analytics",
            "computer science", "information systems"
        ],
        "signals": ["business analyst", "requirements gathering", "process analysis"],
        "projects": [
            "Business Requirements Document",
            "Process Improvement Case Study",
            "Business KPI Dashboard"
        ],
        "roadmap": [
            "Learn requirements gathering and process documentation.",
            "Practise user stories, process maps and stakeholder communication.",
            "Build business analysis case studies and KPI reports."
        ]
    },
    "HR / Recruitment Specialist": {
        "skills": [
            "human resources", "recruitment", "talent acquisition",
            "interviewing", "employee relations", "hr management",
            "payroll", "onboarding"
        ],
        "education": ["human resources", "business administration", "management"],
        "signals": ["hr specialist", "recruiter", "talent acquisition"],
        "projects": [
            "Recruitment Tracking Dashboard",
            "Employee Onboarding Checklist",
            "Candidate Screening Workflow"
        ],
        "roadmap": [
            "Learn recruitment processes and HR documentation.",
            "Practise candidate tracking and interview coordination.",
            "Explore talent acquisition or HR operations."
        ]
    }
}

JOB_PROFILES = {
    career: profile["skills"]
    for career, profile in CAREER_PROFILES.items()
}

EDUCATION_KEYWORDS = {
    career: profile["education"]
    for career, profile in CAREER_PROFILES.items()
}


# =========================================================
# DATABASE AND MIGRATIONS
# =========================================================

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def ensure_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS resume_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_name TEXT,
                match_score REAL DEFAULT 0,
                skill_gap REAL DEFAULT 100,
                career_recommendation TEXT,
                matched_skills TEXT,
                missing_skills TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        existing_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(resume_analysis)"
            ).fetchall()
        }

        extra_columns = {
            "overall_score": "REAL DEFAULT 0",
            "detected_skills": "TEXT DEFAULT ''",
            "top_careers": "TEXT DEFAULT ''",
            "project_ideas": "TEXT DEFAULT ''",
            "resume_text": "TEXT DEFAULT ''"
        }

        for column, definition in extra_columns.items():
            if column not in existing_columns:
                connection.execute(
                    f"ALTER TABLE resume_analysis ADD COLUMN {column} {definition}"
                )


ensure_database()


def save_analysis(data):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO resume_analysis (
                resume_name, match_score, skill_gap,
                career_recommendation, matched_skills, missing_skills,
                overall_score, detected_skills, top_careers,
                project_ideas, resume_text
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["resume_name"],
            data["match_score"],
            data["skill_gap"],
            data["career_recommendation"],
            ", ".join(data["matched_skills"]),
            ", ".join(data["missing_skills"]),
            data["overall_score"],
            ", ".join(data["detected_skills"]),
            " | ".join(
                f'{item["name"]} ({item["score"]} points)'
                for item in data["top_careers"]
            ),
            " | ".join(data["project_ideas"]),
            data["resume_text"][:50000]
        ))
        return cursor.lastrowid


# =========================================================
# TEXT PROCESSING
# =========================================================

def normalize_text(text):
    text = (text or "").lower()
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def term_present(text, term):
    text = normalize_text(text)
    term = normalize_text(term)
    if not term:
        return False

    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def extract_resume_text(file_path):
    try:
        reader = PdfReader(file_path)

        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                return ""

        page_text = []
        for page in reader.pages:
            try:
                page_text.append(page.extract_text() or "")
            except Exception:
                continue

        return normalize_text("\n".join(page_text))

    except Exception as error:
        app.logger.exception("Resume PDF extraction failed: %s", error)
        return ""


def detect_skills(resume_text):
    text = normalize_text(resume_text)
    found = []

    all_skills = sorted(
        {
            skill
            for profile in CAREER_PROFILES.values()
            for skill in profile["skills"]
        },
        key=len,
        reverse=True
    )

    for skill in all_skills:
        if term_present(text, skill):
            if skill not in found:
                found.append(skill)

    return found


# =========================================================
# CAREER RECOMMENDATION
# =========================================================

def recommend_careers(resume_text):
    text = normalize_text(resume_text)
    ranked = []

    for career, profile in CAREER_PROFILES.items():
        matched_skills = [
            skill for skill in profile["skills"]
            if term_present(text, skill)
        ]

        education_hits = [
            item for item in profile["education"]
            if term_present(text, item)
        ]

        explicit_signals = [
            item for item in profile["signals"]
            if term_present(text, item)
        ]

        score = (
            len(explicit_signals) * 10
            + len(education_hits) * 5
            + len(matched_skills) * 2
        )

        if score > 0:
            ranked.append({
                "name": career,
                "score": score,
                "matched_skills": matched_skills,
                "education_evidence": education_hits,
                "career_evidence": explicit_signals,
                "projects": profile["projects"]
            })

    ranked.sort(
        key=lambda item: (
            item["score"],
            len(item["career_evidence"]),
            len(item["education_evidence"]),
            len(item["matched_skills"])
        ),
        reverse=True
    )

    top_careers = ranked[:2]

    if not top_careers:
        return {
            "top_careers": [],
            "career_recommendation":
                "Insufficient evidence for a reliable match",
            "career_roadmap": [
                "Add your qualification and field of study.",
                "Mention relevant professional skills and experience.",
                "Include projects, internships or achievements."
            ],
            "career_project_ideas": [
                "Build a practical project related to your field.",
                "Create a portfolio documenting your actual skills.",
                "Document project methods, tools and results."
            ]
        }

    primary_career = top_careers[0]["name"]
    primary_profile = CAREER_PROFILES[primary_career]

    return {
        "top_careers": top_careers,
        "career_recommendation": primary_career,
        "career_roadmap": primary_profile["roadmap"],
        "career_project_ideas": primary_profile["projects"]
    }


# =========================================================
# JOB MATCHING AND SKILL GAP
# =========================================================

def calculate_match(resume_text, required_skills):
    resume_text = normalize_text(resume_text)
    required_skills = list(dict.fromkeys(required_skills or []))

    if not required_skills:
        return 0.0, 100.0, [], []

    matched = [
        skill for skill in required_skills
        if term_present(resume_text, skill)
    ]
    missing = [
        skill for skill in required_skills
        if skill not in matched
    ]

    skill_match_percentage = len(matched) / len(required_skills) * 100

    # TF-IDF adds text similarity, but skill evidence remains important.
    text_similarity = 0.0
    if resume_text.strip():
        requirements_text = " ".join(required_skills)
        try:
            matrix = TfidfVectorizer().fit_transform([
                resume_text,
                requirements_text
            ])
            text_similarity = float(
                cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
            ) * 100
        except ValueError:
            text_similarity = 0.0

    match_score = round(
        (skill_match_percentage * 0.85) + (text_similarity * 0.15), 2
    )
    skill_gap = round(100 - skill_match_percentage, 2)

    return (
        max(0.0, min(100.0, match_score)),
        max(0.0, min(100.0, skill_gap)),
        matched,
        missing
    )


def calculate_overall_score(match_score, skill_gap):
    skill_score = max(0.0, min(100.0, 100.0 - float(skill_gap or 0)))
    match_score = max(0.0, min(100.0, float(match_score or 0)))
    return round((match_score * 0.60) + (skill_score * 0.40), 2)


def generate_project_ideas(top_careers, fallback_projects=None):
    ideas = []

    if top_careers:
        career = top_careers[0]["name"]
        profile = CAREER_PROFILES[career]
        projects = profile.get("projects", [])
        skills = profile.get("skills", [])[:5]
    else:
        career = "Explore your field"
        projects = fallback_projects or []
        skills = ["Subject knowledge", "Research", "Documentation"]

    for index in range(3):
        if index < len(projects):
            title = projects[index]
        else:
            title = f"Practical Portfolio Project {index + 1} for {career}"

        ideas.append({
            "title": title,
            "description": (
                f"Practise skills relevant to {career}. Document the "
                "methods, tools, and actual results of your project."
            ),
            "career": career,
            "level": "Beginner" if index == 0 else "Intermediate",
            "skills": skills
        })

    return ideas


# =========================================================
# INSIGHTS AND LEARNING RECOMMENDATIONS
# =========================================================

LEARNING_RECOMMENDATIONS = {
    "python": "Learn Python fundamentals, functions, OOP, file handling and data analysis.",
    "sql": "Practise SELECT, WHERE, JOINs, GROUP BY, subqueries and aggregate functions.",
    "excel": "Improve formulas, Pivot Tables, charts, lookup functions and data cleaning.",
    "power bi": "Learn dashboards, Power Query, data modelling and basic DAX.",
    "pandas": "Practise data cleaning, filtering, grouping, merging and analysis.",
    "numpy": "Learn arrays, indexing, slicing and numerical operations.",
    "teaching": "Practise lesson planning, teaching methods and student assessment.",
    "classroom management": "Learn classroom organisation, communication and student engagement.",
    "curriculum development": "Practise creating learning outcomes and structured lesson plans.",
    "html": "Practise semantic HTML and accessible page structure.",
    "css": "Learn responsive layouts, Flexbox and Grid.",
    "javascript": "Practise functions, DOM manipulation and asynchronous programming.",
    "machine learning": "Study model training, evaluation and data preparation.",
    "figma": "Practise wireframing, prototyping and documenting design decisions.",
    "cybersecurity": "Study networking, Linux, defensive security and safe lab practice.",
    "accounting": "Practise bookkeeping, reconciliations and financial reporting."
}


def build_insights(resume_text, detected_skills, missing_skills,
                   career_recommendation):
    text = normalize_text(resume_text)
    strengths = []
    improvements = []
    insights = []

    has_experience = any(term_present(text, term) for term in [
        "work experience", "professional experience", "employment history",
        "internship", "worked as", "experience"
    ])

    has_education = any(term_present(text, term) for term in [
        "education", "bachelor", "master", "degree", "university",
        "college", "b.sc", "bsc", "bs computer science"
    ])

    has_projects = any(term_present(text, term) for term in [
        "projects", "project experience", "portfolio", "academic project"
    ])

    if has_experience:
        strengths.append("Professional or practical experience is included.")
    if has_education:
        strengths.append("Educational background is represented.")
    if detected_skills:
        strengths.append(
            f"{len(detected_skills)} listed technical or professional skills were detected."
        )
    if has_projects:
        strengths.append("Project or portfolio information is included.")

    if not strengths:
        strengths.append("Resume text was extracted and reviewed.")

    if missing_skills:
        improvements.append(
            "Missing required skills: " + ", ".join(missing_skills) + "."
        )

    if not has_projects:
        improvements.append("No clearly mentioned projects were detected.")

    if not has_experience:
        improvements.append(
            "Add relevant experience, internships, volunteering or practical work."
        )

    if not has_education:
        improvements.append("Clearly list your qualification and institution.")

    if not detected_skills:
        improvements.append(
            "No recognised technical or professional skills were detected. "
            "Check whether the PDF contains selectable text."
        )

    if career_recommendation.startswith("Insufficient"):
        insights.append(
            "The resume did not provide enough evidence for a reliable career recommendation."
        )
    else:
        insights.append(
            f"Resume evidence most strongly matches: {career_recommendation}."
        )

    if missing_skills:
        insights.append("Consider learning the missing skills before applying.")
    if has_projects:
        insights.append("Describe your own role and measurable project results.")

    suggestions = [
        "Tailor your resume to the requirements of each job.",
        "Add skills only when you have genuinely learned or practised them.",
        "Include relevant projects, tools used and measurable results.",
        "Consider adding a GitHub profile containing relevant projects.",
        "Keep your professional LinkedIn profile updated."
    ]

    learning = []
    for skill in missing_skills:
        message = LEARNING_RECOMMENDATIONS.get(
            skill.lower(),
            f"Practise {skill} through a structured course and a practical project."
        )
        if message not in learning:
            learning.append(message)

    return {
        "strengths": strengths,
        "improvement_areas": improvements,
        "ai_insights": insights,
        "resume_suggestions": suggestions,
        "learning_recommendations": learning
    }


# =========================================================
# HELPERS FOR TEMPLATES
# =========================================================

def get_recent_analyses(limit=100):
    with get_connection() as connection:
        return connection.execute("""
            SELECT * FROM resume_analysis
            ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()


def get_analysis_by_id(analysis_id):
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM resume_analysis WHERE id = ?",
            (analysis_id,)
        ).fetchone()


def safe_render(template, **context):
    try:
        return render_template(template, **context)
    except Exception as error:
        app.logger.exception("Template rendering error: %s", error)
        return (
            f"Template error: {template}. "
            "Check that the template file exists in the templates folder."
        ), 500


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():
    return safe_render("index.html")


@app.route("/analyze")
def analyze_page():
    if os.path.isfile(os.path.join(BASE_DIR, "templates", "Analyze Resume.html")):
        return safe_render("Analyze Resume.html")
    return redirect(url_for("index"))


# =========================================================
# UPLOAD AND ANALYZE RESUME
# =========================================================

@app.route("/upload", methods=["POST"])
def upload_resume():
    uploaded_file = (
        request.files.get("resume")
        or request.files.get("resume_file")
        or request.files.get("file")
    )

    if not uploaded_file or not uploaded_file.filename:
        flash("Please select a PDF resume first.")
        return redirect(url_for("index"))

    original_name = secure_filename(uploaded_file.filename)

    if not original_name.lower().endswith(".pdf"):
        flash("Only PDF resumes are supported.")
        return redirect(url_for("index"))

    if not original_name:
        flash("Invalid filename.")
        return redirect(url_for("index"))

    # Avoid overwriting an earlier upload with the same filename.
    import uuid
    stored_name = f"{uuid.uuid4().hex}_{original_name}"
    file_path = os.path.join(UPLOAD_FOLDER, stored_name)

    try:
        uploaded_file.save(file_path)
        resume_text = extract_resume_text(file_path)

        if len(resume_text.strip()) < 20:
            flash(
                "Text could not be extracted from this PDF. "
                "It may be a scanned image. Try a text-based PDF."
            )
            return redirect(url_for("index"))

        detected_skills = detect_skills(resume_text)
        career_result = recommend_careers(resume_text)

        top_careers = career_result["top_careers"]
        career_recommendation = career_result["career_recommendation"]

        # Use the explicitly selected career/job if the form supplies one.
        selected_career = (
            request.form.get("target_career", "").strip()
            or request.form.get("career", "").strip()
        )

        if selected_career not in CAREER_PROFILES:
            selected_career = (
                career_recommendation
                if career_recommendation in CAREER_PROFILES
                else ""
            )

        # A supplied job description takes precedence over a career profile.
        job_description = (
            request.form.get("job_description", "").strip()
            or request.form.get("job_requirements", "").strip()
        )

        if job_description:
            required_skills = detect_skills(job_description)
            if not required_skills:
                # Avoid a misleading perfect match for an unrecognised description.
                required_skills = []
        elif selected_career:
            required_skills = JOB_PROFILES[selected_career]
        else:
            required_skills = []

        if required_skills:
            match_score, skill_gap, matched_skills, missing_skills = (
                calculate_match(resume_text, required_skills)
            )
        else:
            match_score = 0.0
            skill_gap = 100.0
            matched_skills = []
            missing_skills = []

        overall_score = calculate_overall_score(match_score, skill_gap)

        project_ideas = generate_project_ideas(
            top_careers,
            career_result["career_project_ideas"]
        )

        insight_result = build_insights(
            resume_text,
            detected_skills,
            missing_skills,
            career_recommendation
        )

        analysis_id = save_analysis({
            "resume_name": original_name,
            "match_score": match_score,
            "skill_gap": skill_gap,
            "career_recommendation": career_recommendation,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "overall_score": overall_score,
            "detected_skills": detected_skills,
            "top_careers": top_careers,
            "project_ideas": [item["title"] for item in project_ideas],
            "resume_text": resume_text
        })

        context = {
            "analysis_id": analysis_id,
            "resume_name": original_name,
            "match_score": match_score,
            "skill_gap": skill_gap,
            "skill_gap_percentage": skill_gap,
            "overall_score": overall_score,
            "career_recommendation": career_recommendation,
            "selected_career": selected_career,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "detected_skills": detected_skills,
            "found_skills": detected_skills,
            "top_careers": top_careers,
            "career_roadmap": career_result["career_roadmap"],
            "career_project_ideas": career_result["career_project_ideas"],
            "project_ideas": project_ideas,
            "strengths": insight_result["strengths"],
            "improvement_areas": insight_result["improvement_areas"],
            "ai_insights": insight_result["ai_insights"],
            "learning_recommendations": insight_result["learning_recommendations"],
            "resume_suggestions": insight_result["resume_suggestions"],
            "job_requirements": required_skills
        }

        return safe_render("result.html", **context)

    except Exception as error:
        app.logger.exception("Resume analysis failed: %s", error)
        flash("Resume analysis failed. Check the terminal for the error.")
        return redirect(url_for("index"))


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():
    analyses = get_recent_analyses(200)
    return safe_render(
        "history.html",
        analyses=analyses,
        history=analyses,
        records=analyses
    )


@app.route("/candidate/<int:analysis_id>")
@app.route("/candidate_details/<int:analysis_id>")
def candidate_details(analysis_id):
    record = get_analysis_by_id(analysis_id)

    if record is None:
        flash("Analysis record not found.")
        return redirect(url_for("history"))

    return safe_render(
        "candidate_details.html",
        candidate=record,
        analysis=record,
        record=record
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():
    analyses = get_recent_analyses(10000)

    total_candidates = len(analyses)
    average_match = (
        round(sum(float(row["match_score"] or 0) for row in analyses) / total_candidates, 2)
        if total_candidates else 0
    )
    average_gap = (
        round(sum(float(row["skill_gap"] or 0) for row in analyses) / total_candidates, 2)
        if total_candidates else 0
    )

    career_counts = Counter(
        row["career_recommendation"] or "Not available"
        for row in analyses
    )

    career_labels = list(career_counts.keys())
    career_values = list(career_counts.values())

    return safe_render(
        "dashboard.html",
        analyses=analyses[:20],
        total_candidates=total_candidates,
        total_resumes=total_candidates,
        average_match=average_match,
        avg_match=average_match,
        average_gap=average_gap,
        avg_skill_gap=average_gap,
        career_labels=career_labels,
        career_values=career_values,
        career_counts=dict(career_counts)
    )


# =========================================================
# CANDIDATE RANKING
# =========================================================

@app.route("/ranking")
def ranking():
    analyses = get_recent_analyses(10000)

    ranked_candidates = sorted(
        analyses,
        key=lambda row: (
            float(row["overall_score"] or 0),
            float(row["match_score"] or 0)
        ),
        reverse=True
    )

    return safe_render(
        "ranking.html",
        candidates=ranked_candidates,
        ranked_candidates=ranked_candidates,
        analyses=ranked_candidates
    )


# =========================================================
# ADMIN / DELETE
# =========================================================


@app.route("/admin")
def admin():
    analyses = get_recent_analyses(500)

    candidates = []

    for item in analyses:
        candidate = dict(item)

        candidate["id"] = candidate.get("id", "")
        candidate["filename"] = (
            candidate.get("filename")
            or candidate.get("resume_name")
            or candidate.get("resume_filename")
            or "Unknown Resume"
        )

        match_score = candidate.get("match_score") or 0
        skill_gap = candidate.get("skill_gap") or 0

        try:
            match_score = float(match_score)
        except (ValueError, TypeError):
            match_score = 0

        try:
            skill_gap = float(skill_gap)
        except (ValueError, TypeError):
            skill_gap = 0

        candidate["match_score"] = match_score
        candidate["skill_gap"] = skill_gap
        candidate["overall_score"] = round(
            (match_score + (100 - skill_gap)) / 2, 2
        )

        candidate["recommended_career"] = (
            candidate.get("recommended_career")
            or candidate.get("career_recommendation")
            or "Not determined"
        )

        candidates.append(candidate)

    candidates.sort(
        key=lambda item: item["overall_score"],
        reverse=True
    )

    return safe_render(
        "admin.html",
        candidates=candidates,
        analyses=analyses,
        records=analyses,
        total_candidates=len(candidates)
    )



@app.route("/delete/<int:analysis_id>", methods=["POST", "GET"])
def delete_analysis(analysis_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM resume_analysis WHERE id = ?",
            (analysis_id,)
        )

    flash("Analysis record deleted.")
    return redirect(url_for("history"))


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(413)
def file_too_large(error):
    flash("The uploaded file is too large. Maximum size is 10 MB.")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    return "Page not found. Please return to the home page.", 404


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
