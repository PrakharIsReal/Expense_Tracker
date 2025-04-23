from contextlib import contextmanager
import mysql.connector
from logging_setup import setup_logger
from datetime import date, datetime
from pydantic import BaseModel

logger = setup_logger('talking_with_db')

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "392004",
    "database": "expense_manager"
}


@contextmanager
def get_cursor(commit=False):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    try:
        logger.debug("Database connection opened.")
        yield cursor
        if commit:
            conn.commit()
            logger.debug("Changes committed to the database.")
    finally:
        cursor.close()
        conn.close()
        logger.debug("Database connection closed.")


def fetch_expense_for_date(expense_date):
    logger.info(f"Fetching expenses for date: {expense_date}")
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        logger.info(f"Fetched {len(expenses)} expenses.")
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Inserting expense: {expense_date}, {amount}, {category}, {notes}")
    with get_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )
        logger.info("Expense inserted successfully.")


def delete_expenses_for_date(expense_date):
    logger.info(f"Deleting expenses for date: {expense_date}")
    with get_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))
        logger.info("Expenses deleted successfully.")


def fetch_expense_summary(start_date, end_date):
    if isinstance(start_date, datetime):
        start_date = start_date.date()

    if isinstance(end_date, datetime):
        end_date = end_date.date()
    logger.info(f"Fetching summary between {start_date} and {end_date}")
    with get_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
               FROM expenses
               WHERE expense_date BETWEEN %s AND %s
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()

        print(type(start_date))
        logger.info(f"Summary fetched with {len(data)} categories.")
        return data


if __name__ == "__main__":
    summary = fetch_expense_summary("2024-08-02", "2024-08-25")
    for s in summary:
        print(s)
