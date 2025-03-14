import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(layout="wide", page_title="Daily Remark Summary", page_icon="📊", initial_sidebar_state="expanded")

# Apply dark mode
st.markdown(
    """
    <style>
    .reportview-container {
        background: #2E2E2E;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #2E2E2E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Daily Remark Summary')

@st.cache_data
def load_data(uploaded_file):
    # Load all the sheets into a dictionary of DataFrames
    xls = pd.ExcelFile(uploaded_file)
    call_history = pd.read_excel(xls, 'Call History')
    call_status_summary = pd.read_excel(xls, 'Call Status Summary')
    call_received_summary = pd.read_excel(xls, 'Call Received Summary')
    login_logout_activity = pd.read_excel(xls, 'Login Logout Activity')
    volare_status_summary = pd.read_excel(xls, 'Volare Status Summary')
    return call_history, call_status_summary, call_received_summary, login_logout_activity, volare_status_summary

uploaded_file = st.sidebar.file_uploader("PREDICTIVE TIME PER AGENTS", type="xlsx")

if uploaded_file is not None:
    # Load the data from the uploaded file
    call_history, call_status_summary, call_received_summary, login_logout_activity, volare_status_summary = load_data(uploaded_file)

    # Filter out unnecessary data by excluding specific agents
    login_logout_activity = login_logout_activity[~login_logout_activity['Collector'].isin([
        'FGPANGANIBAN', 'KPILUSTRISIMO', 'BLRUIZ', 'MMMEJIA', 'SAHERNANDEZ', 'GPRAMOS',
        'JGCELIZ', 'JRELEMINO', 'HVDIGNOS', 'RALOPE', 'DRTORRALBA', 'RRCARLIT', 'MEBEJER',
        'DASANTOS', 'SEMIJARES', 'GMCARIAN', 'RRRECTO', 'JMBORROMEO', 'EUGALERA', 'JATERRADO'
    ])]

    # Function to calculate the total time spent per agent
    def calculate_total_time(df):
        # Convert the "Connect/Disconnect Date Time" to datetime format
        df['Connect/Disconnect Date Time'] = pd.to_datetime(df['Connect/Disconnect Date Time'], errors='coerce')
        
        # Make sure that the 'Collector' and 'Connect/Disconnect Date Time' columns exist
        if 'Collector' in df.columns and 'Connect/Disconnect Date Time' in df.columns:
            # Calculate the time spent per row (difference between Connect and Disconnect times)
            df['Time Spent'] = df['Connect/Disconnect Date Time'].diff().shift(-1)
            df['Time Spent'] = df['Time Spent'].fillna(pd.Timedelta(0))  # Replace NaN with 0 time
        
            # Sum the time spent per agent (sum times for the same 'Collector')
            total_time_per_agent = df.groupby('Collector')['Time Spent'].sum()
            
            return total_time_per_agent
        else:
            st.error('Columns "Collector" or "Connect/Disconnect Date Time" not found in the data.')
            return None

    # Calculate total time for each agent in "Login Logout Activity"
    total_time_per_agent = calculate_total_time(login_logout_activity)

    # Display the total time per agent
    if total_time_per_agent is not None:
        st.write("Total Time Per Agent:", total_time_per_agent)
