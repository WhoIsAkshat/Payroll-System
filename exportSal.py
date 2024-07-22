from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import sys
import mysql.connector
from mysql.connector import Error
py = sys.executable

# creating window
class EmployeeManagement(Tk):
    def __init__(self):
        super().__init__()
        self.maxsize(500, 450)
        self.minsize(500, 450)
        self.title('EXPORT SALARY SLIP FOR CURRENT MONTH - APEX THERMOCON')
        self.canvas = Canvas(width=500, height=450)
        self.canvas.pack()

        def ceo():
            os.system('%s %s' % (py,'salary-system/convertCEO.py'))
            messagebox.showinfo("Done", "Create Successfully in <folder name>")
        
        def dist():
            os.system('%s %s' % (py,'salary-system/convertSalDist.py'))
            messagebox.showinfo("Done", "Create Successfully in <folder name>")

        
        Label(self, text="EXPORT SALARY SLIP", bg='white', fg='black', font=("garamond", 24, 'bold')).place(x=80, y=20)

        self.addEmp = Button(self, text="SLIP for CEO", width=30, font=('Garamond', 15), command=ceo).place(x=80, y=150)
        self.searchEmp = Button(self, text="SLIP for Distribution", width=30, font=('Garamond', 15), command=dist).place(x=80, y=220)


EmployeeManagement().mainloop()
