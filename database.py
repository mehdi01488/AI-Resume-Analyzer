import sqlite3


def create_database():

    connection = sqlite3.connect("resume_analyzer.db")

    cursor = connection.cursor()

    cursor.execute("""
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


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")