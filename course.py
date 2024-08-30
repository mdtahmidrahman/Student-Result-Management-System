from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class CourseClass:
    def __init__(self, root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x500+85+170")
        self.root.config(bg="#f1f0e8")
        self.root.focus_force()

        #title
        title=Label(self.root, text="Manage Course Details",
                    font=("arial", 20, "bold"), bg="#243c77", fg="#ffffff").place(x=10, y=15, width=1330, height=35)

        #variables
        self.var_course=StringVar()
        self.var_duration=StringVar()
        self.var_charges=StringVar()

        #widgets
        lbl_coursename=Label(self.root, text="Course Name", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=60)
        lbl_duration=Label(self.root, text="Course Code", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=100)
        lbl_charges=Label(self.root, text="Credit", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=140)
        lbl_description=Label(self.root, text="Description", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=10, y=180)
        
        #entry fields
        self.txt_coursename=Entry(self.root, textvariable=self.var_course, font=("calibri", 15), bg='#ffffff')
        self.txt_coursename.place(x=150, y=60, width=200)
        txt_duration=Entry(self.root, textvariable=self.var_duration, font=("calibri", 15), bg='#ffffff').place(x=150, y=100, width=200)
        txt_charges=Entry(self.root, textvariable=self.var_charges, font=("calibri", 15), bg='#ffffff').place(x=150, y=140, width=200)
        self.txt_description=Text(self.root, font=("calibri", 15), bg='#ffffff')
        self.txt_description.place(x=150, y=180, width=470, height=200)

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
        lbl_search_courseName=Label(self.root, text="Course Name", font=("calibri", 15, 'bold'), bg='#f1f0e8').place(x=660, y=60)
        txt_search_coursename=Entry(self.root, textvariable=self.var_search, font=("calibri", 15, 'bold'), bg='#ffffff').place(x=810, y=60, width=350)
        btn_update=Button(self.root, text="Search", font=("arial", 14, "bold"), bg="#03867a", fg="white", cursor="hand2", command=self.search).place(x=1190, y=60, width=150, height=30)

        #content
        self.c_frame=Frame(self.root, bd=2, relief=RIDGE)
        self.c_frame.place(x=660, y=100, width=680, height=340)

        scrolly=Scrollbar(self.c_frame, orient=VERTICAL)
        scrollx=Scrollbar(self.c_frame, orient=HORIZONTAL)
        self.coursetable=ttk.Treeview(self.c_frame, columns=("cid", "name", "code", "credit", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.coursetable.xview)
        scrolly.config(command=self.coursetable.yview)

        self.coursetable.heading("cid", text="Course ID")
        self.coursetable.heading("name", text="Name")
        self.coursetable.heading("code", text="Course Code")
        self.coursetable.heading("credit", text="Course Credit")
        self.coursetable.heading("description", text="Description")
        self.coursetable["show"]='headings'
        self.coursetable.column("cid", width=60)
        self.coursetable.column("name", width=180)
        self.coursetable.column("code", width=90)
        self.coursetable.column("credit", width=70)
        self.coursetable.column("description", width=150)
        self.coursetable.pack(fill=BOTH, expand=1)
        self.coursetable.bind("<ButtonRelease>", self.get_data)
        self.show()

    #===============================================================================

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_coursename.config(state=NORMAL)

    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select course from the list first", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)  
                    if op == True:
                        cur.execute("delete from course where name=?", (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Course deleted successfully!", parent= self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def get_data(self, ev):
        self.txt_coursename.config(state='readonly')
        self.txt_coursename
        r = self.coursetable.focus()
        content = self.coursetable.item(r)
        row = content["values"]
        # print(row)
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        # self.var_course.set(row[4])
        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[4])

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Course Name already present", parent=self.root)
                else:
                    cur.execute("insert into course (name, duration, charges, description) values(?, ? , ?, ?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")
    
    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select Course from list", parent=self.root)
                else:
                    cur.execute("update course set duration=?, charges=?, description=? where name=?", (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Update Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from course")
            rows=cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
            rows=cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=CourseClass(root)
    root.mainloop()
