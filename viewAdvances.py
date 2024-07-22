from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import mysql.connector
import calendar
from mysql.connector import Error
py = sys.executable

#creating window
class Search(Tk):
    def __init__(self):
        super().__init__()
        f = StringVar()
        g = StringVar()
        self.maxsize(800,500)
        self.minsize(800,500)
        self.canvas = Canvas(width=1200, height=500)
        self.title('VIEW ADVANCE DETAILS- APEX THERMOCON')
        self.canvas.pack()
        l1=Label(self,text="View Advances",bg='white', font=("Garamond",20,'bold')).place(x=280,y=20)
        l = Label(self, text="Search By",bg='white', font=("Garamond", 15, 'bold')).place(x=60, y=96)

        def insert(data):
            self.listTree.delete(*self.listTree.get_children())
            for row in data:
                self.listTree.insert("", 'end', text=row[0], values=(row[1], row[2],row[3]))
        
        def ge():
            if (len(g.get())) == 0:
                messagebox.showinfo('Error', 'First select an item')
            elif (len(f.get())==0):
                messagebox.showinfo('Error', 'Enter the '+g.get())
            elif g.get() == 'Employee ID':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                                        database='salary',
                                                        user='root',
                                                        password='123456')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from advances where emp_id = %s", [f.get()])
                    self.pc = self.mycursor.fetchall()
                    self.mycursor.execute("Select Rem_Advance from emp where emp_id = %s", [f.get()])
                    self.pp = self.mycursor.fetchall()
                    slip="The Net Remaining Advance for ID:"+str(f.get())+"\n= "+str(self.pp[0][0])
                    l2=Label(self,text=slip,bg='white', font=("Garamond",12,'bold')).place(x=500,y=140)
                    if self.pc:
                        insert(self.pc)
                    else:
                        messagebox.showinfo("Oop's","Employee with this ID has not taken any Advances")
                except Error:
                    messagebox.showerror("Error","Something went wrong")
            elif g.get() == 'By Year-Month':
                try:
                    conn = mysql.connector.connect(host='localhost',
                                                        database='salary',
                                                        user='root',
                                                        password='123456')
                    mycursor = conn.cursor()
                    if f.get():
                        xx = "'%"+str(f.get())+"%'"
                        mycursor.execute(f"Select * from advances where day_date like {xx}")
                        pc = mycursor.fetchall()
                        if pc:
                            insert(pc)
                        else:
                            messagebox.showinfo("Oop's","No Advances Issued this month.")
                    else:
                        messagebox.showinfo("Oop's","Employee with this ID has not taken any Advances")
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Something went wrong: {err}")

        b=Button(self,text="Find",width=15,bg='white',font=("Courier new",10,'bold'),command=ge).place(x=560,y=100)
        c=ttk.Combobox(self,textvariable=g,values=["Employee ID","By Year-Month"],width=40,state="readonly").place(x = 180, y = 100)
        en = Entry(self,textvariable=f,width=43).place(x=180,y=155)
        la = Label(self, text="Enter",bg='white', font=("Garamond", 15, 'bold')).place(x=100, y=150)

        def handle(event):
            if self.listTree.identify_region(event.x,event.y) == "separator":
                return "break"

        self.listTree = ttk.Treeview(self, height=13,columns=('amount', 'day_date', 'type'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.listTree.configure(yscrollcommand=self.vsb.set)
        self.listTree.heading("#0", text='Emp ID', anchor='center')
        self.listTree.column("#0", width=100, anchor='center')
        self.listTree.heading("amount", text='Amount')
        self.listTree.column("amount", width=270, anchor='center')
        self.listTree.heading("day_date", text='Day and Date')
        self.listTree.column("day_date", width=230, anchor='center')
        self.listTree.heading("type", text='Type')
        self.listTree.column("type", width=100, anchor='center')
        self.listTree.bind('<Button-1>', handle)
        self.listTree.place(x=40, y=200)
        self.vsb.place(x=740,y=200,height=287)
        ttk.Style().configure("Treeview", font=('Garamond', 15))

Search().mainloop()


