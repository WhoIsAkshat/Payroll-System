from tkinter import *
from tkinter import messagebox
import os
import sys
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime
py=sys.executable

class MainWin(Tk):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas(width=1600, height=800)
        self.canvas.pack()
        self.maxsize(500,400)
        self.minsize(500,400)
        self.title('SALARY MANAGEMENT SYSTEM - APEX THERMOCON')
        self.a = StringVar()
        self.b = StringVar()
        self.mymenu = Menu(self)
        year = datetime.now().year
        month = datetime.now().month
        yes = "Y"

        if month == 1:
            try:
                self.conn = mysql.connector.connect(host='localhost',
                                            database='salary',
                                            user='root', password='123456')
                self.myCursor = self.conn.cursor()
                self.myCursor.execute("select * from reset_holidays where year=%s",[year])
                self.rows = self.myCursor.fetchall()
                if self.rows == []:
                        self.myCursor.execute("insert into reset_holidays values(%s,%s)",[year,yes])
                        self.conn.commit()
                        self.myCursor.execute("UPDATE remaining_holidays SET holidays=12")
                        self.conn.commit()
                self.myCursor.close()
                self.conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error","Something went wrong")


        def a_e():
            os.system('%s %s' % (py, 'salary-system/addEmployee.py'))

        def s_e():
            os.system('%s %s' % (py, 'salary-system/searchEmployee.py'))

        def u_e():
            os.system('%s %s' % (py, 'salary-system/update.py'))

        def adv():
            os.system('%s %s' % (py,'salary-system/advance.py'))

        def c_s():
            os.system('%s %s' % (py,'salary-system/calculateSalary.py'))

        def s_adv():
            os.system('%s %s' % (py,'salary-system/viewAdvances.py'))

        def s_s():
            os.system('%s %s' % (py,'salary-system/viewPay.py'))
        
        def c_a():
            os.system('%s %s' % (py,'salary-system/attendance.py'))
        
        def e_s():
            os.system('%s %s' % (py,'salary-system/exportSal.py'))

        def log():
            conf = messagebox.askyesno("Confirm", "Are you sure you want to Logout?")
            if conf:
                self.destroy()
                os.system('%s %s' % (py, 'salary-system/login.py'))


        self.adv = Button(self, text="ISSUE ADVANCES", width=30, font=('Garamond', 15), command=adv).place(x=70, y=70)
        self.searchAdv = Button(self, text="VIEW ADVANCES", width=30, font=('Garamond', 15), command=s_adv).place(x=70, y=210)
        self.searchSal = Button(self, text="ENTER ATTENDANCE", width=30, font=('Garamond', 15), command=c_a).place(x=70, y=140)
        self.logout = Button(self, text="LOGOUT", width=30, bg="red", font=('Garamond', 15), command=log).place(x=70, y=280)

MainWin().mainloop()
