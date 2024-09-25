import streamlit as st
import boto3
import pandas as pd
import json
import io
import openai
from dotenv import load_dotenv
import os
import pathlib
from sqlalchemy import create_engine, text

env_path = pathlib.Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

openai.api_key = os.getenv('OPENAI_API_KEY')

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

# Initialize the S3 client using boto3
s3 = boto3.client('s3')
bucket_name = 'bigdatadamg7245'
s3_file_key = 'staging/2023/validation/metadata.jsonl'


# Function to insert or update data using raw SQL
def insert_or_update_metadata(task_id, task_level, direct_response, annotator_response):
    with engine.connect() as conn:
        try:
            # Check if the task_id already exists
            select_query = text(f"SELECT task_id FROM ai.metadata WHERE task_id = '{task_id}'")
            print(f"{select_query}")
            result = conn.execute(select_query, {'task_id':task_id}).fetchone()
            print(result)
            if result:
                # If task_id exists, update the record
                update_query = text(f"""
                    UPDATE ai.metadata
                    SET direct_response = case when '{direct_response}' = '-1' then direct_response else '{direct_response}' end, 
                        annotator_response = '{annotator_response}' 
                    WHERE task_id = '{task_id}'
                """)
                conn.execute(update_query, {'task_id' : task_id, 'direct_response' : '1' if direct_response else '0', 'annotator_response' : '1' if annotator_response else '0'})
                print(update_query)
                st.success(f"Task {task_id} updated successfully.")
                conn.commit()
            else:
                # If task_id doesn't exist, insert a new record
                insert_query = text(f"""
                    INSERT INTO ai.metadata (task_id, task_level)
                    VALUES ('{task_id}', '{task_level}')
                """)
                conn.execute(insert_query, {'task_id':task_id, 'task_level':task_level})
                st.success(f"Task {task_id} inserted successfully.")
                conn.commit()
        except Exception as e:
            st.error(f"Error executing SQL query: {e}")
            conn.rollback()


# Function to query OpenAI model with a selected question
def ask_openai(question, metadata=None):
    try:
        if metadata:
            prompt = f"Question: {question}\nAnnotator Metadata: {json.dumps(metadata)}"
        else:
            prompt = f"Question: {question}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt+"provide only final answer"}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error querying OpenAI: {e}")
        return None

# Function to fetch the .jsonl file from S3
def load_jsonl_from_s3(bucket_name, s3_file_key):
    try:
        file_obj = s3.get_object(Bucket=bucket_name, Key=s3_file_key)
        
        file_content = file_obj['Body'].read().decode('utf-8')
        
        json_lines = [json.loads(line) for line in file_content.strip().split('\n')]
        
        df = pd.DataFrame(json_lines)
        
        return df
    except Exception as e:
        st.error(f"Error loading data from S3: {e}")
        return None

# Streamlit app layout
st.title("Ask Anything")

# Load the metadata from S3
metadata_df = load_jsonl_from_s3(bucket_name, s3_file_key)

if metadata_df is not None:
    questions = metadata_df['Question'].tolist()
    
    selected_question = st.selectbox("Choose a Question", options=questions)
    
    selected_task = metadata_df[metadata_df['Question'] == selected_question].iloc[0]
    annotator_metadata = selected_task['Annotator Metadata']
    task_level = selected_task['Level']
    task_id = selected_task['task_id']
    final_answer = selected_task['Final answer']
    st.write(f"Expected Output : {final_answer}")

    if st.button("Submit"):
        if selected_question:
            with st.spinner("Waiting for OpenAI response..."):
                
                openai_response = ask_openai(selected_question)
                insert_or_update_metadata(task_id, task_level, '1' if openai_response.lower() == final_answer else '0', '0')
                if openai_response:

                    st.write(f"OpenAI Response: {openai_response}")
                else:
                    st.error("Failed to get a response from OpenAI.")
        else:
            st.error("Please select a question first.")
    
    if st.button("Try Again"):
        if selected_question:
            with st.spinner("Waiting for OpenAI response with annotator metadata..."):
                openai_response_with_metadata = ask_openai(selected_question, metadata=annotator_metadata)
                insert_or_update_metadata(task_id, task_level, '-1', '1' if openai_response_with_metadata.lower() == final_answer else '0')

                if openai_response_with_metadata:
                    st.write(f"OpenAI Response with Metadata: {openai_response_with_metadata}")
                else:
                    st.error("Failed to get a response from OpenAI.")
        else:
            st.error("Please select a question first.")
