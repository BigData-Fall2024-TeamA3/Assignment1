import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc

def show():
    # Azure SQL connection parameters
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

    # Ensure numeric conversion
    df['task_level'] = pd.to_numeric(df['task_level'], errors='coerce')

    # Drop rows with NaN values in task_level
    df = df.dropna(subset=['task_level'])

    # Convert task_level to integer
    df['task_level'] = df['task_level'].astype(int)

    # Line chart: Direct Response vs Annotator Response over Task IDs
    st.subheader("Response Trends Over Task IDs")
    fig_line = px.line(df, x='metadata_sk', y=['direct_response', 'annotator_response'], 
                    labels={
                        'metadata_sk': 'Task ID',
                        'value': 'Response Count',
                        'variable': 'Response Type'
                    },
                    title="Direct Response vs Annotator Response Across Task IDs")
    st.plotly_chart(fig_line)


    