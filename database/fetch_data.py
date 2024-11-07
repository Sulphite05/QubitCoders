import sqlite3
import pandas as pd
import os


def get_db_connection():
    base_path = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_path, "students.db")  # to resolve conflicting streamlit and db paths
    conn = sqlite3.connect(db_path)
    return conn


def fetch_student_rankings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
                SELECT full_name, s.username, batch, problems_solved, contest_count, contest_rating
                FROM STUDENT_INFO s
                JOIN PROBLEMS_SOLVED p ON s.username = p.username
                JOIN CONTEST_INFO c ON s.username = c.username
                ORDER BY contest_rating DESC, problems_solved DESC
            """)
    rows = cur.fetchall()
    conn.close()
    return rows


def save_rankings():
    raw_data = fetch_student_rankings()
    column_names = ["Full Name", "Username", "Batch", "Problems Solved", "Contest Count", "Contest Rating"]
    df = pd.DataFrame(raw_data, columns=column_names)
    base_path = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.join(base_path, "student_rankings.csv")
    df.to_csv(csv_path, index=False)


def fetch_table():
    base_path = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.join(base_path, "student_rankings.csv")
    if not os.path.exists(csv_path):
        save_rankings()
    df = pd.read_csv(csv_path)
    df.index = range(1, len(df) + 1)
    df['Batch'] = df['Batch'].astype(str)
    return df
