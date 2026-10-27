import streamlit as st

st.title("📈 Report")
st.write("This is Report Page")
st.write(f"Hello {st.session_state.get('user_name', 'There is no user name yet!')}!")