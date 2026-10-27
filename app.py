import streamlit as st
from pathlib import Path

st.set_page_config(page_title = "First Streamlit App", page_icon = "📊", layout = "wide")

#Path
page_dir = Path(__file__).resolve().parent / "pages"
login_page_path = page_dir / "login_page.py"
home_page_path = page_dir / "home_page.py"
report_page_path = page_dir / "report_page.py"
expense_page_path = page_dir / "expense_page.py"
chat_bot_path = page_dir / "chat_bot.py"

#Page
login_page = st.Page(login_page_path, title = "Login Page", icon = "🔐")
home_page = st.Page(home_page_path, title = "Home Page", icon = "🏠", default = True)
report_page = st.Page(report_page_path, title = "Report", icon = "📈")
expense_page = st.Page(expense_page_path, title = "Expense Journal", icon = "💰")
chat_bot_page = st.Page(chat_bot_path, title = "Chat bot", icon = "🤖")


#Menu
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    menu = st.navigation([login_page])
else:
    menu = st.navigation([home_page, report_page, expense_page, chat_bot_page])

menu.run()





