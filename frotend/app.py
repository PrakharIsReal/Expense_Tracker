import streamlit as st
import requests
from datetime import datetime
import pandas as pd

API_url = "http://127.0.0.1:8000"  # Your FastAPI backend URL
categories = ["Food", "Travel", "Rent", "Utilities", "Other"]

st.title("💸 Expense Management System")

tab1, tab2 = st.tabs(["📥 Add/Update Expenses", "📊 Analytics"])

# ---------------------- TAB 1: Add/Update Expenses -----------------------
with tab1:
    selected_date = st.date_input("📅 Select Date", datetime(2024, 8, 1))
    submitted = False

    # Fetch existing expenses
    try:
        fetch_response = requests.get(f"{API_url}/expenses/{selected_date}")
        fetch_response.raise_for_status()
        data = fetch_response.json()
    except Exception as e:
        st.error(f"Failed to retrieve expenses: {e}")
        data = []

    if data:
        st.subheader(f"📄 Existing Expenses for {selected_date}")
        st.dataframe(data)
    else:
        st.info("No expenses recorded for this date.")

    st.markdown("---")
    st.subheader("➕ Add New Expenses")

    with st.form(key="expense_form"):
        expenses = []

        for i in range(5):  # Add up to 5 entries
            if i < len(data):
                amount_val = data[i]['amount']
                category_val = data[i]["category"]
                notes_val = data[i]["notes"]
            else:
                amount_val = 0.0
                category_val = "Other"
                notes_val = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount = st.number_input("Amount", min_value=0.0, step=1.0, value=amount_val, key=f"amount_{i}")
            with col2:
                category = st.selectbox("Category", options=categories,
                                        index=categories.index(category_val) if category_val in categories else 0,
                                        key=f"category_{i}")
            with col3:
                notes = st.text_input("Notes", value=notes_val, key=f"notes_{i}")

            if amount > 0:
                expenses.append({
                    'amount': amount,
                    'category': category,
                    'notes': notes
                })

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if expenses:
                try:
                    response = requests.post(f"{API_url}/expenses/{selected_date}", json={"expenses": expenses})
                    if response.status_code in [200, 201]:
                        st.success("Expenses updated successfully!")
                        st.experimental_rerun()
                    else:
                        st.error(f"Failed to update expenses: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("No valid expenses to submit.")

# ---------------------- TAB 2: Analytics ----------------------------------
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        try:
            response = requests.post(f"{API_url}/analytics/", json=payload)
            response.raise_for_status()
            result = response.json()

            if not result:
                st.warning("No analytics data available for the selected range.")
            else:
                data = {
                    "Category": list(result.keys()),
                    "Total": [result[cat]["total"] for cat in result],
                    "Percentage": [result[cat]["percentage"] for cat in result]
                }

                df = pd.DataFrame(data)
                df_sorted = df.sort_values(by="Percentage", ascending=False)

                st.title("📊 Expense Breakdown By Category")
                st.bar_chart(data=df_sorted.set_index("Category")["Percentage"])

                df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
                df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}%".format)

                st.table(df_sorted)

        except Exception as e:
            st.error(f"Failed to fetch analytics: {e}")
