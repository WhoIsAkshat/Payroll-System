from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import calendar

class Search(Tk):
    def __init__(self):
        super().__init__()
        f = StringVar()
        g = StringVar()
        self.maxsize(1300, 500)
        self.minsize(1300, 500)
        self.canvas = Canvas(width=1200, height=500)
        self.title('VIEW PAY DETAILS - APEX THERMOCON')
        self.canvas.pack()
        l1 = Label(self, text="View Pay Details", bg='white', font=("Garamond", 20, 'bold')).place(x=480, y=20)
        l = Label(self, text="Search By", bg='white', font=("Garamond", 15, 'bold')).place(x=260, y=96)

        def insert(data):
            self.listTree.delete(*self.listTree.get_children())
            for row in data:
                self.listTree.insert("", 'end', text=row[0], values=(row[1], row[2],row[11], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10]))

        def ge():
            if len(g.get()) == 0:
                messagebox.showinfo('Error', 'First select an item')
            elif len(f.get()) == 0:
                messagebox.showinfo('Error', 'Enter the ' + g.get())
            elif g.get() == 'Employee ID':
                try:
                    conn = mysql.connector.connect(host='localhost',
                                                   database='salary',
                                                   user='root',
                                                   password='123456')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM pay WHERE emp_id = %s", (f.get(),))
                    records = cursor.fetchall()
                    if records:
                        insert(records)
                    else:
                        messagebox.showinfo("Oop's", "No records found for the given Employee ID")
                    conn.close()
                except Error as err:
                    messagebox.showerror("Error", f"Something went wrong: {err}")
            elif g.get() == 'Month and Year':
                try:
                    conn = mysql.connector.connect(host='localhost',
                                                   database='salary',
                                                   user='root',
                                                   password='123456')
                    cursor = conn.cursor()
                    xx = f.get().split("-")
                    x = calendar.month_name[int(xx[0])]
                    cursor.execute("SELECT * FROM pay WHERE month = %s AND year = %s",[x,xx[1]])
                    records = cursor.fetchall()
                    if records:
                        insert(records)
                    else:
                        messagebox.showinfo("Oop's", "No records found for the given Month and Year")
                    conn.close()
                except Error as err:
                    messagebox.showerror("Error", f"Something went wrong: {err}")

        b = Button(self, text="Find", width=15, bg='white', font=("Courier new", 10, 'bold'), command=ge).place(x=760, y=100)
        c = ttk.Combobox(self, textvariable=g, values=["Employee ID", "Month and Year"], width=40, state="readonly").place(x=380, y=100)
        en = Entry(self, textvariable=f, width=43).place(x=380, y=155)
        la = Label(self, text="Enter", bg='white', font=("Garamond", 15, 'bold')).place(x=300, y=150)

        def handle(event):
            if self.listTree.identify_region(event.x, event.y) == "separator":
                return "break"

        self.listTree = ttk.Treeview(self, height=13, columns=('emp_name', 'base','base_att', 'pf', 'esi', 'overtime', 'adv_deducted', 'refreshments', 'month', 'year','total_salary'))
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.listTree.yview)
        self.listTree.configure(yscrollcommand=self.vsb.set)
        self.listTree.heading("#0", text='Emp ID', anchor='center')
        self.listTree.column("#0", width=70, anchor='center')
        self.listTree.heading("emp_name", text='Emp Name')
        self.listTree.column("emp_name", width=150, anchor='center')
        self.listTree.heading("base", text='Base Salary')
        self.listTree.column("base", width=130, anchor='center')
        self.listTree.heading("base_att", text='Net Base (Att)')
        self.listTree.column("base_att", width=130, anchor='center')
        self.listTree.heading("pf", text='PF')
        self.listTree.column("pf", width=80, anchor='center')
        self.listTree.heading("esi", text='ESI')
        self.listTree.column("esi", width=80, anchor='center')
        self.listTree.heading("overtime", text='Overtime')
        self.listTree.column("overtime", width=100, anchor='center')
        self.listTree.heading("adv_deducted", text='Adv Deducted')
        self.listTree.column("adv_deducted", width=100, anchor='center')
        self.listTree.heading("refreshments", text='Refreshments')
        self.listTree.column("refreshments", width=100, anchor='center')
        self.listTree.heading("month", text='Month')
        self.listTree.column("month", width=70, anchor='center')
        self.listTree.heading("year", text='Year')
        self.listTree.column("year", width=70, anchor='center')
        self.listTree.heading("total_salary", text='Total Salary')
        self.listTree.column("total_salary", width=150, anchor='center')
        self.listTree.bind('<Button-1>', handle)
        self.listTree.place(x=30, y=200)
        self.vsb.place(x=1245, y=200, height=287)
        ttk.Style().configure("Treeview", font=('Garamond', 12))

Search().mainloop()
