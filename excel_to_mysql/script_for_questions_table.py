import pandas as pd
import mysql.connector
from datetime import datetime
from decouple import config

# MySQL settings
DB_CONFIG = {
    "host": config('db_host'),
    "user": config('db_user'),
    "password": config('db_password'),
    "database": config('db_name'),
    "port": config('db_port')
}

# Data from Excel
file_path = "./texts(1).xlsx"
df = pd.read_excel(file_path, header=2, usecols="B:D") # columns: question, answer, language

print("Excel columns:", df.columns.tolist())

# connect to db
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("connection established1")
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# SQL-query to insert into question_answer table
insert_query = """
INSERT INTO question_answer (question, answer, language, created_at, updated_at, embedding)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE question = VALUES(question), answer = VALUES(answer), language = VALUES(language), updated_at = VALUES(updated_at)
"""

now = datetime.now()
for _, row in df.iterrows():
    question = row["question"]
    answer = row["answer"]
    language = row["language"]
    created_at = now
    updated_at = now
    embedding = None

    cursor.execute(insert_query, (question, answer, language, created_at, updated_at, embedding))

conn.commit()
cursor.close()
conn.close()

print("Data loaded successfully into question_answer table.")
