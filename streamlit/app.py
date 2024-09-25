import streamlit as st

import pyodbc
import bcrypt
import time 
import visualization



def get_db_connection():

    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=damg-server-name.database.windows.net;'
        'Database=damg_sql_db;'
        'UID=damg_admin;'
        'PWD=Dadabi@123;'
    )
    return conn


def signup(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ai.user_tbl(username, user_password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        return True  # Indicate successful signup
    except pyodbc.IntegrityError:
        return False  # Indicate failure due to username conflict

# Login function
def login(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_password FROM ai.user_tbl WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
            return True
        return False

# Streamlit app
st.title("Welcome")
st.sidebar.title("Navigation")
# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Redirect to visualization if logged in
if st.session_state.logged_in:
    st.success("Login successful!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False  # Set logged in state to False
        st.session_state.signup_mode = False  # Reset signup mode if it was set
         # Rerun to show the login page

    # Replace this with your visualization function
    visualization.show()  
    # Replace this with your visualization function

else:
    # Determine the current mode (Login or Signup)
    if 'signup_mode' not in st.session_state:
        st.session_state.signup_mode = False

    # Show the login form
    if not st.session_state.signup_mode:
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                  # Rerun the script to show the visualization page
            else:
                st.error("Invalid username or password.")

        # Link to switch to signup
        if st.button("Create an Account"):
            st.session_state.signup_mode = True  # Set to signup mode
              # Rerun to show the signup form

    # Show the signup form
    else:
        st.subheader("Create Account")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')

        if st.button("Sign Up"):
            if signup(new_username, new_password):
                st.success("Account created successfully!")  # Show success
                st.session_state.signup_mode = False  # Reset signup mode
                  # Rerun to go back to login
            else:
                st.error("Username already exists. Please choose a different username.")
            