from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import mysql.connector

# creating window
class AttendanceManagement(Tk):
    def __init__(self):
        super().__init__()
        self.maxsize(720, 600)
        self.minsize(720, 600)
        self.title('ATTENDANCE MANAGEMENT - APEX THERMOCON')
        self.canvas = Canvas(width=720, height=600)
        self.canvas.pack()
        
        self.emp_id = IntVar()
        self.month = StringVar()
        
        # label and input box
        Label(self, text="Attendance Management", bg='white', fg='black', font=("garamond", 24, 'bold')).place(x=200, y=20)
        Label(self, text='Employee ID', bg='white', font=('garamond', 10, 'bold')).place(x=90, y=70)
        Entry(self, textvariable=self.emp_id, width=30).place(x=250, y=70)
        Label(self, text='Month (YYYY-MM)', bg='white', font=('garamond', 10, 'bold')).place(x=90, y=100)
        Entry(self, textvariable=self.month, width=30).place(x=250, y=100)
        Button(self, text="Load Days", command=self.load_days).place(x=450, y=95)
        
        self.attendance_vars = []
        self.attendance_frame = Frame(self)
        self.attendance_frame.place(x=70, y=130)
        
        Button(self, text="Submit", width=15, command=self.submit_attendance).place(x=290, y=520)

    def load_days(self):
        month_str = self.month.get()
        try:
            # month_date = datetime.strptime(month_str, "%Y-%m")
            # days_in_month = (month_date.replace(month=month_date.month % 12 + 1, day=1) - month_date).days
            month_date = datetime.strptime(month_str, "%Y-%m")
            next_month = month_date.replace(day=28) + timedelta(days=4)
            days_in_month = (next_month - timedelta(days=next_month.day)).day
        except ValueError:
            messagebox.showerror("Error", "Invalid month format. Use YYYY-MM.")
            return

        for widget in self.attendance_frame.winfo_children():
            widget.destroy()

        self.attendance_vars.clear()
        max_rows = 10  # Maximum number of rows before moving to the next column
        for day in range(1, days_in_month + 1):
            row = (day - 1) % max_rows
            col = (day - 1) // max_rows * 4  # Each entry requires 4 columns
            date = month_date.replace(day=day)
            day_of_week = date.strftime('%a')  # Get day of the week as a three-letter abbreviation
            Label(self.attendance_frame, text=f"{day} ({day_of_week})", font=('garamond', 10, 'bold')).grid(row=row, column=col, padx=5, pady=5)
            present_var = StringVar()
            overtime_var = StringVar()
            self.attendance_vars.append((present_var, overtime_var))
            Entry(self.attendance_frame, textvariable=present_var, width=5).grid(row=row, column=col + 1, padx=5, pady=5)
            Entry(self.attendance_frame, textvariable=overtime_var, width=5).grid(row=row, column=col + 2, padx=5, pady=5)

        self.check_overtime_permission()

    def check_overtime_permission(self):
        employee_id = self.emp_id.get()
        try:
            self.conn = mysql.connector.connect(host='localhost',
                                                database='salary',
                                                user='root', password='123456')
            self.myCursor = self.conn.cursor()
            self.myCursor.execute("SELECT overtime FROM emp WHERE emp_id = %s", (employee_id,))
            result = self.myCursor.fetchone()
            self.conn.close()
            
            if result and result[0] == 'Y':
                self.allow_overtime = True
                for present_var, overtime_var in self.attendance_vars:
                    overtime_var.set('')
                    present_var.set('P')
            else:
                self.allow_overtime = False
                for present_var, overtime_var in self.attendance_vars:
                    overtime_var.set('N/A')
                    present_var.set('P')
                    overtime_var.trace_add('write', lambda *args: overtime_var.set('N/A'))
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")

    def submit_attendance(self):
        employee_id = self.emp_id.get()
        month_str = self.month.get()
        try:
            month_date = datetime.strptime(month_str, "%Y-%m")
            days_in_month = (month_date.replace(month=month_date.month % 12 + 1, day=1) - month_date).days
        except ValueError:
            messagebox.showerror("Error", "Invalid month format. Use YYYY-MM.")
            return
        
        attendance_data = []
        for day in range(1, days_in_month + 1):
            present_var = self.attendance_vars[day-1][0].get()
            overtime_var = self.attendance_vars[day-1][1].get()
            attendance_data.append((employee_id, f"{month_str}-{day:02}", present_var, overtime_var))
        
        try:
            # Calculate total attendance and overtime
            total_days = len(attendance_data)
            present_days = sum(1 for data in attendance_data if data[2] == 'P')
            total_overtime_hours = sum(float(data[3]) for data in attendance_data if self.is_float(data[3]) and data[2] == 'P')                
            refreshment_days = len([float(data[3]) for data in attendance_data if self.is_float(data[3]) and data[2] == 'P' and datetime.strptime(data[1], "%Y-%m-%d").weekday() != 6 and float(data[3])>=3.0])
            # Apply rules
            holidays = [data[1] for data in attendance_data if data[2] == 'A']
            holiday_days = [datetime.strptime(holiday, "%Y-%m-%d").weekday() for holiday in holidays]
            additional_holidays = 0
            excluded_holidays = set()

            # Remove Sundays as paid leaves
            for i in holiday_days:
                if i==6:
                    present_days += 1

            if self.allow_overtime:
                # Rule 1: A person can't have overtime for the day they were absent
                for i in range(total_days):
                    if attendance_data[i][2] == 'A':
                        attendance_data[i] = (attendance_data[i][0], attendance_data[i][1], attendance_data[i][2], 'N/A')
                
                # Rule 2: Any 3 consecutive holidays result in an additional holiday
                if len(holidays) == 3:
                    i=0
                    while i < (len(holidays) - 2):
                        if (datetime.strptime(holidays[i+2], "%Y-%m-%d") - datetime.strptime(holidays[i], "%Y-%m-%d")).days == 2:
                            if ((datetime.strptime(holidays[i], "%Y-%m-%d").weekday() == 6 and datetime.strptime(holidays[i+1], "%Y-%m-%d").weekday() == 0 and datetime.strptime(holidays[i+2], "%Y-%m-%d").weekday() == 1) or
                                (datetime.strptime(holidays[i], "%Y-%m-%d").weekday() == 4 and datetime.strptime(holidays[i+1], "%Y-%m-%d").weekday() == 5 and datetime.strptime(holidays[i+2], "%Y-%m-%d").weekday() == 6)):
                                i += 1
                            else:
                                additional_holidays += 1
                                excluded_holidays.update(holidays[i:i+3])
                                i+=3
                        else: 
                            i+=1

                # Rule 3: (4<=x<=6  +1) (7<=x<=12  +2) (13<=x<=18  +3)
                weekday_holidays = [holiday for holiday in holidays if datetime.strptime(holiday, "%Y-%m-%d").weekday() != 6 and holiday not in excluded_holidays]
                if len(weekday_holidays) >= 4 and len(weekday_holidays) <= 6:
                    additional_holidays += 1
                elif len(weekday_holidays) >= 7 and len(weekday_holidays) <= 12:
                    additional_holidays += 2
                elif len(weekday_holidays) >= 13 and len(weekday_holidays) <= 18:
                    additional_holidays += 3

            else: # no overtime
                #check for available holidays in the year
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                                        database='salary',
                                                        user='root', password='123456')
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("SELECT holidays FROM remaining_holidays WHERE emp_id = %s", (employee_id,))
                    holiday_result = self.myCursor.fetchone()[0]
                    if (holiday_result - (total_days-present_days)) >= 0:
                        additional_holidays = 0
                        edit_holiday = holiday_result - (total_days-present_days)
                        self.myCursor.execute("UPDATE remaining_holidays set holidays = %s WHERE emp_id = %s", (edit_holiday, employee_id))
                        self.conn.commit()
                        self.conn.close()
                    else:
                        additional_holidays = (total_days-present_days) - holiday_result
                        edit_holiday = 0
                        self.myCursor.execute("UPDATE remaining_holidays set holidays = %s WHERE emp_id = %s", (edit_holiday, employee_id))
                        self.conn.commit()
                        self.conn.close()
                    
                    present_days = total_days

                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Something went wrong: {err}")

            present_days -= additional_holidays
            attendance_percentage = (present_days / total_days) * 100
            
            # Display detailed daily attendance in a popup
            detailed_attendance = "\n".join([f"Date: {data[1]}, Present: {data[2]}, Overtime: {data[3]}" for data in attendance_data])
            messagebox.showinfo("Attendance Details", detailed_attendance)
            
            # Store summarized data in the database
            self.conn = mysql.connector.connect(host='localhost',
                                                database='salary',
                                                user='root', password='123456')
            self.myCursor = self.conn.cursor()
            self.myCursor.execute(
                "REPLACE INTO attendance_summary(emp_id, month, attendance_percentage, total_overtime_hours, refreshment_days) VALUES (%s, %s, %s, %s, %s)",
                (employee_id, month_str, attendance_percentage, total_overtime_hours, refreshment_days)
            )
            self.conn.commit()
            
            messagebox.showinfo("Attendance Summary", f"Attendance: {present_days}/{total_days} days\nAttendance Percentage: {attendance_percentage:.2f}%\nTotal Overtime Hours: {total_overtime_hours:.2f}\nRefreshment: {refreshment_days}")
            
            self.myCursor.close()
            self.conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

AttendanceManagement().mainloop()