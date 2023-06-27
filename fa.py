from fastapi import FastAPI
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from dotenv import load_dotenv
import os

app = FastAPI()




def connects_lang():
    load_dotenv()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    PG_DB_URL = os.environ.get('PG_DB_URL')

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    db = SQLDatabase.from_uri(PG_DB_URL)
    llm = OpenAI(temperature=0)

    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    # try:
    return db_chain.run("what is the exchage rate of INR")
    # except Exception:
    #     return "sorry i couldn't find matching data , please try again or give more explanation"
    


@app.get('/')
async def root():
    return {"message" : "hello world" , "data" : connects_lang()}