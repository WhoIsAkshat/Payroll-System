from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import mysql.connector
from mysql.connector import Error
py = sys.executable

import calendar

def days_in_month(month_year):
    # Split the input string to get month and year
    year,month = map(int, month_year.split('-'))
    # Use the calendar module to get the number of days in the month
    num_days = calendar.monthrange(year, month)[1]
    return num_days

#creating window
class Search(Tk):
    def __init__(self):
        super().__init__()
        f = StringVar()
        g = StringVar()
        self.maxsize(1100,500)
        self.minsize(1100,500)
        self.canvas = Canvas(width=1200, height=500)
        self.title('SEARCH EMPLOYEE ATTENDANCE - APEX THERMOCON')
        self.canvas.pack()
        l1=Label(self,text="Search Attendance",bg='white', font=("Garamond",20,'bold')).place(x=430,y=20)
        l = Label(self, text="Search By",bg='white', font=("Garamond", 15, 'bold')).place(x=260, y=96)

        def insert(data,name):
            self.listTree.delete(*self.listTree.get_children())
            
            for row in data:
                try:
                    connection = mysql.connector.connect(host='localhost',
                                                        database='salary',
                                                        user='root',
                                                        password='123456')
                    query = f"select holidays from remaining_holidays where emp_id={row[0]}"
                    cursor = connection.cursor()
                    cursor.execute(query)
                    result = cursor.fetchone()
                    query = f"select emp_name from emp where emp_id={row[0]}"
                    cursor = connection.cursor()
                    cursor.execute(query)
                    name = cursor.fetchone()
                    if result:
                        holidays = result[0]
                    else:
                        holidays = "NA"
                except Error:
                    print("Error while connecting to MySQL", Error)
                dd = days_in_month(row[1])
                da = round((row[2]/100)*dd)
                dss = str(da) + "/" + str(dd)
                self.listTree.insert("", 'end', text=row[0], values=(name[0], row[1], dss, row[3], row[4]*8))
        
        def ge():
            if (len(g.get())) == 0:
                messagebox.showinfo('Error', 'First select an item')
            elif (len(f.get())==0 and g.get()!='All Employees'):
                messagebox.showinfo('Error', 'Enter the '+g.get())
            elif g.get() == 'Employee ID':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                                        database='salary',
                                                        user='root',
                                                        password='123456')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from attendance_summary where emp_id = %s", [f.get()])
                    self.pc = self.mycursor.fetchall()
                    self.mycursor.execute("Select emp_name from emp where emp_id = %s", [f.get()])
                    self.ename = self.mycursor.fetchone()
                    if self.pc:
                        insert(self.pc,self.ename)
                    else:
                        messagebox.showinfo("Oop's","Employee ID not found")
                except Error:
                    messagebox.showerror("Error","Something went wrong")
            elif g.get() == 'Month and Year(YYYY-MM)':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                                        database='salary',
                                                        user='root',
                                                        password='123456')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from attendance_summary where month = %s", [f.get()])
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        insert(self.pc," ")
                    else:
                        messagebox.showinfo("Oop's","Database is empty!")
                except Error:
                    messagebox.showerror("Error","Something went wrong")

        b=Button(self,text="Find",width=15,bg='white',font=("Courier new",10,'bold'),command=ge).place(x=700,y=138)
        c=ttk.Combobox(self,textvariable=g,values=["Employee ID","Month and Year(YYYY-MM)"],width=40,state="readonly").place(x = 380, y = 100)
        en = Entry(self,textvariable=f,width=43).place(x=380,y=155)
        la = Label(self, text="Enter",bg='white', font=("Garamond", 15, 'bold')).place(x=300, y=150)

        def handle(event):
            if self.listTree.identify_region(event.x,event.y) == "separator":
                return "break"

        self.listTree = ttk.Treeview(self, height=13,columns=("Employee Name",'Month', 'Attendance',"Total Overtime Hours", 'Refreshments'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.listTree.configure(yscrollcommand=self.vsb.set)
        self.listTree.heading("#0", text='Emp ID', anchor='center')
        self.listTree.column("#0", width=70, anchor='center')
        self.listTree.heading("Employee Name", text='Employee Name')
        self.listTree.column("Employee Name", width=250, anchor='center')
        self.listTree.heading("Month", text='Year-Month')
        self.listTree.column("Month", width=250, anchor='center')
        self.listTree.heading("Attendance", text='Attendance')
        self.listTree.column("Attendance", width=200, anchor='center')
        self.listTree.heading("Total Overtime Hours", text='Total Overtime Hours')
        self.listTree.column("Total Overtime Hours", width=150, anchor='center')
        self.listTree.heading("Refreshments", text='Refreshments')
        self.listTree.column("Refreshments", width=100, anchor='center')
        self.listTree.bind('<Button-1>', handle)
        self.listTree.place(x=40, y=200)
        self.vsb.place(x=1060,y=200,height=287)
        ttk.Style().configure("Treeview", font=('Garamond', 15))
Search().mainloop()


