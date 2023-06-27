import os
from apikey import apikey

import streamlit as st 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain , SimpleSequentialChain
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY'] = apikey

st.title('scf gpt creator')


prompt = st.text_input('enter your chat here')



# prompt template

title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'tell about finance {topic}'
)


script_template = PromptTemplate(
    input_variables = ['title'],
    template = 'what is supply chain finance{title}'
)



## llm 

llm = OpenAI(temperature = 0.9)

# llm chain

title_chain = LLMChain(
    llm = llm,
    prompt = title_template , verbose = True
)

script_chain = LLMChain(
    llm = llm,
    prompt = title_template , verbose = True
)


seq_chain = SimpleSequentialChain(
    chains = [title_chain,script_chain] , verbose = True 
)

# show response to screen if prompt
if prompt:
    resp = seq_chain.run(prompt)
    st.write(resp)

