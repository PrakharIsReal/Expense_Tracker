# 💸 Expense Management System

A simple yet powerful web app built using **Streamlit** (frontend) and **FastAPI** (backend) to track and analyze your daily expenses, with **MySQL** as the database.

---

## 🔧 Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: MySQL (via `mysql-connector-python`)
- **Data Viz**: pandas + Streamlit charts

---

## 🚀 Features

- Add and update daily expenses
- Categorize expenses (Food, Travel, Rent, etc.)
- Visualize your spending with analytics (bar charts + table summary)
- Date-based filtering and viewing
- Lightweight and easy to deploy locally

---

## 🖼️ App Structure

```bash
project/
│
├── backend/
│   ├── main.py           # FastAPI app
│   ├── database.py       # MySQL connection & queries
│   └── models.py         # Pydantic models
│
├── frontend/
│   └── app.py            # Streamlit app
│
├── requirements.txt
└── README.md
