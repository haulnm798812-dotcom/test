import os
# fmt: off
os.add_dll_directory(
    r'C:\learn_py\learn\env\Lib\site-packages\clidriver\bin'
)
import ibm_db
import ibm_db_dbi
# fmt: on
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
# Rows: Records
# Columns: Attributes
"""
dsn = (
    "DATABASE=BLUDB;"
    "HOSTNAME=your-host.ibm.com;"
    "PORT=50001;"
    "PROTOCOL=TCPIP;"
    "UID=your_username;"
    "PWD=your_password;"
    "SECURITY=SSL;"
)"""    
st.set_page_config(page_title="Habit Tracker", page_icon="📊")
load_dotenv()
DB2_HOSTNAME = os.getenv("DB2_HOSTNAME")
DB2_PORT = os.getenv("DB2_PORT")
DB2_DATABASE = os.getenv("DB2_DATABASE")
DB2_USERNAME = os.getenv("DB2_USERNAME")
DB2_PASSWORD = os.getenv("DB2_PASSWORD")
DB2_SCHEMA =  os.getenv("DB2_USERNAME", "").upper()
TABLE = f"{DB2_SCHEMA}.HABITS"

#Func1: Check data values
def validate_data(habit, sleep_hrs, work_hrs):
    try:
        float(habit.strip())
        return False, "Habit must not be a number"
    except ValueError as e:
        pass
    if habit.strip() == "":
        return False, "Habit can't be BLANK"
    if work_hrs + sleep_hrs > 24:
        return False, f"Work hours and Sleep hours must be <= 24"
    if work_hrs < 0 or sleep_hrs < 0:
        return False, "Work & Sleep hours must be > 0"
    return True, ""


#Func2 KEEP: connect to the Database.
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
            f"SECURITY=SSL")
        ibm_conn = ibm_db.connect(dsn,"","")
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


#Fun3 checks for Table existence/ if not --> Create a NEW one.
def ensure_table_exists(ibm_conn):
    try:
        sql = f"CREATE TABLE {TABLE} (" \
        "ID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY," \
        "LOG_DATE DATE NOT NULL," \
        "SLEEP_HRS SMALLINT NOT NULL," \
        "WORK_HRS SMALLINT NOT NULL," \
        "HABIT VARCHAR(100) NOT NULL)"
        ibm_db.exec_immediate(ibm_conn, sql) 
    except Exception as e:
        if "already exists " in str(e).lower() or "sqlcode=-601" in str(e).lower():
            pass
        else:
            st.warning(f"Table set up issue {e}")


#Func4 KEEP: put data into the Table using 'sql' & 'stmt'.
def insert_habits(ibm_conn, log_date, sleep_hrs, work_hrs, habit):
    try:
        sql = f"INSERT INTO {TABLE} (LOG_DATE, SLEEP_HRS, WORK_HRS, HABIT) VALUES(?,?,?,?)"
        stmt = ibm_db.prepare(ibm_conn, sql)
        ibm_db.execute(stmt,(
            log_date.strftime("%Y-%m-%d"),
            int(sleep_hrs),
            int(work_hrs),
            str(habit).capitalize()
        ))
        return True, None
    except Exception as e:
        return False, str(e)
    
try:
    conn, ibm_conn = get_connection()
    ensure_table_exists(ibm_conn)
except Exception as e:
    st.error(str(e))
    st.stop()

if "counter" not in st.session_state:
    st.session_state.counter = 0
st.title("Daily Habit Tracker")
st.markdown("### Keep track on your Sleep, Work & Habit!")
st.header("Log today's habit")
file_form = st.form("habit tracker")

with file_form:
    todate = st.date_input("Date", value=datetime.today())
    sleep_hrs = st.number_input("Sleep hours",
                                min_value=0.0,
                                max_value=24.0,
                                format="0.1f",
                                help="Put in today's sleep hours")
    work_hrs = st.number_input("Work hours",
                               min_value=0.0,
                               max_value=24.0,
                               format="0.1f",
                               help="Put in today's work hours")
    hab_done = st.text_input("Main Habit?",
                             placeholder="for ex: Gym, Reading, Gaming, Cooking, etc",
                             help="What you did in free time")
    submitted = st.form_submit_button("Submit here")
if submitted:
    st.write("---")
    st.session_state.counter += 1
    is_valid, advice = validate_data(
        hab_done, sleep_hrs, work_hrs)
    if not is_valid:
        st.error(f"{advice}")
        st.stop()
    insert_success, comment = insert_habits(ibm_conn, todate, sleep_hrs, work_hrs, hab_done)
    if insert_success:
        st.success(f"Successfully integrate data in {TABLE}")
        st.info(f"Submit count: {st.session_state.counter} times")
    else:
        st.error(comment)
        st.stop() 
