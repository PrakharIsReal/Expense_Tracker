import streamlit as st
from datetime import datetime
import requests

API_url = "http://127.0.0.1:8000"

def add_update_tab():
        global data
        categories = ["Food", "Travel", "Rent", "Utilities", "Other"]
        selected_date = st.date_input("📅 Select Date", datetime(2024, 8, 1))

        # Display existing expenses for the selected date
        fetch_response = requests.get(f"{API_url}/expenses/{selected_date}")
        submitted = False

        if fetch_response.status_code == 200:
            data = fetch_response.json()
            if data:
                st.subheader(f"📄 Existing Expenses for {selected_date}")
                st.dataframe(data)
            else:
                st.info("No expenses recorded for this date.")
        else:
            if not submitted:
                st.error("Failed to retrieve expenses.")

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

                # Only collect if something meaningful is entered
                if amount > 0:  # Ensure non-zero amounts
                    expenses.append({
                        'amount': amount,
                        'category': category,
                        'notes': notes
                    })

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                # Only submit expenses with a positive amount
                filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

                if filtered_expenses:
                    response = requests.post(f"{API_url}/expenses/{selected_date}", json=filtered_expenses)

                    if response.status_code == 200 or response.status_code == 201:
                        st.success("Expenses updated successfully!")
                    else:
                        st.error(f"Failed to update expenses: {response.text}")
                else:
                    st.warning("No valid expenses to submit.")
