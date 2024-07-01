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

def format_output(result):
    if isinstance(result, list):
        if len(result) == 0:
            return "No results found."
        if len(result) == 1 and isinstance(result[0], tuple) and len(result[0]) == 1:
            # Single value result like [(66,)]
            return result[0][0]
        if all(isinstance(item, tuple) for item in result):
            if all(len(item) == 1 for item in result):
                # Single column result
                return [item[0] for item in result]
            else:
                # Multiple columns
                return pd.DataFrame(result)
    return result  # Return as is if it doesn't match expected formats

# Streamlit UI
st.title("AI SQL Query Generator")

user_question = st.text_input("Enter your question about the database:")

if st.button("Generate SQL and Execute"):
    if user_question:
        generated_sql, query_result = connects_lang(user_question)

        st.subheader("Generated SQL Query:")
        st.code(generated_sql, language="sql")

        st.subheader("Query Result:")
        formatted_result = format_output(query_result)
        
        if isinstance(formatted_result, pd.DataFrame):
            st.dataframe(formatted_result)
        elif isinstance(formatted_result, list):
            if len(formatted_result) == 1:
                st.metric("Result", formatted_result[0])
            else:
                st.write(formatted_result)
        elif isinstance(formatted_result, (int, float, str)):
            st.metric("Result", formatted_result)
        else:
            st.write(formatted_result)

    else:
        st.warning("Please enter a question.")