import streamlit as st
from database.fetch_data import fetch_table

st.set_page_config(
    page_title="LeetCode Rankings",
    page_icon="💻"
)

st.title("LeetCode Rankings 💻")

df = fetch_table()
st.dataframe(df, width=1400, height=600)
