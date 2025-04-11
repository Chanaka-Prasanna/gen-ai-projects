import langchain
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import sqlite3

load_dotenv()

# configure our api
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# FUNCTION TO LOAD THE GEMINI MODEL AND PROVIDE SQL QUERY AS RESPONSE

def get_response(question,prompt):
    model=genai.GenerativeModel('gemini-2.0-pro-exp-02-05')
    response=model.generate_content([prompt,question])
    return response.text

# Retrive the queary from the sql database
def read_db(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)

    return rows

prompt = '''
You are an expert in converting English questions to SQL queries!  

The SQL database has the name STUDENT and has the following columns: NAME, CLASS, SECTION, and MARKS.  

- Ensure that `NAME` and `CLASS` fields have each word capitalized manually when constructing the query.  
- Ensure that `SECTION` is always in uppercase.  

Don't use the functions for that. Just capitalize it by you when adding the names,sections or classes

Example 1: How many entries of records are present?  
The SQL command will be: SELECT COUNT(*) FROM STUDENT;  

Example 2: Tell me all the students studying in Data Science class?  
The SQL command will be: SELECT * FROM STUDENT WHERE CLASS = "Data Science";  

Example 3: Show all students in machine learning section a.  
User input: Show all students in machine learning section a.  
The SQL command will be: SELECT * FROM STUDENT WHERE CLASS = "Machine Learning" AND SECTION = "A";  

Example 4: Need all marks for student called chanaka.  
User input: Need all marks for student called chanaka.  
The SQL command will be: SELECT MARKS FROM STUDENT WHERE NAME = "Chanaka";  

Now, use this structure to generate an SQL query based on the following user request:  

Make sure not to add ``` in the beginning or end and do not include the word "sql" in the query.  

User request: {user_input}  

'''




# Streamlit app
st.set_page_config(page_title="SQL data retriever in text")
st.header("App to retrive SQL data ")

question=st.text_input("Input: ",key='input')
submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_response(question,prompt)
    print(response)
    data=read_db(response,'student.db')
    st.subheader("The response is ")
    for row in data:
        print(row)
        st.write(row)
