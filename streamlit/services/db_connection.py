# services/db_connection.py

import streamlit as st

class DatabaseConnection:
    def __init__(self):
        # https://huggingface.co/docs/datasets/en/filesystems
        # https://docs.streamlit.io/develop/tutorials/databases/aws-s3
        # https://stackoverflow.com/questions/73398636/how-to-interact-read-write-delete-files-in-s3-bucket-directly-through-streamli
        # self.conn = st.connection('db', type='sql')
        # store instance of metadata and instance of media files
        # Store final response (success: bool, context_required: bool)
        # Seed data??
        # cache the metadata file
        
        self.conn = None

    def query(self, sql, params=None):
        # return self.conn.query(sql, params=params)
        return {"placeholder response"}

    def execute(self, sql, params=None):
        # return self.conn.execute(sql, params=params)
        return {"placeholder response"}

db = DatabaseConnection()