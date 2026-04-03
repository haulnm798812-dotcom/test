import os
# fmt: off
os.add_dll_directory(r'C:\learn_py\learn\env\Lib\site-packages\clidriver\bin')
import ibm_db
import ibm_db_dbi
# fmt: on
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Dashboard")
st.write("### Show your entries history")
load_dotenv()
DB2_HOSTNAME = os.getenv("DB2_HOSTNAME")
DB2_PORT = os.getenv("DB2_PORT")
DB2_DATABASE = os.getenv("DB2_DATABASE")
DB2_USERNAME = os.getenv("DB2_USERNAME")
DB2_PASSWORD = os.getenv("DB2_PASSWORD")
DB2_SCHEMA =  os.getenv("DB2_USERNAME", "").upper()
TABLE = f"{DB2_SCHEMA}.HABITS"

@st.cache_resource
def get_connection():
    try:
        dsn = (
            f"DATABASE={DB2_DATABASE};"
            f"HOSTNAME={DB2_HOSTNAME};"
            f"PORT={DB2_PORT};"
            f"PROTOCOL=TCPIP;"
            f"UID={DB2_USERNAME};"
            f"PWD={DB2_PASSWORD};"
            f"SECURITY=SSL;"
            f"AUTHENTICATION=DIRECT")
        ibm_conn = ibm_db.connect(dsn, "", "")
        return ibm_db_dbi.Connection(ibm_conn), ibm_conn
    except Exception as e:
        raise ConnectionError(f"DB2 Connection Error: {e}")
    
def get_live_connection():
    conn, ibm_conn = get_connection()
    try:
        ibm_db.execute(ibm_db.prepare(ibm_conn, "SELECT 1 FROM SYSIBM.SYSDUMMY1"), ())
    except Exception:
        get_connection.clear()
        conn, ibm_conn = get_connection()
    return conn, ibm_conn


try:
    conn, _ = get_live_connection()
except Exception as e:
    st.error(e)
    st.stop()   

@st.cache_data(ttl=120)
def load_habit():
    try:
        conn, _ = get_live_connection()
        df = pd.read_sql(f"SELECT * FROM {TABLE} ORDER BY LOG_DATE DESC", conn)
        df.columns = [c.lower() for c in df.columns]
        if "log_date" in df.columns:
            df['log_date'] = pd.to_datetime(df['log_date']).dt.date
        return df, None
    except Exception as e:
        return None, str(e) 
    
df, problem = load_habit()
if problem:
    st.error(problem)
    st.stop()


#There is a bug needed to be fixed.
def make_stats_metrics(df, num_cols):
    """
    Args: Take columns from the 2nd function to make statistics about data

    Return:
    -statistics if succeeded, None for problem.
    -None stats if failed, problem: problem to fix. """
    try:
        stats = {}
        for col in num_cols:
            stats[col] = {
                "mean": df[col].mean(),
                "sum": df[col].sum(),
                "max": df[col].max(),
                "min": df[col].min()}
        return stats, None
    except ValueError as e:
        return None, f"{e}"

digit_cols = ['sleep_hrs', 'work_hrs']
statics, metric_error = make_stats_metrics(df, digit_cols)
if metric_error:
    st.error(metric_error)
    st.stop()
if "counter" in st.session_state and st.session_state.counter > 0:
    st.success(f"Page 1 submission: {st.session_state.counter} times.")
st.dataframe(df, use_container_width=True)
st.write("## 📈 Statistics:")
st.write(f"Tracked {len(df)} days!")
cols = st.columns(len(digit_cols))
for idx, col_name in enumerate(digit_cols):
    with cols[idx]:
        st.metric(label=f"Average {col_name}",
                  value=f"{statics[col_name]['mean']:.1f}")
with st.expander(f"📊 Detailed Statistics"):
    for col_name in digit_cols:
        st.write(f"**{col_name}**")
        col1, col2, col3, col4 = st.columns(4, border=True)
        with col1:
            st.metric(
                "Average", f"{statics[col_name]['mean']:.1f}")
        with col2:
            st.metric('Total', f"{statics[col_name]['sum']:.1f}")
        with col3:
            st.metric('Most', statics[col_name]['max'])
        with col4:
            st.metric('Least', statics[col_name]['min'])
