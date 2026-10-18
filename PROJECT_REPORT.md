# AI Resume Analyzer & Job Matching System

## 1. Introduction

Recruiters may receive many resumes for one vacancy, making manual review time-consuming. The AI Resume Analyzer is a web application prototype that extracts text from PDF resumes and compares the content with a target job profile. It presents an estimated match score, required skills found, missing skills, career recommendations, and improvement suggestions.

## 2. Objectives

- Automate initial resume text extraction from PDF files.
- Estimate alignment between a resume and a target job profile.
- Identify matched and missing technical skills.
- Recommend a potential career path based on resume keywords.
- Store analyses so users can review, compare, and rank candidates.
- Present results through a simple browser-based interface.

## 3. Technology stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Resume extraction | pypdf |
| Text matching | scikit-learn TF-IDF and cosine similarity |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Runtime | Local Python web server |

## 4. System workflow

1. The user opens the web application and uploads a PDF resume.
2. The server validates the file and extracts text from its pages.
3. The text is compared with the configured job description using TF-IDF/cosine similarity.
4. Required technical skills are detected with keyword patterns.
5. The system calculates match, skill-gap, and overall scores.
6. Career recommendation and improvement suggestions are generated from detected keywords.
7. The analysis is saved to SQLite.
8. The result page displays the analysis; the dashboard, history, ranking, and candidate pages use saved records.

## 5. Scoring approach

Let `C` be required-skill coverage (percentage), `T` be TF-IDF similarity (percentage), and `G` be the skill-gap percentage.

- Match score = `0.60 × C + 0.40 × T`
- Skill gap = `(number of missing required skills / total required skills) × 100`
- Overall candidate score = `0.60 × Match score + 0.40 × (100 − G)`

The current Data Analyst profile checks Python, SQL, Excel, Power BI, Pandas, and NumPy. These weights are transparent heuristics for a classroom prototype, not a validated hiring assessment.

## 6. Functional modules

- **Resume upload and parsing:** accepts PDF files, extracts text, and handles unreadable or image-only PDFs with a user-facing error.
- **Resume matching:** calculates a hybrid score using skill coverage and text similarity.
- **Skill-gap analysis:** displays matched and missing skills.
- **Career recommendation:** scores several career paths using keyword rules.
- **Insights and suggestions:** presents strengths, weaknesses, learning topics, and resume improvement tips.
- **History and dashboard:** stores analyses and summarizes past results.
- **Ranking and recruiter views:** orders candidates by overall score and provides candidate details.

## 7. Database design

The `resume_analysis` table stores an auto-incrementing ID, resume filename, match score, skill gap, career recommendation, matched skills, missing skills, and analysis timestamp. SQL queries use parameterized values for record insertion and deletion.

## 8. Testing checklist

| Test | Expected result |
|---|---|
| Open home page | Resume upload form is displayed |
| Submit without a file | Helpful validation message is shown |
| Upload a non-PDF file | Request is rejected |
| Upload a valid text-based PDF | Scores and insights are displayed |
| Upload a scanned PDF without extractable text | User is asked to upload a text-based PDF |
| Open history after analysis | Saved analysis appears in the table |
| Open dashboard | Counts and averages render |
| Open ranking page | Candidates are ordered by overall score |
| Open candidate details | Correct record details are shown |
| Delete a candidate from admin page | Record is removed from SQLite |
| Upload a file larger than 10 MB | Upload is rejected with a size message |

## 9. Limitations and future enhancements

- Skill detection is keyword-based and may miss equivalent skills expressed in unusual wording.
- TF-IDF is lexical similarity, not deep semantic understanding.
- Scanned PDFs need OCR support.
- The current target profile and weights are configured in source code.
- Authentication, role-based authorization, audit logging, and production deployment security can be added in a future version.
- Future improvements could include job-description input, configurable skill sets, OCR, model evaluation on labeled resumes, and recruiter login.

## 10. Conclusion

The application demonstrates an end-to-end resume screening workflow with PDF parsing, hybrid matching, skill-gap analysis, career recommendations, persistent storage, dashboards, and candidate ranking. It is intended as an educational prototype that can be extended with more advanced NLP and security controls.
