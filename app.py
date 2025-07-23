import streamlit as st
from db import SessionLocal, User, Expense, hash_password, verify_password
import pandas as pd
from datetime import date

st.set_page_config("Expense Tracker", layout="centered")

session = SessionLocal()

# --- SIGNUP ---
def signup():
    st.subheader("📝 Create New Account")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        if session.query(User).filter_by(username=username).first():
            st.error("Username already exists")
        else:
            new_user = User(username=username, password=hash_password(password))
            session.add(new_user)
            session.commit()
            st.success("Account created! Please log in.")

# --- LOGIN ---
def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(password, user.password):
            st.session_state.logged_in = True
            st.session_state.user_id = user.id
            st.session_state.username = username
            st.success(f"Welcome {username}")
        else:
            st.error("Invalid username or password")

# --- EXPENSE TRACKER ---
def expense_tracker(user_id):
    st.subheader("📊 Expense Tracker")
    with st.form("expense_form"):
        edate = st.date_input("Date", date.today())
        category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Travel", "Other"])
        desc = st.text_input("Description")
        amt = st.number_input("Amount", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Add Expense")

    if submit:
        session.add(Expense(user_id=user_id, date=edate, category=category, description=desc, amount=amt))
        session.commit()
        st.success("Expense added!")

    # Show user’s expenses
    expenses = session.query(Expense).filter_by(user_id=user_id).all()
    df = pd.DataFrame([(e.date, e.category, e.description, e.amount) for e in expenses],
                      columns=["Date", "Category", "Description", "Amount"])

    st.dataframe(df)
    st.metric("💰 Total", f"₹ {df['Amount'].sum():,.2f}")
    if not df.empty:
        st.bar_chart(df.groupby("Category")["Amount"].sum())

# --- MAIN ---
st.title("🔐 Secure Expense Tracker")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = st.sidebar.radio("Menu", ["Login", "Sign Up", "Expense Tracker"])

if menu == "Sign Up":
    signup()
elif menu == "Login":
    login()
elif menu == "Expense Tracker":
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()
        expense_tracker(st.session_state.user_id)
    else:
        st.warning("Please log in first.")
