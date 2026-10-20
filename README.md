<<<<<<< HEAD
# AI Resume Analyzer & Job Matching System

A Flask web application that analyzes text-based PDF resumes against a configurable project target role (currently Data Analyst), estimates job alignment, identifies missing skills, recommends career paths, and stores analysis history in SQLite.

## Main features

- PDF resume upload and text extraction with file-type and size checks
- Hybrid resume matching score: 60% required-skill coverage + 40% TF-IDF text similarity
- Skill-gap calculation and matched/missing skill lists
- Rule-based career recommendation (Data Analyst, Data Scientist, ML Engineer, BI/Data Analyst, Web Developer)
- Candidate strengths, weaknesses, learning recommendations, and improvement suggestions
- SQLite analysis history
- Dashboard with aggregate statistics and recent analyses
- Candidate ranking and individual candidate details
- Admin/recruiter view and candidate deletion
- Responsive HTML/CSS templates

## Run on Windows / VS Code

1. Extract the ZIP file.
2. Open the extracted `AI_Resume_Project` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt instead:

   ```bat
   venv\Scripts\activate.bat
   ```

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the application:

   ```powershell
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in your browser.

## Pages

- `/` — Upload a resume
- `/dashboard` — Analysis statistics and recent records
- `/history` — Previous resume analyses
- `/ranking` — Candidates ordered by overall score
- `/admin` — Recruiter/admin overview
- `/candidate/<id>` — Candidate details

## Scoring method

- **Skill coverage** = matched required skills / total required skills × 100
- **Match score** = 60% of skill coverage + 40% of TF-IDF text similarity
- **Skill gap** = missing required skills / total required skills × 100
- **Overall candidate score** = 60% of match score + 40% of (100 − skill gap)

Scores are estimates based on the configured target role and keyword/text overlap. They are not a guarantee of hiring suitability and are not produced by a trained large language model.

## Current target role

The included configuration targets **Data Analyst** and checks Python, SQL, Excel, Power BI, Pandas, and NumPy. To customize the role, update `JOB_DESCRIPTION`, `REQUIRED_SKILLS`, and the skill-pattern/recommendation logic in `app.py`.

## Notes

- Upload a text-based PDF. Scanned/image-only PDFs may not contain extractable text and require OCR, which is not included.
- The application limits uploads to 10 MB.
- The SQLite database is created automatically on first run.
- Existing resume PDFs and the old database are intentionally excluded from this submission ZIP to avoid sharing personal data. Keep your original folder as a backup if you need previous analysis records.
- This is a university project/demo. Authentication and production deployment hardening are not included; do not expose the admin/delete routes to the public internet as-is.
=======
# AI-Resume-Analyzer
AI-Based Resume Screening and Job Matching System
>>>>>>> e315c9e2baa5322026f18d7cd5b00269b787a763
