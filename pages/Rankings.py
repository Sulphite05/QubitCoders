import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(
    page_title="LeetCode Rankings",
    page_icon="💻"
)

st.title("LeetCode Rankings 💻")

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(base_path, "students.db")    # to resolve conflicting streamlit and db paths
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
cur.execute("SELECT username FROM CONTEST_INFO")
cur.execute("""
            SELECT full_name, s.username, batch, problems_solved, contest_count, contest_rating
            FROM STUDENT_INFO s
            JOIN PROBLEMS_SOLVED p ON s.username = p.username
            JOIN CONTEST_INFO c ON s.username = c.username
            ORDER BY contest_rating DESC, problems_solved DESC
        """)

rows = cur.fetchall()
conn.close()
column_names = ["Full Name", "Username", "Batch", "Problems Solved", "Contest Count", "Contest Rating"]
df = pd.DataFrame(rows, columns=column_names, index=range(1, len(rows) + 1))
st.table(df)




# username = "sulphite"
# r = requests.get(f'https://leetcodeapi-v1.vercel.app/contest/{username}')
# print(r.json())

# username = "sulphite"
# r = requests.get(f'https://leetcodeapi-v1.vercel.app/contest/{username}')
# print(r.json())
