from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime, timedelta
import calendar

def days_in_month(month_year):
    # Split the input string to get month and year
    year,month = map(int, month_year.split('-'))
    # Use the calendar module to get the number of days in the month
    num_days = calendar.monthrange(year, month)[1]
    return num_days


class SalaryCalculation(Tk):
    def __init__(self):
        super().__init__()
        self.maxsize(800, 600)
        self.minsize(800, 600)
        self.title('SALARY CALCULATION - APEX THERMOCON')
        self.canvas = Canvas(width=800, height=600)
        self.canvas.pack()

        self.selected_employee = StringVar()
        self.employee_details = {}

        self.create_widgets()
        self.load_employees()

    def create_widgets(self):
        Label(self, text="Salary Calculation", bg='white', fg='black', font=("garamond", 24, 'bold')).place(x=220, y=10)
        
        Label(self, text='Employee', bg='white', font=('garamond', 10, 'bold')).place(x=70, y=60)
        self.employee_combobox = ttk.Combobox(self, textvariable=self.selected_employee, width=40)
        self.employee_combobox.place(x=240, y=60)
        Button(self, text="Load Details", command=self.load_employee_details).place(x=520, y=55)

        self.detail_labels = {}
        self.detail_entries = {}
        details = ["Base Salary", "Old Advance", "Attendance Percentage", "Total Overtime Hours", "Refreshments", "PF", "ESI", "Adj Advance", "Cheque", "Cash"]
        y_offset = 100
        for detail in details:
            Label(self, text=detail, bg='white', font=('garamond', 10, 'bold')).place(x=70, y=y_offset)
            entry = Entry(self, width=30)
            entry.place(x=240, y=y_offset)
            self.detail_labels[detail] = entry
            y_offset += 40

        Button(self, text="Calculate", command=self.calculate_salary).place(x=200, y=y_offset)
        self.total_label = Label(self, text="", bg='white', font=('garamond', 15, 'bold'))
        self.total_label.place(x=300, y=y_offset)

        self.bonus_label = Label(self, text="", bg='white', font=('garamond', 15, 'bold'))
        self.bonus_label.place(x=450, y=y_offset)
        
        Button(self, text="Publish", command=self.publish_salary).place(x=200, y=y_offset + 40)

    def load_employees(self):
        try:
            conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
            cursor = conn.cursor()
            cursor.execute("SELECT emp_id, emp_name, dept FROM emp")
            employees = cursor.fetchall()
            self.employee_combobox['values'] = [f"{emp[1]}-{emp[2]} ({emp[0]})" for emp in employees]
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")

    def load_employee_details(self):
        emp_info = self.selected_employee.get()
        emp_id = emp_info.split('(')[-1].strip(')')
        try:
            self.conn = mysql.connector.connect(host='localhost', 
                                           database='salary', 
                                           user='root', 
                                           password='123456')
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT emp_name, salary, Rem_Advance,dept FROM emp WHERE emp_id = %s", (emp_id,))
            emp_details = self.cursor.fetchone()
            current_date = datetime.now()
            first_day_of_current_month = current_date.replace(day=1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            current_yyyy_mm = last_day_of_previous_month.strftime('%Y-%m')
            self.cursor.execute("SELECT attendance_percentage, total_overtime_hours, refreshment_days FROM attendance_summary WHERE emp_id = %s AND month = %s", 
                           (emp_id, current_yyyy_mm))
            attendance_details = self.cursor.fetchone()
            
            if emp_details and attendance_details:
                self.employee_details = {
                    "emp_id": emp_id,
                    "emp_name": emp_details[0],
                    "Base Salary": emp_details[1],
                    "Old Advance": emp_details[2],
                    "Attendance Percentage": attendance_details[0] if attendance_details[0] else 0,
                    "Total Overtime Hours": attendance_details[1] if attendance_details[1] else 0,
                    "Refreshments": attendance_details[2] if attendance_details[2] else 0,
                    "Department": emp_details[3]
                }
                for detail in self.employee_details:
                    if detail in self.detail_labels:
                        self.detail_labels[detail].delete(0, END)
                        self.detail_labels[detail].insert(0, self.employee_details[detail])
            
            self.conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")
        self.total_label.config(text="")
        self.bonus_label.config(text="")
        self.detail_labels["Cash"].delete(0, END)
        self.detail_labels["Cheque"].delete(0, END)
        self.detail_labels["PF"].delete(0, END)
        self.detail_labels["ESI"].delete(0, END)
        self.detail_labels["Adj Advance"].delete(0, END)
        self.detail_labels["PF"].insert(0, 0)
        self.detail_labels["ESI"].insert(0, 0)
        self.detail_labels["Adj Advance"].insert(0, 0)

    def calculate_salary(self):
        self.detail_labels["Cash"].delete(0, END)
        self.detail_labels["Cheque"].delete(0, END)
        try:
            base_salary = float(self.detail_labels["Base Salary"].get())
            rem_advance = float(self.detail_labels["Old Advance"].get())
            attendance_percentage = float(self.detail_labels["Attendance Percentage"].get())
            total_overtime_hours = float(self.detail_labels["Total Overtime Hours"].get())
            refreshments = float(self.detail_labels["Refreshments"].get())
            pf = float(self.detail_labels["PF"].get())
            esi = float(self.detail_labels["ESI"].get())
            adj_advance = float(self.detail_labels["Adj Advance"].get())
            mydate = datetime.now()

            ## prev month
            first_day_of_current_month = mydate.replace(day=1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            prev_month = last_day_of_previous_month.strftime('%Y-%m')
            t_d = days_in_month(prev_month)
            if adj_advance > rem_advance:
                messagebox.showerror("Error", "Adjusted Advance cannot be greater than Old Advance")
                return
            
            self.base_att = base_salary*(attendance_percentage / 100)
            total_salary = round((base_salary*(attendance_percentage / 100)) + ((total_overtime_hours/8)/t_d)*base_salary + refreshments*8 - pf - esi - adj_advance)

            self.bonus = 'NA'
            self.bonus_label.config(text=f"Bonus: {self.bonus}")

            if attendance_percentage == 100.0 and self.employee_details['Department'] == 'CNC':
                if str(self.employee_details.get("emp_name")) != 'Sunil Singh' and str(self.employee_details.get("emp_name")) != 'Bahadur Singh':
                    total_salary += 200
                    self.bonus = 'Y'
                    self.bonus_label.config(text=f"Bonus: {self.bonus}")
                else:
                    self.bonus = 'N'
                    self.bonus_label.config(text=f"Bonus: {self.bonus}")
            elif attendance_percentage < 100.0 and self.employee_details['Department'] == 'CNC':
                self.bonus = 'N'
                self.bonus_label.config(text=f"Bonus: {self.bonus}")

            self.total_label.config(text=f"Total: {total_salary:.2f}")
            self.total_value = total_salary
            self.detail_labels["Cash"].insert(0, int(total_salary))
            self.detail_labels["Cheque"].insert(0, 0)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all fields")

    def publish_salary(self):
        if int(self.detail_labels["Cheque"].get()) + int(self.detail_labels["Cash"].get()) != self.total_value:
            messagebox.showerror("Error", "Cheque + Cash is not equal to Total!")
            return
        emp_id = self.employee_details.get("emp_id")
        emp_name = self.employee_details.get("emp_name")
        base_salary = self.detail_labels["Base Salary"].get()
        base_att = self.base_att
        pf = self.detail_labels["PF"].get()
        esi = self.detail_labels["ESI"].get()
        total_overtime_hours = self.detail_labels["Total Overtime Hours"].get()
        adj_advance = self.detail_labels["Adj Advance"].get()
        refreshments = self.detail_labels["Refreshments"].get()
        current_month_name = datetime.now().strftime("%B")
        curr_year = datetime.now().year
        curr_date = datetime.now().strftime('%Y-%m-%d')
        total_salary = self.total_value
        bonus_status = self.bonus
        cheque = self.detail_labels["Cheque"].get()
        cash = self.detail_labels["Cash"].get()
        
        # Check if Adjusted Advance is less than or equal to Old Advance
        if float(adj_advance) > float(self.employee_details.get("Old Advance", 0)):
            messagebox.showerror("Error", "Adjusted Advance cannot be greater than Old Advance")
            return

        try:
            conn = mysql.connector.connect(host='localhost', database='salary', user='root', password='123456')
            cursor = conn.cursor()
            cursor.execute(
                "REPLACE INTO pay (emp_id, emp_name, base, base_att, pf, esi, overtime, adv_deducted, refreshments, month, year,total_salary, bonus_status, cheque, cash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (emp_id, emp_name, base_salary,base_att, pf, esi, total_overtime_hours, adj_advance, int(refreshments)*8, current_month_name, curr_year,total_salary, bonus_status,cheque,cash) 
            )
            conn.commit()
            cursor.execute("Insert into advances(emp_id,amount,day_date,type) values (%s,%s,%s,%s)",[emp_id,adj_advance, curr_date, "DR"])
            conn.commit()
            cursor.execute("UPDATE emp SET Rem_Advance = Rem_Advance - %s where emp_id=%s;", [adj_advance,emp_id])
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Salary published successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")



SalaryCalculation().mainloop()
