from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class ResultClass:
    def __init__(self, root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x500+160+170")
        self.root.config(bg="#f1f0e8")
        self.root.focus_force()

        #title
        title=Label(self.root, text="Add Student Results",
                    font=("arial", 24, "bold"), bg="#f19c00", fg="#243c77").place(x=10, y=15, width=1180, height=50)
        
        #widgets
        #variables
        self.var_id=StringVar()
        self.var_name=StringVar()
        self.var_course=StringVar()
        self.var_marks=StringVar()
        self.var_full_marks=StringVar()
        self.id_list=[]
        self.fetch_id()
        
        lbl_select=Label(self.root, text="Select Student", font=("calibri", 20, 'bold'), bg='#f1f0e8').place(x=50, y=100)
        lbl_name=Label(self.root, text="Name", font=("calibri", 20, 'bold'), bg='#f1f0e8').place(x=50, y=160)
        lbl_course=Label(self.root, text="Course", font=("calibri", 20, 'bold'), bg='#f1f0e8').place(x=50, y=220)
        lbl_marks_ob=Label(self.root, text="Marks Obtained", font=("calibri", 20, 'bold'), bg='#f1f0e8').place(x=50, y=280)
        lbl_full_marks=Label(self.root, text="Full Marks", font=("calibri", 20, 'bold'), bg='#f1f0e8').place(x=50, y=340)

        self.txt_student=ttk.Combobox(self.root, textvariable=self.var_id, values=self.id_list, font=("calibri", 15), state='readonly', justify=CENTER)
        self.txt_student.place(x=280, y=105, width=200)
        self.txt_student.set("Select")
        btn_search=Button(self.root, text="Search", font=("arial", 14, "bold"), bg="#03867a", fg="white", cursor="hand2", command=self.search).place(x=500, y=105, width=100, height=30)

        txt_name=Entry(self.root, textvariable=self.var_name, font=("calibri", 15), bg='#ffffff', state='readonly').place(x=280, y=160, width=320)
        txt_course=Entry(self.root, textvariable=self.var_course, font=("calibri", 15), bg='#ffffff', state='readonly').place(x=280, y=220, width=320)
        txt_marks=Entry(self.root, textvariable=self.var_marks, font=("calibri", 15), bg='#ffffff').place(x=280, y=280, width=320)
        txt_full_marks=Entry(self.root, textvariable=self.var_full_marks, font=("calibri", 15), bg='#ffffff').place(x=280, y=340, width=320)

        #button
        self.btn_add=Button(self.root, text="Submit", font=("arial", 14, "bold"), bg="#697fe2", activebackground="#697fe2",fg="white", cursor="hand2", command=self.add).place(x=300, y=420, width=120, height=35)
        self.btn_clear=Button(self.root, text="Clear", font=("arial", 14, "bold"), bg="#5296bc", activebackground="#5296bc", fg="white", cursor="hand2", command=self.clear).place(x=430, y=420, width=120, height=35)

        #image
        self.bg_img=Image.open("images/result.jpg")
        self.bg_img=self.bg_img.resize((500, 300), Image.LANCZOS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg=Label(self.root, image=self.bg_img).place(x=630, y=100)

#==========================================================================================
    def fetch_id(self):
            con=sqlite3.connect(database="rms.db")
            cur=con.cursor()
            try:
                cur.execute("select id from student")
                rows=cur.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        self.id_list.append(row[0])
            except Exception as ex:
                messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select name, course from student where id=?", (self.var_id.get(),))
            row=cur.fetchone()
            if row != None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])                
            else:
                messagebox.showerror("Error", "No records found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def add(self):
            con=sqlite3.connect(database="rms.db")
            cur=con.cursor()
            try:
                if self.var_name.get()=="":
                    messagebox.showerror("Error", "Please first search student record", parent=self.root)
                else:
                    cur.execute("select * from result where id=? and course=?", (self.var_id.get(), self.var_course.get()))
                    row=cur.fetchone()
                    if row != None:
                        messagebox.showerror("Error", "Result already present", parent=self.root)
                    else:
                        def marks_to_cgpa(marks):
                            if marks >= 80:
                                return 4.0
                            elif marks >= 75:
                                return 3.75
                            elif marks >= 70:
                                return 3.5
                            elif marks >= 65:
                                return 3.25
                            elif marks >= 60:
                                return 3.0
                            elif marks >= 55:
                                return 2.75
                            elif marks >= 50:
                                return 2.5
                            elif marks >= 45:
                                return 2.25
                            elif marks >= 40:
                                return 2.0
                            else:
                                return 0.0
                        marks = int(self.var_marks.get())
                        per = float(marks_to_cgpa(marks))
                        cur.execute("insert into result (id, name, course, marks_ob, full_marks, per) values(?, ?, ?, ?, ?, ?)", (
                            self.var_id.get(),
                            self.var_name.get(),
                            self.var_course.get(),
                            self.var_marks.get(),
                            self.var_full_marks.get(),
                            str(per)
                        ))
                        con.commit()
                        messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Error duo to {str(ex)}")
    def clear(self):
        self.var_id.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        
if __name__=="__main__":
    root=Tk()
    obj=ResultClass(root)
    root.mainloop()