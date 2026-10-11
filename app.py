from flask import Flask, render_template, request, redirect
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

def save_analysis(
    resume_name,
    match_score,
    skill_gap,
    career_recommendation,
    matched_skills,
    missing_skills
):

    connection = sqlite3.connect("resume_analyzer.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO resume_analysis
        (
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
        matched_skills,
        missing_skills
    ))

    connection.commit()

    connection.close()


# =========================================================
# Home Page
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# Upload Resume
# =========================================================

@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:

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

    overall_score = calculate_overall_score(
        match_score,
        skill_gap_percentage
    )


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

        improvement_suggestions.append(
            "Consider adding a professional LinkedIn profile."
        )


    # =====================================================
    # Save Analysis
    # =====================================================

    save_analysis(
        resume_name,
        match_score,
        skill_gap_percentage,
        career_recommendation,
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

        improvement_suggestions=improvement_suggestions
    )


# =========================================================
# Resume History
# =========================================================

@app.route("/history")
def history():

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
# =========================================================

@app.route("/ranking")
def ranking():

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


    return render_template(
        "ranking.html",
        candidates=ranked_candidates
    )


# =========================================================
# Dashboard
# =========================================================

@app.route("/dashboard")
def dashboard():

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
    )


# =========================================================
# Admin / Recruiter Panel
# =========================================================

@app.route("/admin")
def admin():

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

        candidates=ranked_candidates
    )


# =========================================================
# Candidate Details
# =========================================================

@app.route("/candidate/<int:candidate_id>")
def candidate_details(candidate_id):

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

        candidate_rank=candidate_rank
    )


# =========================================================
# Delete Candidate
# =========================================================

@app.route("/delete/<int:candidate_id>", methods=["POST"])
def delete_candidate(candidate_id):

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


    return redirect("/admin")


# =========================================================
# Run Application
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )