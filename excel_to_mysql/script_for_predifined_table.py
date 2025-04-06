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
file_path = "C:/Users/user/Desktop/texts.xlsx"
df = pd.read_excel(file_path, header=2, usecols="B:D")

print(df.columns)

# connect to db
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# SQL-query for inserting data
insert_query = """
INSERT INTO predefined_responses (command, response_text, language, created_at)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE response_text = VALUES(response_text), created_at = VALUES(created_at)
"""

for _, row in df.iterrows():
    command = row["command"]
    response_text = row["response_text"]
    language = row["language"]
    created_at = datetime.now()

    cursor.execute(insert_query, (command, response_text, language, created_at))

conn.commit()
cursor.close()
conn.close()

print("Data loaded successfully in DB.")
