import streamlit as st

st.title("🔐 Login page")

pw = st.text_input("Password", type = "password")
if st.button("Log in"):
    if pw == st.secrets["app_password"]:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error("Wrong password.")

