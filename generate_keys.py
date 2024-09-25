import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ["Aishwarya patil", "Deepak"]
username =["Aish","Deep"] 
password = ["XXX","XXX"]

hashed_passwords = stauth.Hasher(password).generate()

#load hashed passwords
file_path = Path(__file__).parent / "hashed.pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)
    