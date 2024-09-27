import streamlit as st

import pyodbc
import bcrypt
from page import visualization
from page import model_evaluation

driver = st.secrets['driver']
server = st.secrets['server']
database = st.secrets['database']
username = st.secrets['username']
password = st.secrets['password']

connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection_string)



def user_exists(username):
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM ai.user_tbl WHERE username = ?", (username,))
        return cursor.fetchone() is not None 


def signup(username, password):
    if user_exists(username):
        return False, "User already exists!"
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ai.user_tbl(username, user_password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        return True, "Account created successfully!"
    except pyodbc.IntegrityError:
        return False, "Signup failed due to a database error."

# Login function
def login(username, password):
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_password FROM ai.user_tbl WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
            return True
        return False


st.title("Welcome")
st.sidebar.title("Navigation")


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


if st.session_state.logged_in:
    with st.sidebar:
        if st.button("Visualization Page"):
            st.session_state.page = 'visualization'
        if st.button("Test Case Selection"):
            st.session_state.page = 'model_evaluation'
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.signup_mode = False
            st.rerun()
            st.session_state.page = 'login'
    
    if 'page' not in st.session_state:
        st.session_state.page = 'model_evaluation' 
    
    if st.session_state.page == 'visualization':
        visualization.show()
    elif st.session_state.page == 'model_evaluation':
        model_evaluation.show()

else:

    if 'signup_mode' not in st.session_state:
        st.session_state.signup_mode = False


    if not st.session_state.signup_mode:
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        

        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both username and password.")
            elif login(username, password):
                st.session_state.logged_in = True
                st.rerun() 
            else:
                st.error("Invalid username or password.")

        if st.button("Create an Account"):
            st.session_state.signup_mode = True
            st.rerun()


    else:
        st.subheader("Create Account")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')


        if st.button("Sign Up"):
            if not new_username or not new_password:
                st.error("Please fill in both username and password.")
            else:
                success, message = signup(new_username, new_password)
                if success:
                    st.success(message)
                    st.session_state.signup_mode = False 
                    st.rerun() 
                else:
                    st.error(message)
            
        if st.button("Back"):
            st.session_state.signup_mode = False
            st.rerun()
            