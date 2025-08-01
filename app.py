import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
import uuid

st.set_page_config(page_title="Monthly Expense Tracker Made By Vashu", layout="centered")

# --- Initialize session state ---
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["ID", "Date", "Category", "Description", "Amount"])

if "custom_categories" not in st.session_state:
    st.session_state.custom_categories = ["Food", "Rent", "Utilities", "Travel", "Entertainment", "Other"]

if "amount_input" not in st.session_state:
    st.session_state.amount_input = 0.0

if "amount_clicked" not in st.session_state:
    st.session_state.amount_clicked = False

# --- Function to clear amount input on click ---
def clear_amount():
    if not st.session_state.amount_clicked:
        st.session_state.amount_input = 0.0
        st.session_state.amount_clicked = True

# --- Title ---
st.title("📊 Monthly Expense Tracker")

# --- Add Custom Category ---
with st.expander("➕ Add New Category"):
    new_cat = st.text_input("Enter new category name")
    if st.button("Add Category"):
        if new_cat and new_cat not in st.session_state.custom_categories:
            st.session_state.custom_categories.append(new_cat)
            st.success(f"Category '{new_cat}' added!")

# --- Expense Input Form ---
with st.form("expense_form"):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", st.session_state.custom_categories)
    description = st.text_input("Description")

    amount = st.number_input(
        "Amount (INR)",
        min_value=0.0,
        format="%.2f",
        value=st.session_state.amount_input,
        key="amount_input",
        on_change=clear_amount
    )

    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_entry = {
        "ID": str(uuid.uuid4()),
        "Date": expense_date,
        "Category": category,
        "Description": description,
        "Amount": st.session_state.amount_input
    }
    st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_entry])], ignore_index=True)
    st.success("✅ Expense added!")

    # Reset amount field
    st.session_state.amount_input = 0.0
    st.session_state.amount_clicked = False

# --- Editable Table ---
st.subheader("🧾 Expense Summary")

if not st.session_state.expenses.empty:
    for idx, row in st.session_state.expenses.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 3, 2, 1.5, 1])
        col1.date_input("Date", row["Date"], key=f"date_{row['ID']}")
        col2.selectbox("Category", st.session_state.custom_categories,
                       index=st.session_state.custom_categories.index(row["Category"]), key=f"cat_{row['ID']}")
        col3.text_input("Description", row["Description"], key=f"desc_{row['ID']}")
        col4.number_input("Amount", value=row["Amount"], format="%.2f", key=f"amt_{row['ID']}")
        if col5.button("💾 Update", key=f"update_{row['ID']}"):
            st.session_state.expenses.loc[idx, "Date"] = st.session_state[f"date_{row['ID']}"]
            st.session_state.expenses.loc[idx, "Category"] = st.session_state[f"cat_{row['ID']}"]
            st.session_state.expenses.loc[idx, "Description"] = st.session_state[f"desc_{row['ID']}"]
            st.session_state.expenses.loc[idx, "Amount"] = st.session_state[f"amt_{row['ID']}"]
            st.success("Updated successfully")
        if col6.button("🗑️ Delete", key=f"del_{row['ID']}"):
            st.session_state.expenses.drop(index=idx, inplace=True)
            st.session_state.expenses.reset_index(drop=True, inplace=True)
            st.rerun()

# --- Total Amount ---
total = st.session_state.expenses["Amount"].sum()
st.metric("💰 Total Expenses", f"₹ {total:,.2f}")

# --- Category-wise Summary Chart ---
st.subheader("📂 Category-wise Summary")

if not st.session_state.expenses.empty:
    summary = st.session_state.expenses.groupby("Category")["Amount"].sum().reset_index()

    # Seaborn Bar Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=summary, x="Category", y="Amount", palette="muted", ax=ax)

    # Add labels
    for i in ax.containers:
        ax.bar_label(i, fmt="₹%.2f", label_type="edge", fontsize=9)

    ax.set_ylabel("Amount (INR)")
    ax.set_title("Category-wise Expense Breakdown")
    st.pyplot(fig)

    # Optional: Pie Chart
    with st.expander("📈 Show Pie Chart"):
        fig2, ax2 = plt.subplots()
        ax2.pie(summary["Amount"], labels=summary["Category"], autopct="%.1f%%", startangle=90, counterclock=False)
        ax2.set_title("Expense Distribution")
        st.pyplot(fig2)
