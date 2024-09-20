from streamlit.pages import home
import streamlit as st
from dotenv import load_dotenv
from pages import test_case_selection, model_evaluation, visualization
# from requests import pathlib
import sys



def main():
    print(sys.path)
    st.set_page_config(page_title="GAIA Model Evaluation", layout="wide")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Test Case Selection", "Model Evaluation", "Visualization"])

    if page == "Test Case Selection":
        test_case_selection.show()
    elif page == "Model Evaluation":
        model_evaluation.show()
    elif page == "Visualization":
        visualization.show()

if __name__ == "__main__":
    main()