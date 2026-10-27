from datetime import datetime
import pandas as pd
import streamlit as st
from sqlalchemy import text

#Open connection base on configuration [connections.db] in db_config.toml
conn = st.connection("db", type = "sql")

def record(r_date, r_category, r_amount, r_note):
    with conn.session as s:
        s.execute(
            text("""
                insert into analyst.temp_expense("date", category, amount, note)
                values(:date, :category, :amount, :note)
            """),
            {"date": r_date, "category": r_category, "amount": r_amount, "note": r_note}
        )
        s.commit()

def del_id(id_need_del):
    with conn.session as s:
        s.execute(text("delete from analyst.temp_expense where id = :id"), {"id": id_need_del})
        s.commit()

def read_all():
    df = conn.query("select * from analyst.temp_expense order by date desc, id desc", ttl = 0)
    df["amount"] = df["amount"].astype(float)
    return df

#Dialog Delete Confirm -----
@st.dialog("Confirm Deletion")
def confirmation_box(id_need_del):
    st.warning(f"Remove transaction ID {id_need_del}? Can not undo.")
    c1, c2 = st.columns(2)
    if c1.button("Yes, Remove", type = "primary"):
        del_id(id_need_del)
        st.rerun()
    if c2.button("No"):
        st.rerun()

#Fragment: Statistical Area ----
# @st.fragment(run_every = "10s") #df để ngoài fragment mà claude kêu thêm dòng này rồi quan sát ông nội T hay gì ?
@st.fragment
def statistical_area(df):
    st.caption(f"+ Fragment rerun at: {datetime.now():%H:%M:%S}")

    df = df.copy()
    df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
    list_month = ["All"] + sorted([str(m) for m in df["month"].unique()], reverse = True)
    month = st.selectbox("View by Month", list_month)

    df_filtered = df if month == "All" else df[df["month"] == month]

    c1, c2 = st.columns(2)
    c1.metric("Total Expense", f"{df_filtered['amount'].sum():,.0f} VND")
    c2.metric("Trans No.", len(df_filtered))

    st.bar_chart(df_filtered.groupby("category")["amount"].sum())

    # Detail - unhide 2 lines and hide zone 3 below to filter detail with chart
    # st.subheader("Detail")
    # st.dataframe(df_filtered, hide_index = True)


#Page Layout -----
st.title("💰 Expense Journal")
st.caption(f"+ All page run at: {datetime.now():%H:%M:%S}")

# Zone 1: Out of FRAGMENT
with st.form("form_expense", clear_on_submit = True):
    c1, c2 = st.columns(2)
    inp_date = c1.date_input("Date")
    inp_category = c2.selectbox("Category", ["Food & Beverage", "Transport", "Shopping", "Billing", "Others"])
    inp_amount = st.number_input("Amount (VND)", min_value = 0, max_value = 100000000)
    inp_note = st.text_input("Note")
    form_send = st.form_submit_button("Save")

if form_send:
    if inp_amount <= 0:
        st.error("Amount have to better than zero.")
    else:
        record(r_date = inp_date, r_category = inp_category, r_amount = inp_amount, r_note = inp_note)
        st.success("Saved!")

df = read_all()

if df.empty:
    st.info("Didn't have any transactions yet.")
    st.stop()

#Zone 2: Statistical (In FRAGMENT)
st.subheader("Statistical")
statistical_area(df)

#Zone 3: Detail table & Remove (Out of FRAGMENT)
st.subheader("Detail")
st.dataframe(df, hide_index = True)

with st.expander("Delete a Transaction"):
    id_need_del = st.selectbox("Select ID need to delete", df["id"])
    if st.button("Delete"):
        confirmation_box(id_need_del)



