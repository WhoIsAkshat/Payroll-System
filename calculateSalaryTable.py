from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime, timedelta
import calendar

def days_in_month(month_year):
    year, month = map(int, month_year.split('-'))
    num_days = calendar.monthrange(year, month)[1]
    return num_days

def previous_month_and_year():
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    
    previous_month_name = last_day_of_previous_month.strftime('%B')  # Full month name
    previous_year = last_day_of_previous_month.year
    
    return [previous_month_name, previous_year]

class SalaryCalculation(Tk):
    def __init__(self):
        super().__init__()
        self.maxsize(1400, 800)
        self.minsize(1400, 800)
        self.title('SALARY CALCULATION - APEX THERMOCON')

        self.employee_details = []
        self.create_widgets()
        self.load_employees()

    def create_widgets(self):
        # Create a frame to hold the canvas and scrollbar
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=1)

        # Create a canvas
        self.canvas = Canvas(self.frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add a scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside the canvas
        self.scrollable_frame = Frame(self.canvas)

        # Add that new frame to a window in the canvas
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")

        Label(self.scrollable_frame, text="Salary Calculation", bg='white', fg='black', font=("garamond", 24, 'bold')).grid(row=0, columnspan=7, pady=10)

        columns = ["Employee", "Base Salary", "Old Advance", "New Advance","Att Days", "Overtime", "T", "PF", "ESI", "Adj Advance", "Cheque", "Cash", "Total", "Bonus","Remaining_Advance"]
        for col_num, col_name in enumerate(columns):
            Label(self.scrollable_frame, text=col_name, bg='white', font=('garamond', 10, 'bold')).grid(row=1, column=col_num, padx=5)

        self.entries = []

        Button(self.scrollable_frame, text="Load Saved Data", command=self.load_saved_data).grid(row=0, column=10, pady=10)
        Button(self.scrollable_frame, text="Load Details", command=self.load_employee_details).grid(row=0, column=8, pady=10)
        Button(self.scrollable_frame, text="Save", command=self.save_data).grid(row=0, column=9, pady=10)
        Button(self.scrollable_frame, text="Publish", command=self.publish_salary).grid(row=0, column=12, pady=10)
        Button(self.scrollable_frame, text="Calculate", command=self.calculate_salary).grid(row=0, column=11, pady=10)

    def load_employees(self):
        try:
            conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
            cursor = conn.cursor()
            cursor.execute("SELECT emp_id, emp_name, dept FROM emp")
            employees = cursor.fetchall()

            for row_num, emp in enumerate(employees, start=3):
                emp_id, emp_name, dept = emp
                self.employee_details.append({"emp_id": emp_id, "emp_name": emp_name, "dept": dept})
                Label(self.scrollable_frame, text=f"{emp_name} - {dept}", bg='white', font=('garamond', 10, 'bold')).grid(row=row_num, column=0, padx=5, pady=5)
                row_entries = [Entry(self.scrollable_frame, width=10) for _ in range(14)]
                for col_num, entry in enumerate(row_entries, start=1):
                    entry.grid(row=row_num, column=col_num, padx=5)
                self.entries.append(row_entries)

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")

    def load_employee_details(self):
        try:
            conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
            cursor = conn.cursor()

            current_date = datetime.now()
            first_day_of_current_month = current_date.replace(day=1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            current_yyyy_mm = last_day_of_previous_month.strftime('%Y-%m')
            total_days = days_in_month(current_yyyy_mm)

            for row_num, emp in enumerate(self.employee_details, start=3):
                emp_id = emp["emp_id"]
                cursor.execute("SELECT emp_name, salary, Rem_Advance, dept,pf,esi FROM emp WHERE emp_id = %s", (emp_id,))
                emp_details = cursor.fetchone()
                cursor.execute("SELECT attendance_percentage, total_overtime_hours, refreshment_days FROM attendance_summary WHERE emp_id = %s AND month = %s", (emp_id, current_yyyy_mm))
                attendance_details = cursor.fetchone()

                if emp_details and attendance_details:
                    attendance_days = round(total_days * (attendance_details[0] / 100))
                    data = {
                        "Base Salary": emp_details[1],
                        "Old Advance": emp_details[2],
                        "New Advance": 0,
                        "Attendance Days": attendance_days,
                        "Total Overtime Hours": attendance_details[1] if attendance_details[1] else 0,
                        "Refreshments": attendance_details[2] if attendance_details[2] else 0
                    }
                    for col_num, key in enumerate(data, start=0):
                        self.entries[row_num-3][col_num].delete(0, END)
                        self.entries[row_num-3][col_num].insert(0, data[key])
                    
                    # Set Adj Advance as Old Advance - New Advance
                    adj_advance = emp_details[2] - 0
                    self.entries[row_num-3][8].delete(0, END)
                    self.entries[row_num-3][8].insert(0, adj_advance)
                    self.entries[row_num-3][6].delete(0, END)
                    self.entries[row_num-3][6].insert(0, 0)
                    self.entries[row_num-3][7].delete(0, END)
                    self.entries[row_num-3][7].insert(0, 0)
                    self.entries[row_num-3][9].delete(0, END)
                    self.entries[row_num-3][9].insert(0, 0)
                    self.entries[row_num-3][10].delete(0, END)
                    self.entries[row_num-3][10].insert(0, 0)
                    self.entries[row_num-3][11].delete(0, END)
                    self.entries[row_num-3][11].insert(0, 0)
                    self.entries[row_num-3][13].delete(0, END)
                    self.entries[row_num-3][13].insert(0, 0)

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")

    def load_saved_data(self):
        try:
            conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
            cursor = conn.cursor()
            m = previous_month_and_year()
            month = m[0]
            year = m[1]
            for row_num, emp in enumerate(self.employee_details, start=3):
                emp_id = emp["emp_id"]
                cursor.execute("SELECT base, old_adv, new_adv, att_d, overtime, t, pf, esi, adj_adv, cheque, cash, total, bonus, rem_adv FROM save_data WHERE emp_id = %s AND month = %s AND year = %s", (emp_id,month,year))
                saved_data = cursor.fetchone()
                if saved_data:
                    total_days = days_in_month(datetime.now().strftime('%Y-%m'))
                    attendance_days = total_days * (saved_data[2] / 100)
                    for col_num, value in enumerate(saved_data):
                        self.entries[row_num-3][col_num].delete(0, END)
                        self.entries[row_num-3][col_num].insert(0, value)
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")

    def save_data(self):
        try:
            try:
                conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
                cursor = conn.cursor()
                m = previous_month_and_year()
                month = m[0]
                year = m[1]

                cursor.execute("SELECT month ,year from save_data")
                data_mm_yy = cursor.fetchone()
                if month != data_mm_yy[0] and year != data_mm_yy[1]:
                    cursor.execute("truncate table save_data")
                    conn.commit()
                    
                conn.close()

            except mysql.connector.Error as err:
                print(err)
                messagebox.showerror("Error", f"Something went wrong: {err}")

            conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
            cursor = conn.cursor()
            
            for row_num, emp in enumerate(self.employee_details, start=3):
                emp_id = emp["emp_id"]
                m = previous_month_and_year()
                month = m[0]
                year = m[1]

                data = list(entry.get() for entry in self.entries[row_num-3])
                data[0:12] = map(float, data[0:12])
                data[13] = float(data[13])  # Convert elements from index 2 to 13 to int
                data = tuple(data)

                # Combine emp_id, emp_name, and data into a single tuple for the execute statement
                params = (emp_id, emp["emp_name"]) + data + (month, year)
                
                query = f"""
                    REPLACE INTO save_data 
                    (emp_id, emp_name, base, old_adv, new_adv, att_d, overtime, t, pf, esi, adj_adv, cheque, cash, total, bonus, rem_adv, month, year) 
                    VALUES 
                    {params}
                """
                cursor.execute(query)
                conn.commit()

            conn.close()
            messagebox.showinfo("Success", "Data saved successfully")
        
        except mysql.connector.Error as err:
            print(err)
            messagebox.showerror("Error", f"Something went wrong: {err}")

    def calculate_salary(self):
        try:
            for row_num, emp in enumerate(self.employee_details, start=3):
                base_salary = float(self.entries[row_num-3][0].get())
                rem_advance = float(self.entries[row_num-3][1].get())
                new_advance = float(self.entries[row_num-3][2].get())
                total_overtime_hours = float(self.entries[row_num-3][4].get())
                refreshments = float(self.entries[row_num-3][5].get())
                pf = float(self.entries[row_num-3][6].get())
                esi = float(self.entries[row_num-3][7].get())
                adj_advance = float(self.entries[row_num-3][8].get())
                cheque = float(self.entries[row_num-3][9].get() or 0)  # Default to 0 if empty
                mydate = datetime.now()
                first_day_of_current_month = mydate.replace(day=1)
                last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
                prev_month = last_day_of_previous_month.strftime('%Y-%m')
                t_d = days_in_month(prev_month)
                attendance_percentage = float(self.entries[row_num-3][3].get()) / t_d

                new_rem = rem_advance + new_advance
                if adj_advance > new_rem:
                    messagebox.showerror("Error", "Adjusted Advance cannot be greater than Old Advance")
                    return

                total_salary = round((base_salary * attendance_percentage) + ((total_overtime_hours / 8) / t_d) * base_salary + refreshments * 8 - pf - esi - adj_advance)
                bonus = 'NA'
                if attendance_percentage == 1.0 and emp['dept'] == 'CNC':
                    if emp["emp_name"] not in ['Sunil Singh', 'Bahadur Singh']:
                        total_salary += 200
                        bonus = 'Y'
                    else:
                        bonus = 'N'
                elif attendance_percentage < 100.0 and emp['dept'] == 'CNC':
                    bonus = 'N'
                self.entries[row_num-3][11].delete(0, END)
                self.entries[row_num-3][11].insert(0, total_salary)
                self.entries[row_num-3][12].delete(0, END)
                self.entries[row_num-3][12].insert(0, bonus)
                cash = total_salary - cheque
                self.entries[row_num-3][10].delete(0, END)
                self.entries[row_num-3][10].insert(0, cash)
                self.entries[row_num-3][13].delete(0, END)
                self.entries[row_num-3][13].insert(0, new_rem-adj_advance)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all fields")

    def publish_salary(self):
        try:
            conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
            cursor = conn.cursor()
            mydate1 = datetime.now()
            first_day_of_current_month1 = mydate1.replace(day=1)
            last_day_of_previous_month1 = first_day_of_current_month1 - timedelta(days=1)
            prev_month = last_day_of_previous_month1.strftime('%Y-%m')
            t_d1 = days_in_month(prev_month)
            prev_month_date = last_day_of_previous_month1.strftime('%Y-%m-%d')
            for row_num, emp in enumerate(self.employee_details, start=3):
                emp_id = emp["emp_id"]
                base_salary = float(int(self.entries[row_num-3][0].get()))
                base_att = base_salary * (int(self.entries[row_num-3][3].get()) / t_d1)
                pf = self.entries[row_num-3][6].get()
                esi = self.entries[row_num-3][7].get()
                total_overtime_hours = self.entries[row_num-3][4].get()
                adj_advance = self.entries[row_num-3][8].get()
                refreshments = self.entries[row_num-3][5].get()

                old_adv = self.entries[row_num-3][1].get()
                new_adv = self.entries[row_num-3][2].get()
                rem_adv = self.entries[row_num-3][13].get()

                m = previous_month_and_year()
                current_month_name = m[0]
                curr_year = m[1]
                curr_date = datetime.now().strftime('%Y-%m-%d')

                total_salary = self.entries[row_num-3][11].get()
                bonus_status = self.entries[row_num-3][12].get()
                cheque = self.entries[row_num-3][9].get()
                cash = self.entries[row_num-3][10].get()

                if float(adj_advance) > float(self.entries[row_num-3][1].get()):
                    messagebox.showerror("Error", "Adjusted Advance cannot be greater than Old Advance")
                    return

                cursor.execute(
                    "REPLACE INTO pay (emp_id, emp_name, base, base_att, pf, esi, overtime, adv_deducted, refreshments, month, year, total_salary, bonus_status, cheque, cash,old_adv,new_adv) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (emp_id, emp["emp_name"], base_salary, base_att, pf, esi, total_overtime_hours, adj_advance, int(refreshments) * 8, current_month_name, curr_year, total_salary, bonus_status, cheque, cash,old_adv,new_adv)
                )
                conn.commit()
                cursor.execute("INSERT INTO advances (emp_id, amount, day_date, type) VALUES (%s, %s, %s, %s)", (emp_id, new_adv, prev_month_date, "CR"))
                conn.commit()
                cursor.execute("INSERT INTO advances (emp_id, amount, day_date, type) VALUES (%s, %s, %s, %s)", (emp_id, adj_advance, curr_date, "DR"))
                conn.commit()
                cursor.execute("UPDATE emp SET Rem_Advance = Rem_Advance - %s WHERE emp_id = %s", (int(adj_advance)-int(new_adv), emp_id))
                conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Salary published successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")

SalaryCalculation().mainloop()
