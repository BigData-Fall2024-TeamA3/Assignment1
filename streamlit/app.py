import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import test_case_selection, model_evaluation, visualization



#User auhtnetication
names = ["Aishwarya patil", "Deepak"]
username =["Aish","Deep"] 

#load hashed passwords
file_path = Path(__file__).parent / "hashed.pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
    
authenticator = stauth.Authenticate(names,username, hashed_passwords, "sales_dashboard", "abcdef",cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status == False:
    st.error("username/Password is incorrect")
if authentication_status == None:
    st.error("Please insert Username/password")
sidebar_placeholder = st.sidebar.empty()
if authentication_status:
    def main():
        st.sidebar.title(f"Welcome {name}")
        if st.sidebar.button("Test Case Selection"):
            test_case_selection.show()
        if st.sidebar.button("Model Evaluation"):
            model_evaluation.show()
        if st.sidebar.button("Visualization"):
            visualization.show()
        authenticator.logout("Logout","sidebar")

        
    if __name__ == "__main__":
        main()                        
