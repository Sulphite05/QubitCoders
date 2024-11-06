import streamlit as st

st.set_page_config(
    page_title="AI Profile Classifier",
    page_icon="🧬"
)

st.title("AI Profile Classifier 🧬")
st.text("This AI profile classifier will help you evaluate your profile strength.\n")

text_input = st.text_input(
    "Enter username 👇",

    placeholder="e.g. neal_wu",
)