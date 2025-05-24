import mysql.connector as my
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.geometry("750x615")
root.title("Student management system")

db = my.connect(host="localhost", user="root", password="Doge2254")
cr = db.cursor()
cr.execute("create database if not exists school")
cr.execute("use school")

for i in range(6, 13):
    cr.execute(f"create table if not exists student{i}(Regn_no int, Name char(50), Class int, Roll_no int, Mobile_no bigint)")

def stu_rec():
    t = Toplevel()
    t.geometry("640x400")
    frame1 = Frame(t)
    frame1.pack()
    e = Entry(frame1, width=50)
    e1 = Entry(frame1, width=50)
    e2 = Entry(frame1, width=50)
    e3 = Entry(frame1, width=50)
    e4 = Entry(frame1, width=50)
    for label, entry in [("Enter the registration number", e), ("Enter the name", e1),
                         ("Enter the class", e2), ("Enter the roll number", e3),
                         ("Enter the mobile number", e4)]:
        Label(frame1, text=label).pack(anchor="w")
        entry.pack(anchor="e")
    Button(frame1, text="Submit", command=lambda: add_db(e, e1, e2, e3, e4, t)).pack(anchor="center")

def add_db(e, e1, e2, e3, e4, t):
    for i in range(6, 13):
        cr.execute(f"Select * from Student{i} where Regn_no=%s", (e.get(),))
        if cr.fetchone():
            messagebox.showerror("Student entry", "Regn no. already taken!")
            return
    cr.execute(f"insert into student{e2.get()} values(%s,%s,%s,%s,%s)", (int(e.get()), str(e1.get()), int(e2.get()), int(e3.get()), int(e4.get())))
    db.commit()
    t.destroy()

def stu_edit(y):
    y.destroy()
    t = Toplevel()
    t.geometry("640x400")
    frame1 = Frame(t)
    frame1.pack()
    e = Entry(frame1, width=50)
    Label(frame1, text="Enter the registration number").pack(anchor="w")
    e.pack(anchor="e")
    vars = [IntVar() for _ in range(5)]
    for text, var in zip(["Regn No.", "Name", "Class", "Roll No.", "Mobile No."], vars):
        Checkbutton(frame1, text=text, variable=var).pack(anchor=W)
    Button(frame1, text="Submit", command=lambda: edit_db(e, t, *vars)).pack(anchor="center")

def edit_db(e, t, v1, v2, v3, v4, v5):
    l = []
    for i in range(6, 13):
        cr.execute(f"Select * from Student{i} where Regn_no=%s", (e.get(),))
        row = cr.fetchone()
        if row:
            l = list(row)
            break
    t.destroy()
    t1 = Toplevel()
    t1.geometry("640x400")
    frame1 = Frame(t1)
    frame1.pack()
    e_fields = []
    for flag, label in zip([v1, v2, v3, v4, v5], ["new registration number", "new name", "new class", "new roll no.", "new phone no."]):
        if flag.get():
            Label(frame1, text=f"Enter the {label}").pack(anchor="w")
            entry = Entry(frame1, width=50)
            entry.pack(anchor="e")
            e_fields.append(entry)
        else:
            e_fields.append(None)
    Button(frame1, text="Submit", command=lambda: editt(e.get(), t1, e_fields, [v1, v2, v3, v4, v5], l)).pack(anchor="center")

def editt(m, t1, e_fields, vars, l):
    new_vals = [entry.get() if var.get() == 1 else l[idx] for idx, (entry, var) in enumerate(zip(e_fields, vars))]
    t1.destroy()
    cr.execute(f"Update Student{l[2]} set Regn_no=%s, Name=%s, Class=%s, Roll_no=%s, Mobile_no=%s where Regn_no=%s",
               (new_vals[0], new_vals[1], new_vals[2], new_vals[3], new_vals[4], m))
    db.commit()

def stu_see():
    t = Toplevel()
    t.geometry("640x480")
    frame1 = Frame(t)
    frame1.pack()
    tr = ttk.Treeview(frame1, columns=("Regn No.", "Name", "Class", "Roll No.", "Mobile no."), show='headings')
    for col in tr["columns"]:
        tr.heading(col, text=col)
    for i in range(6, 13):
        cr.execute(f"Select * from Student{i}")
        for row in cr.fetchall():
            tr.insert('', 'end', values=row)
    tr.pack()

def stu_del():
    t = Toplevel()
    t.geometry("640x400")
    frame1 = Frame(t)
    frame1.pack()
    e = Entry(frame1, width=50)
    Label(frame1, text="Enter the registration number").pack(anchor="w")
    e.pack(anchor="e")
    Button(frame1, text="Submit", command=lambda: del_db(t, e)).pack(anchor="center")

def del_db(t, e):
    for i in range(6, 13):
        cr.execute(f"Delete from Student{i} where Regn_no=%s", (e.get(),))
    db.commit()
    t.destroy()

def stu_sear():
    t = Toplevel()
    t.geometry("640x400")
    frame1 = Frame(t)
    frame1.pack()
    e = Entry(frame1, width=50)
    Label(frame1, text="Enter the registration number").pack(anchor="w")
    e.pack(anchor="e")
    Button(frame1, text="Submit", command=lambda: sear_db(t, e)).pack(anchor="center")

def sear_db(t, e):
    l = None
    for i in range(6, 13):
        cr.execute(f"Select * from Student{i} where Regn_no=%s", (e.get(),))
        row = cr.fetchone()
        if row:
            l = row
            break
    t.destroy()
    if not l:
        messagebox.showinfo("Search result", "No record found")
        return
    t1 = Toplevel()
    t1.geometry("1000x500")
    frame1 = Frame(t1)
    frame1.pack()
    for field, val in zip(["Regn No.", "Name", "Class", "Roll No.", "Mobile No."], l):
        Label(frame1, text=f"{field}: {val}", font=("System", 15)).pack(anchor=CENTER)
    Button(frame1, text="Edit profile", command=lambda: stu_edit(t1)).pack(anchor="center")

frame = Frame(root)
frame.pack()
Button(frame, text="Enter student records", height=2, width=30, command=stu_rec).pack()
Button(frame, text="Edit student records", height=2, width=30, command=lambda: stu_edit(root)).pack()
Button(frame, text="View student records", height=2, width=30, command=stu_see).pack()
Button(frame, text="Delete student records", height=2, width=30, command=stu_del).pack()
Button(frame, text="Search for student records", height=2, width=30, command=stu_sear).pack()
Button(frame, text="Exit", height=2, width=30, command=root.destroy).pack()

root.mainloop()