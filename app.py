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
st.title("Applying Natural Language to SQL Queries")
st.text("This app uses OpenAI's GPT-3 to generate SQL queries based on user questions. The generated SQL queries are then executed on a PostgreSQL database.")

# Create the full dataframe with the provided data
data = {
    'Customer_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'first_name': ["Francoise", "Kendra", "Lourdes", "Hannah", "Tom", "Queenie", "Hui", "Josefa", "Lea", "Paola"],
    'last_name': ["Rautenstrauch", "Loud", "Bauswell", "Edmison", "Loeza", "Kramarczyk", "Portaro", "Opitz", "Steinhaus", "Vielma"],
    'company_name': ["Riebesell, H F Jr", "Deloitte & Touche", "Oklahoma Neon Inc", "M B A Paint Stores", "Sheraton Shreveport Hotel", "Goeman Wood Products Inc", "A Storage Inn Of Gloucester", "Norman Gale Isuzu", "James, Christopher Esq", "Congress Title"],
    'address': ["2335 Canton Hwy #6", "6 Arch St #9757", "9547 Belmont Rd #21", "73 Pittsford Victor Rd", "447 Commercial St Se", "47 Garfield Ave", "3 Mill Rd", "136 W Grand Ave #3", "80 Maplewood Dr #34", "58 Hancock St"],
    'city': ["Windsor", "Alcida", "Belleville", "Vancouver", "LIle-Perrot", "Swift Current", "Baker Brook", "Delhi", "Bradford", "Aurora"],
    'province': ["ON", "NB", "ON", "BC", "QC", "SK", "NB", "ON", "ON", "ON"],
    'postal': ["N8N 3N2", "E8J 2C4", "K8P 1B3", "V5Z 3K2", "J7V 4T4", "S9H 4V2", "E7A 1T3", "N4B 1C4", "L3Z 2S4", "L4G 2J7"],
    'phone1': ["519-569-8399", "506-363-1526", "613-903-7043", "604-334-3686", "514-487-6096", "306-421-5793", "506-827-7755", "519-788-7645", "905-618-8258", "905-456-1117"],
    'phone2': ["519-978-6179", "506-932-4472", "613-638-6682", "604-692-7694", "514-727-4760", "306-302-7591", "506-276-4830", "519-526-3721", "905-651-3298", "905-263-7711"],
    'email': ["francoise.rautenstrauch@rautenstrauch.com", "kloud@gmail.com", "lourdes_bauswell@aol.com", "hannah@yahoo.com", "tom.loeza@gmail.com", "queenie.kramarczyk@kramarczyk.org", "hui_portaro@cox.net", "josefa.opitz@opitz.org", "lsteinhaus@cox.net", "paola_vielma@aol.com"],
    'web': ["http://www.riebesellhfjr.com", "http://www.deloittetouche.com", "http://www.oklahomaneoninc.com", "http://www.mbapaintstores.com", "http://www.sheratonshreveporthotel.com", "http://www.goemanwoodproductsinc.com", "http://www.astorageinnofgloucester.com", "http://www.normangaleisuzu.com", "http://www.jameschristopheresq.com", "http://www.congresstitle.com"]
}

df = pd.DataFrame(data)

# Pagination logic
page = st.sidebar.selectbox("Select Page", ["Page 1", "Page 2"])

if page == "Page 1":
    st.write("Page 1: Showing first 5 entries")
    st.dataframe(df.head(5))
else:
    st.write("Page 2: Showing next 5 entries and remaining will not display")
    st.dataframe(df.iloc[5:])

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