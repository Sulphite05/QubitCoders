import streamlit as st


st.set_page_config(
    page_title="Welcome",
    page_icon="👋"
)

col1, col2 = st.columns([0.8, 5])

with col1: st.image('images/logo.png', width=100)
with col2: st.title("Welcome to QubitCoders App")
st.divider()

st.subheader("Who We Are 💡")
st.markdown("""
The QubitCoders community exclusively for the CIS, NEDUET students who are ready to **debug** their coding journey 
and **optimize** their problem-solving skills!

Our founders host regular contests to **iterate** on your coding skills and **recursively** enhance your ability 
to tackle the toughest challenges.

This app is designed for the QubitCoders community and anyone looking to **level up** their LeetCode game. We analyze 
your current LeetCode profile and provide insights that help you **refactor** your approach, identify areas to improve, 
and help you **acquire** the skills needed to conquer any DSA problem with confidence.
""")

st.subheader("Our App Features 🏆")
st.write("""
    1. **Ranking**: View the leaderboard to see how CIS students stack up. Wish you first to AK 🫡
    2. **Classifier**: Get your LeetCode profile **classified** to find out which level of coder you are. Whether 
    you’re a **beginner** or an **advanced** problem-solver, we’ll help you debug your path to greatness!\n
""")

st.image('images/dept.png', caption='CIS Department, NEDUET', use_column_width=True,)

footer = """
    <style>
        .footer {
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: #555;
        }
    </style>
    <div class="footer">
        <p>Made with lots of ☕ All rights reserved.</p>
    </div>
"""

st.markdown(footer, unsafe_allow_html=True)