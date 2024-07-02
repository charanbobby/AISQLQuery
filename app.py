import streamlit as st
from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import pandas as pd

def connects_lang(user_question):
    load_dotenv()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    PG_DB_URL = os.environ.get('PG_DB_URL')

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    db = SQLDatabase.from_uri(PG_DB_URL)
    llm = OpenAI(temperature=0)

    # Create the SQL query chain
    chain = create_sql_query_chain(llm, db)
    
    # Function to execute SQL and return results
    def run_query(query):
        return db.run(query)

    # Generate SQL query
    sql_query = chain.invoke({"question": user_question})

    # Execute the query
    result = run_query(sql_query)

    return sql_query, result


# Streamlit UI
st.title("AI SQL Query Generator")

user_question = st.text_input("Enter your question about the database:")

if st.button("Generate SQL and Execute"):
    if user_question:
        generated_sql, query_result = connects_lang(user_question)

        st.subheader("Generated SQL Query:")
        st.code(generated_sql, language="sql")

        st.subheader("Query Result:")
        st.write(query_result)

    else:
        st.warning("Please enter a question.")