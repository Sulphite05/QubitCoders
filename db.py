import sqlite3

conn = sqlite3.connect("students.db")
cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS STUDENT_INFO
                (username TEXT PRIMARY KEY,
                first_name TEXT, 
                last_name TEXT,                 
                batch TEXT, 
                roll_number TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS PROBLEMS_SOLVED
                (username TEXT PRIMARY KEY, 
                problems_solved INTEGER, 
                easy INTEGER, 
                medium INTEGER, 
                hard INTEGER,
                ranking INT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS CONTEST_INFO
                (username TEXT PRIMARY KEY, 
                contest_count INTEGER, 
                contest_rating FLOAT)''')

conn.close()
