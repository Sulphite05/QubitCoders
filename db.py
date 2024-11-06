import sqlite3
import requests
import csv

conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS STUDENT_INFO
                (username TEXT PRIMARY KEY,
                full_name TEXT,               
                batch TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS PROBLEMS_SOLVED
                (username TEXT PRIMARY KEY, 
                problems_solved INTEGER, 
                easy INTEGER, 
                medium INTEGER, 
                hard INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS CONTEST_INFO
                (username TEXT PRIMARY KEY, 
                contest_count INTEGER, 
                contest_rating FLOAT)''')


## Uncomment to insert/update new user data in STUDENT_INFO Table
# with open('data.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)
#
#     for row in csv_reader:
#         cur.execute('INSERT OR REPLACE INTO STUDENT_INFO (full_name, username, batch) VALUES (?, ?, ?)', row)
# conn.commit()


## Uncomment to insert/update new contest/submission data in the CONTEST_INFO and PROBLEMS_SOLVED table
# cur.execute('SELECT username FROM STUDENT_INFO')
# rows = cur.fetchall()
#
#
# for row in rows:
#     username = row[0]
#     try:
#         r = requests.get(f'https://leetcodeapi-v1.vercel.app/contest/{username}')
#         data = r.json()
#         contest_data = (username, data['userContestDetails']['attendedContestsCount'],
#                         data['userContestDetails']['rating'])
#         cur.execute('INSERT OR REPLACE INTO CONTEST_INFO (username, contest_count, contest_rating) '
#                     'VALUES (?, ?, ?)', contest_data)
#
#     except KeyError:
#         cur.execute('INSERT OR REPLACE INTO CONTEST_INFO (username, contest_count, contest_rating) '
#                     'VALUES (?, ?, ?)', (username, 0, 0))
#
#     try:
#         r = requests.get(f'https://leetcodeapi-v1.vercel.app/questions/{username}')
#         data = r.json()
#         submission_data = (username, data['All'], data['Easy'], data['Medium'], data['Hard'])
#         cur.execute('INSERT OR REPLACE INTO PROBLEMS_SOLVED (username, problems_solved, easy, medium, hard) '
#                     'VALUES (?, ?, ?, ?, ?)', submission_data)
#
#     except KeyError:
#         cur.execute('INSERT OR REPLACE INTO PROBLEMS_SOLVED (username, problems_solved, easy, medium, hard) '
#                     'VALUES (?, ?, ?, ?, ?)', (username, 0, 0, 0, 0))
# conn.commit()

cur.execute('SELECT * FROM student_info')
rows1 = cur.fetchall()
cur.execute('SELECT * FROM problems_solved')
rows2 = cur.fetchall()
print(rows1, rows2)
conn.close()
