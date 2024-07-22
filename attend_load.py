import openpyxl
import mysql.connector
import os
from tkinter import filedialog
from tkinter import Tk, messagebox

def update_database(file_path, host, database, user, password):
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    # Connect to the database
    try:
        conn = mysql.connector.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

    # Load the Excel file
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Read data from the Excel file and update the database
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Skipping the header row
        employee_id, month_str, present_days, total_days, attendance_percentage, total_overtime_hours, refreshment_days, remaining_holidays = row

        # Update attendance_summary table
        try:
            cursor.execute("""
                REPLACE INTO attendance_summary(emp_id, month, attendance_percentage, total_overtime_hours, refreshment_days)
                VALUES (%s, %s, %s, %s, %s)
            """, (employee_id, month_str, attendance_percentage, total_overtime_hours, refreshment_days))
        except mysql.connector.Error as err:
            print(f"Error updating attendance_summary: {err}")

        # Update remaining_holidays table if holidays info is present
        if remaining_holidays is not None:
            try:
                cursor.execute("""
                    UPDATE remaining_holidays
                    SET holidays = %s
                    WHERE emp_id = %s
                """, (remaining_holidays, employee_id))
            except mysql.connector.Error as err:
                print(f"Error updating remaining_holidays: {err}")

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def select_file_and_update_db():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return

    # Update these variables with the database credentials of the other system
    host = "localhost"
    database = "salary"
    user = "root"
    password = "123456"

    update_database(file_path, host, database, user, password)
    messagebox.showinfo("Success", "Database updated successfully.")

if __name__ == "__main__":
    select_file_and_update_db()
