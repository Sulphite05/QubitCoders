import streamlit as st
from database.fetch_data import fetch_table

st.set_page_config(
    page_title="LeetCode Rankings",
    page_icon="💻"
)

st.title("CIS LeetCode Rankings 💻")
st.divider()

df = fetch_table()
st.dataframe(df)
