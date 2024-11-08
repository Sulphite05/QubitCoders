import streamlit as st
from fuzzy.classifier import get_user_expertise

st.set_page_config(
    page_title="AI Profile Classifier",
    page_icon="🧬"
)

st.title("AI Profile Classifier 🧬")
st.text("""
This AI profile classifier will help you evaluate your profile strength.
""")
st.divider()

with st.form("my_form"):
    username = st.text_input(
        "Enter Your Username 👇",
        placeholder="e.g. neal_wu",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        score, expertise = get_user_expertise(username)
        st.text(f'''Your profile score is {float(score)}/10 and expertise is {expertise}!''')
