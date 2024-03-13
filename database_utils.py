import streamlit as st
import pandas as pd
import pyodbc
import toml
import os

@st.cache
def connect_to_database():
    # Path to the secrets.toml file
    streamlit_path = os.path.dirname(st.__file__)
    secrets_path = os.path.join('secrets.toml')

    if not os.path.exists(secrets_path):
        return None

    secrets = toml.load(secrets_path)
    server = secrets['database']['server']
    database = secrets['database']['database']
    username = secrets['database']['username']
    password = secrets['database']['password']
    connection_string = f"DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
    return pyodbc.connect(connection_string)

def list_tables():
    connection = connect_to_database()
    if connection is None:
        st.error("Error: secrets.toml file not found.")
        st.stop()

    with connection:
        cursor = connection.cursor()
        query = "SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_type = 'BASE TABLE';"
        cursor.execute(query)
        tables = cursor.fetchall()
        st.write("Tables in the database:")
        st.write([table[0] for table in tables])

def read_data(query):
    connection = connect_to_database()
    if connection is None:
        st.error("Error: Unable to connect to the database.")
        st.stop()

    with connection:
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        return pd.DataFrame.from_records(data, columns=columns)
