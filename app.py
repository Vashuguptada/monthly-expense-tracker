import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Monthly Expense Tracker", layout="centered")

# Use session state to store data
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

st.title("📊 Monthly Expense Tracker")

# Input form
with st.form("expense_form"):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Travel", "Entertainment", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount (INR)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_data = pd.DataFrame([[expense_date, category, description, amount]],
                            columns=["Date", "Category", "Description", "Amount"])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
    st.success("✅ Expense added!")

# Display
st.subheader("🧾 Expense Summary")
st.dataframe(st.session_state.expenses)

# Total amount
total = st.session_state.expenses["Amount"].sum()
st.metric("💰 Total Expenses", f"₹ {total:,.2f}")

# Category-wise breakdown
st.subheader("📂 Category-wise Summary")
if not st.session_state.expenses.empty:
    summary = st.session_state.expenses.groupby("Category")["Amount"].sum().reset_index()
    st.bar_chart(summary.set_index("Category"))
