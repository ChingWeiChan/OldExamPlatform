# streamlit_app.py
import streamlit as st
import psycopg2


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        try:
            return cur.fetchall()
        except:
            pass
