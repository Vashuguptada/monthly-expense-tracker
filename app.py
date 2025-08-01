import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Monthly Expense Tracker Made By Vashu", layout="centered")

# Session State for storing data
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])
if "custom_categories" not in st.session_state:
    st.session_state.custom_categories = []

st.title("📊 Monthly Expense Tracker")

# Add new category
with st.expander("➕ Add New Category"):
    new_cat = st.text_input("Enter new category")
    if st.button("Add Category"):
        if new_cat and new_cat not in st.session_state.custom_categories:
            st.session_state.custom_categories.append(new_cat)
            st.success(f"✅ '{new_cat}' added!")

# Final category list
default_categories = ["Food", "Rent", "Utilities", "Travel", "Entertainment", "Other"]
all_categories = default_categories + st.session_state.custom_categories

# Expense Form
with st.form("expense_form", clear_on_submit=True):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", all_categories)
    description = st.text_input("Description")
    amount = st.number_input("Amount (INR)", min_value=0.0, format="%.2f", step=10.0)
    submitted = st.form_submit_button("➕ Add Expense")

if submitted:
    new_entry = pd.DataFrame([[expense_date, category, description, amount]],
                             columns=["Date", "Category", "Description", "Amount"])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
    st.success("Expense added!")

# Total & Summary
st.subheader("🧾 Expense Summary Made By Vashu")
if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses)

    # Total
    total = st.session_state.expenses["Amount"].sum()
    st.metric("💰 Total Expenses", f"₹ {total:,.2f}")

    # Category-wise Chart
    st.subheader("📂 Category-wise Expenses")
    summary = st.session_state.expenses.groupby("Category")["Amount"].sum().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=summary, x="Category", y="Amount", palette="pastel", ax=ax)
    ax.set_title("Expenses by Category")
    ax.bar_label(ax.containers[0], fmt='₹%.0f', label_type='edge', padding=3)
    st.pyplot(fig)

    # Date-wise Line Chart
    st.subheader("📅 Expenses Over Time")
    line_data = st.session_state.expenses.groupby("Date")["Amount"].sum().reset_index()
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=line_data, x="Date", y="Amount", marker="o", ax=ax2)
    ax2.set_title("Daily Expense Trend")
    for x, y in zip(line_data["Date"], line_data["Amount"]):
        ax2.text(x, y, f"₹{int(y)}", ha="center", va="bottom")
    st.pyplot(fig2)

else:
    st.info("No expenses added yet.")
