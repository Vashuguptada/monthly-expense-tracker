import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Monthly Expense Tracker", layout="centered")

# File path
DATA_PATH = "data/expenses.csv"

# Load or initialize data
if os.path.exists(DATA_PATH):
    expenses = pd.read_csv(DATA_PATH)
else:
    expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

st.title("📊 Monthly Expense Tracker")

# Form to add new expense
with st.form("expense_form"):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Travel", "Entertainment", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount (INR)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_entry = pd.DataFrame([[expense_date, category, description, amount]],
                             columns=["Date", "Category", "Description", "Amount"])
    expenses = pd.concat([expenses, new_entry], ignore_index=True)
    expenses.to_csv(DATA_PATH, index=False)
    st.success("✅ Expense added!")

# Display data
st.subheader("🧾 Expense Summary")
st.dataframe(expenses)

# Total
st.metric("💰 Total Expenses", f"₹ {expenses['Amount'].sum():,.2f}")

# Breakdown
st.subheader("📂 Category-wise Summary")
if not expenses.empty:
    st.bar_chart(expenses.groupby("Category")["Amount"].sum())
