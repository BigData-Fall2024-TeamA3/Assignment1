import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_model_answer(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=100
    )
    return response.choices[0].text.strip()