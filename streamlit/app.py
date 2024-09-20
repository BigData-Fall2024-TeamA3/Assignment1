import streamlit as st
from pages import test_case_selection, model_evaluation, visualization
from IPython import embed

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["test_case_selection", "Model Evaluation", "Visualization"])

    if page == "Model Evaluation":
        model_evaluation.show()
    elif page == "Visualization":
        visualization.show()
    else:
        test_case_selection.show()

if __name__ == "__main__":
    main()                        
