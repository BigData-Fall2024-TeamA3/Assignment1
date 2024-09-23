import streamlit as st
import pyodbc
import bcrypt

# Database connection
def get_db_connection():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=your_server;'
        'Database=your_database;'
        'UID=your_username;'
        'PWD=your_password;'
    )
    return conn

# Signup function
def signup(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()

# Login function
def login(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
            return True
        return False

# Streamlit app
st.title("Login/Signup App")

# Signup form
if st.sidebar.button("Signup"):
    st.subheader("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Submit"):
        signup(username, password)
        st.success("Account created successfully!")

# Login form
if st.sidebar.button("Login"):
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Submit"):
        if login(username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")
