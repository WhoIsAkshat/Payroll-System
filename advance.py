from datetime import date, datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import os
import sys
py = sys.executable

#creating window
class issue(Tk):
    def __init__(self):
        super().__init__()
        self.title('ISSUE ADVANCES - APEX THERMOCON')
        self.maxsize(500,800)
        self.canvas = Canvas(width=500, height=400)
        self.canvas.pack()
        b = StringVar()
        c = StringVar()
        self.selected_employee = StringVar()
        ddate = StringVar()
        ddate.set(date.today().strftime("%Y-%m-%d"))
        chq = IntVar()
        csh = IntVar()

        def isb():
            if (len(self.selected_employee.get())) == 0:
                messagebox.showinfo('Error', 'Empty field! Select the Employee.')
            elif int(c.get()) == 0:
                messagebox.showinfo('Error', 'Empty field! Enter the Amount.')
            elif len(ddate.get()) == 0:
                messagebox.showinfo('Error', 'Empty field! Enter the Date.')
            elif (chq.get()+csh.get()) != int(c.get()):
                messagebox.showinfo('Error', 'Wrong Values! Cheque + Cash should equal Amount.')
            else:
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                                        database='salary',
                                                        user='root',
                                                        password='123456')
                    self.mycursor = self.conn.cursor()
                    emp_info = self.selected_employee.get()
                    id = emp_info.split('(')[-1].strip(')')
                    amount = c.get()
                    idate = ddate.get()
                    cq = chq.get()
                    cs = csh.get()
                    self.mycursor.execute("Insert into advances(emp_id,amount,day_date,type,cheque,cash) values (%s,%s,%s,%s,%s,%s)",[id,amount, idate, "CR",cq,cs])
                    self.conn.commit()
                    self.mycursor.execute("UPDATE emp SET Rem_Advance = Rem_Advance + %s where emp_id=%s;", [amount,id])
                    self.conn.commit()
                    messagebox.showinfo("Success", "Successfully Issued!")
                    ask = messagebox.askyesno("Confirm", "Do you want to issue another?")
                    if ask:
                        self.destroy()
                        os.system('%s %s' % (py, 'salary-system/advance.py'))
                    else:
                        self.destroy()
                except Error:
                    messagebox.showerror("Error", "Something went wrong")

        Label(self, text='Issuing Advances',bg = 'white', font=('Garamond', 24)).place(x=135, y=20)
        Label(self, text='Employee:',bg = 'white', font=('Garamond', 15), fg='black').place(x=40, y=80)
        self.employee_combobox = ttk.Combobox(self, textvariable=self.selected_employee, width=40)
        self.employee_combobox.place(x=160, y=86)
        Label(self, text='Amount:',bg = 'white', font=('Garamond', 15), fg='black').place(x=40, y=130)
        Entry(self, textvariable=c, width=40).place(x=165, y=136)
        Label(self, text='Date (Y-m-d):',bg = 'white', font=('Garamond', 15), fg='black').place(x=40, y=180)
        Entry(self, textvariable=ddate, width=40).place(x=165, y=186)
        Label(self, text='Cheque:',bg = 'white', font=('Garamond', 15), fg='black').place(x=40, y=230)
        Entry(self, textvariable=chq, width=40).place(x=165, y=236)
        Label(self, text='Cash:',bg = 'white', font=('Garamond', 15), fg='black').place(x=40, y=280)
        Entry(self, textvariable=csh, width=40).place(x=165, y=286)
        Button(self, text="ISSUE", width=20, command=isb).place(x=170, y=340)
        

        self.load_employees()
    #verifying input
        

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

    
issue().mainloop()