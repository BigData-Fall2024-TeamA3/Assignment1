import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px

def show():

# Azure SQL connection parameters (replace these with your actual details)
    server = 'damg-server-name.database.windows.net'
    database = 'damg_sql_db'
    username = 'damg_admin'
    password = 'Dadabi@123'
    driver = '{ODBC Driver 17 for SQL Server}'

    # Function to fetch data from Azure SQL
    @st.cache_data(ttl=600)  # cache data for 10 minutes
    def fetch_data_from_azure():
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(conn_str)
        
        # Query your table
        query = "SELECT * FROM ai.metadata"  # Replace with your table name
        df = pd.read_sql(query, conn)
        
        conn.close()
        return df

    # Fetch the data
    df = fetch_data_from_azure()

    # Display the table
    st.title("Azure Data Studio: Metadata Table")
    st.write(df)

    # Visualization examples
    st.title("Trending Visualizations from Azure Data")

    # Line chart for trends over Task IDs
    st.subheader("Response Trends over Task IDs")
    fig_line = px.line(df, x='metadata_sk', y=['direct_response', 'annotator_response'], 
                    title="Direct Response vs Annotator Response over Task IDs")
    st.plotly_chart(fig_line)

    # Area chart for cumulative task levels
    st.subheader("Cumulative Responses by Task Level")
    fig_area = px.area(df, x='task_level', y=['direct_response', 'annotator_response'], 
                    title="Cumulative Direct and Annotator Responses by Task Level")
    st.plotly_chart(fig_area)

    # Scatter plot for task level vs responses
    st.subheader("Scatter Plot: Task Level vs Responses")
    fig_scatter = px.scatter(df, x='task_level', y='direct_response', color='annotator_response',
                            title="Task Level vs Direct/Annotator Responses")
    st.plotly_chart(fig_scatter)
