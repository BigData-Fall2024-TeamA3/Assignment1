import streamlit as st
import openai, boto3, json
import pandas as pd
from IPython import embed


openai.api_key = st.secrets["OPENAI_API_KEY"]
s3 = boto3.client('s3')
bucket_name = st.secrets["BUCKET_NAME"]
s3_file_key = st.secrets["S3_FILE_KEY"]

def show():
    chat_interface()
    # Streamlit app layout
st.title("Ask Anything")

# Function to fetch the .jsonl file from s3 and load it into a DataFrame
@st.cache_data
def load_jsonl_from_s3(bn, s3_fk):
    file_obj = s3.get_object(
        Bucket=bn,
        Key=s3_fk
    )
    file_content = file_obj['Body'].read().decode('utf-8')
    json_lines = [json.loads(line) for line in file_content.strip().split('\n')]
    df = pd.DataFrame(json_lines)
    
    s3 = boto3.resource('s3')

    # Replace the below with your s3 bucket where the model is stored
    bucket = 'assignment4-model-store'

    print("Downloading model from {} bucket...\n".format(bucket))
    s3.Bucket(bucket).download_file('model_state_dict.bin', './model/model_state_dict.bin')

    print("Model successfully downloaded!")
    
    return df

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


# Load the metadata from S3
def chat_interface():
    embed()
    metadata_df = load_jsonl_from_s3(bucket_name, s3_file_key)

    if metadata_df is not None:
        questions = metadata_df['Question'].tolist()
        
        selected_question = st.selectbox("Choose a Question", options=questions)
        
        selected_task = metadata_df[metadata_df['Question'] == selected_question].iloc[0]
        annotator_metadata = selected_task['Annotator Metadata']
        
        if st.button("Submit"):
            if selected_question:
                with st.spinner("Waiting for OpenAI response..."):
                    
                    openai_response = ask_openai(selected_question)
                    
                    
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
                    
                    if openai_response_with_metadata:
                        st.write(f"OpenAI Response with Metadata: {openai_response_with_metadata}")
                    else:
                        st.error("Failed to get a response from OpenAI.")
            else:
                st.error("Please select a question first.")

