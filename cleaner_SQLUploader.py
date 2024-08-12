import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import mysql.connector
from mysql.connector import Error
import os

df = pd.read_excel("path-of-file", header=None)

cleaned = df.drop([0, 24, 25, 26]).dropna(axis=1, how='all').reset_index(drop=True)

output_file_path = "path-to-save"

savedCopy = cleaned.to_excel(output_file_path, index=False, header=False)

engine = create_engine('mysql+mysqlconnector://user:passowrd@localhost:port/')

try:
    
    with engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS dbname"))
        print("Database created successfully.")
except SQLAlchemyError as e:
    print(f"An error occurred: {e}")


tableEngine = create_engine('mysql+mysqlconnector://user:passowrd@localhost:port/dbname')
directory_path = "file-path"

def uploadSql(path):
    try: 
        file = pd.read_excel(path, header=None)
        tableName = os.path.splitext(os.path.basename(path))[0]
        file.to_sql(name=tableName, con=tableEngine, if_exists='replace', index=False)
        print(f"Data from {path} inserted into table {tableName}.")

    except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

for filename in os.listdir(directory_path):
     if filename.endswith('.xlsx'):
          file_path = os.path.join(directory_path, filename)
          uploadSql(file_path)