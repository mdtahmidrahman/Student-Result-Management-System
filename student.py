from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class StudentClass:
    def __init__(self, root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x500+85+170")
        self.root.config(bg="#f1f0e8")
        self.root.focus_force()

        #title
        title=Label(self.root, text="Manage Student Details",
                    font=("arial", 20, "bold"), bg="#243c77", fg="#ffffff").place(x=10, y=15, width=1330, height=35)

        #variables
        self.var_id=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_contact=StringVar()
        self.var_course=StringVar()
        self.var_a_date=StringVar()
        self.var_state=StringVar()
        self.var_city=StringVar()
    
        #widgets
        #col-1
        lbl_id=Label(self.root, text="ID", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=60)
        lbl_name=Label(self.root, text="Name", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=100)
        lbl_email=Label(self.root, text="Email", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=140)
        lbl_gender=Label(self.root, text="Gender", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=180)
        lbl_state=Label(self.root, text="State", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=220)
        lbl_address=Label(self.root, text="Address", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=260)

        #entry fields
        self.txt_id=Entry(self.root, textvariable=self.var_id, font=("calibri", 15), bg='#ffffff')
        self.txt_id.place(x=120, y=60, width=200)
        txt_name=Entry(self.root, textvariable=self.var_name, font=("calibri", 15), bg='#ffffff').place(x=120, y=100, width=200)
        txt_email=Entry(self.root, textvariable=self.var_email, font=("calibri", 15), bg='#ffffff').place(x=120, y=140, width=200)
        self.txt_gender=ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), font=("calibri", 15), state='readonly', justify=CENTER)
        self.txt_gender.place(x=120, y=180, width=200)
        self.txt_gender.current(0)
        txt_state=Entry(self.root, textvariable=self.var_state, font=("calibri", 15), bg='#ffffff').place(x=120, y=220, width=200)

        #col-2
        lbl_dob=Label(self.root, text="Date of Birth", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=330, y=60)
        lbl_contact=Label(self.root, text="Contact", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=330, y=100)
        lbl_addmission=Label(self.root, text="Addmission", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=330, y=140)
        lbl_course=Label(self.root, text="Course", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=330, y=180)
        lbl_city=Label(self.root, text="City", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=330, y=220)

        #entry fields
        self.course_list=[]
        #function_call to update list
        self.fetch_course()
        txt_dob=Entry(self.root, textvariable=self.var_dob, font=("calibri", 15), bg='#ffffff').place(x=450, y=60, width=200)
        txt_contact=Entry(self.root, textvariable=self.var_contact, font=("calibri", 15), bg='#ffffff').place(x=450, y=100, width=200)
        txt_addmisson=Entry(self.root, textvariable=self.var_a_date, font=("calibri", 15), bg='#ffffff').place(x=450, y=140, width=200)
        self.txt_course=ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, font=("calibri", 15), state='readonly', justify=CENTER)
        self.txt_course.place(x=450, y=180, width=200)
        self.txt_course.set("Select")
        txt_city=Entry(self.root, textvariable=self.var_city, font=("calibri", 15), bg='#ffffff').place(x=450, y=220, width=200)

        #text address
        self.txt_address=Text(self.root, font=("calibri", 15), bg='#ffffff')
        self.txt_address.place(x=120, y=260, width=470, height=100)

        #buttons
        self.btn_add=Button(self.root, text="Save", font=("arial", 14, "bold"), bg="#697fe2", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=400, width=110, height=40)
        self.btn_update=Button(self.root, text="Update", font=("arial", 14, "bold"), bg="#03867a", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)
        self.btn_delete=Button(self.root, text="Delete", font=("arial", 14, "bold"), bg="#d8653e", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)
        self.btn_clear=Button(self.root, text="Clear", font=("arial", 14, "bold"), bg="#5296bc", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)
        
        #search panal
        self.var_search=StringVar()
        lbl_search_id=Label(self.root, text="ID", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=660, y=60)
        txt_search_id=Entry(self.root, textvariable=self.var_search, font=("calibri", 15, 'bold'), bg='#ffffff').place(x=810, y=60, width=350)
        btn_search=Button(self.root, text="Search", font=("arial", 14, "bold"), bg="#03867a", fg="white", cursor="hand2", command=self.search).place(x=1190, y=60, width=150, height=30)

        #content
        self.c_frame=Frame(self.root, bd=2, relief=RIDGE)
        self.c_frame.place(x=660, y=100, width=680, height=340)

        scrolly=Scrollbar(self.c_frame, orient=VERTICAL)
        scrollx=Scrollbar(self.c_frame, orient=HORIZONTAL)
        self.coursetable=ttk.Treeview(self.c_frame, columns=("id", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "address"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.coursetable.xview)
        scrolly.config(command=self.coursetable.yview)

        self.coursetable.heading("id", text="ID")
        self.coursetable.heading("name", text="Name")
        self.coursetable.heading("email", text="Email")
        self.coursetable.heading("gender", text="Gender")
        self.coursetable.heading("dob", text="Date of Birth")
        self.coursetable.heading("contact", text="Contact")
        self.coursetable.heading("admission", text="Admission")
        self.coursetable.heading("course", text="Course")
        self.coursetable.heading("state", text="State")
        self.coursetable.heading("city", text="City")
        self.coursetable.heading("address", text="Address")
        self.coursetable["show"]='headings'
        self.coursetable.column("id", width=85)
        self.coursetable.column("name", width=140)
        self.coursetable.column("email", width=150)
        self.coursetable.column("gender", width=65)
        self.coursetable.column("dob", width=90)
        self.coursetable.column("contact", width=120)
        self.coursetable.column("admission", width=100)
        self.coursetable.column("course", width=200)
        self.coursetable.column("state", width=100)
        self.coursetable.column("city", width=70)
        self.coursetable.column("address", width=200)
        self.coursetable.pack(fill=BOTH, expand=1)
        self.coursetable.bind("<ButtonRelease>", self.get_data)
        self.show()

    #===============================================================================

    def clear(self):
        self.show()
        self.var_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_a_date.set("")
        self.var_course.set("Select")
        self.var_state.set("")
        self.var_city.set("")
        self.txt_address.delete("1.0", END)
        self.txt_id.config(state=NORMAL)
        self.var_search.set("")

    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror("Error", "ID should be required", parent=self.root)
            else:
                cur.execute("select * from student where id=?", (self.var_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select student from the list first", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)  
                    if op == True:
                        cur.execute("delete from student where id=?", (self.var_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Student deleted successfully!", parent= self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def get_data(self, ev):
        self.txt_id.config(state='readonly')
        self.txt_id
        r = self.coursetable.focus()
        content = self.coursetable.item(r)
        row = content["values"]
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])
        self.var_a_date.set(row[6])
        self.var_course.set(row[7])
        self.var_state.set(row[8])
        self.var_city.set(row[9])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[10])

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror("Error", "ID should be required", parent=self.root)
            else:
                cur.execute("select * from student where id=?", (self.var_id.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "ID already present", parent=self.root)
                else:
                    cur.execute("insert into student(id, name, email, gender, dob, contact, admission, course, state, city, address) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(
                        self.var_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_a_date.get(),
                        self.var_course.get(),
                        self.var_state.get(),
                        self.var_city.get(),
                        self.txt_address.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")
    
    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror("Error", "ID should be required", parent=self.root)
            else:
                cur.execute("select * from student where id=?", (self.var_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select student from list", parent=self.root)
                else:
                    cur.execute("update student set name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, state=?, city=?, address=? where id=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_a_date.get(),
                        self.var_course.get(),
                        self.var_state.get(),
                        self.var_city.get(),
                        self.txt_address.get("1.0", END),
                        self.var_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Update Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from student")
            rows=cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def fetch_course(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select name from course")
            rows=cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.course_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from student where id=?", (self.var_search.get(),))
            row=cur.fetchone()
            if row != None:
                self.coursetable.delete(*self.coursetable.get_children())
                self.coursetable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No records found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")



if __name__=="__main__":
    root=Tk()
    obj=StudentClass(root)
    root.mainloop()
