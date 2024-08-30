from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class ReportClass:
    def __init__(self, root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x500+160+170")
        self.root.config(bg="#f1f0e8")
        self.root.focus_force()

        #title
        title=Label(self.root, text="View Student Results",
                    font=("arial", 24, "bold"), bg="#f19c00", fg="#243c77").place(x=10, y=15, width=1180, height=50)
        
        #search
        self.var_search=StringVar()
        self.var_id = ""
        lbl_search=Label(self.root, text="Search By ID", font=("calibri", 20, 'bold'), bg='#f1f0e8').place(x=300, y=100)
        txt_search=Entry(self.root, textvariable=self.var_search, font=("calibri", 20), bg='#ffffff').place(x=450, y=100, width=200)
        btn_search=Button(self.root, text="Search", font=("arial", 14, "bold"), bg="#03867a", fg="white", cursor="hand2", command=self.search).place(x=660, y=100, width=100, height=35)
        btn_clear=Button(self.root, text="Clear", font=("arial", 14, "bold"), bg="grey", fg="white", cursor="hand2", command=self.clear).place(x=770, y=100, width=100, height=35)

        #result labels
        lbl_id=Label(self.root, text="ID", font=("calibri", 20, 'bold'), bg='#f1f0e8', bd=2, relief=GROOVE).place(x=90, y=230, width=100, height=50)
        lbl_name=Label(self.root, text="Name", font=("calibri", 20, 'bold'), bg='#f1f0e8', bd=2, relief=GROOVE).place(x=190, y=230, width=180, height=50)
        lbl_course=Label(self.root, text="Course", font=("calibri", 20, 'bold'), bg='#f1f0e8', bd=2, relief=GROOVE).place(x=370, y=230, width=310, height=50)
        lbl_marks_ob=Label(self.root, text="Marks Obtained", font=("calibri", 20, 'bold'), bg='#f1f0e8', bd=2, relief=GROOVE).place(x=680, y=230, width=200, height=50)
        lbl_full_marks=Label(self.root, text="Total Marks", font=("calibri", 20, 'bold'), bg='#f1f0e8', bd=2, relief=GROOVE).place(x=880, y=230, width=150, height=50)
        lbl_per=Label(self.root, text="CGPA", font=("calibri", 20, 'bold'), bg='#f1f0e8', bd=2, relief=GROOVE).place(x=1030, y=230, width=90, height=50)

        self.id=Label(self.root, font=("calibri", 15), bg='#f1f0e8', bd=2, relief=GROOVE)
        self.id.place(x=90, y=280, width=100, height=50)
        self.name=Label(self.root, font=("calibri", 15), bg='#f1f0e8', bd=2, relief=GROOVE)
        self.name.place(x=190, y=280, width=180, height=50)
        self.course=Label(self.root, font=("calibri", 15), bg='#f1f0e8', bd=2, relief=GROOVE)
        self.course.place(x=370, y=280, width=310, height=50)
        self.marks_ob=Label(self.root, font=("calibri", 15), bg='#f1f0e8', bd=2, relief=GROOVE)
        self.marks_ob.place(x=680, y=280, width=200, height=50)
        self.full_marks=Label(self.root, font=("calibri", 15), bg='#f1f0e8', bd=2, relief=GROOVE)
        self.full_marks.place(x=880, y=280, width=150, height=50)
        self.per=Label(self.root, font=("calibri", 15), bg='#f1f0e8', bd=2, relief=GROOVE)
        self.per.place(x=1030, y=280, width=90, height=50)

        #button delete
        btn_delete=Button(self.root, text="Delete", font=("arial", 15, "bold"), bg="red", fg="white", cursor="hand2", command=self.delete).place(x=500, y=350, width=150, height=35)

#=========================================================================================================================
    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "ID should be required", parent=self.root)
            else:
                cur.execute("select * from result where id=?", (self.var_search.get(),))
                row=cur.fetchone()
                if row != None:
                    self.var_id=row[0]
                    self.id.config(text=row[1])
                    self.name.config(text=row[2])
                    self.course.config(text=row[3])
                    self.marks_ob.config(text=row[4])
                    self.full_marks.config(text=row[5])
                    self.per.config(text=row[6])

                else:
                    messagebox.showerror("Error", "No records found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    def clear(self):
        self.var_id=""
        self.id.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks_ob.config(text="")
        self.full_marks.config(text="")
        self.per.config(text="")
        self.var_search.set("")

    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_id=="":
                messagebox.showerror("Error", "Search Student result first", parent=self.root)
            else:
                cur.execute("select * from result where rid=?", (self.var_id,))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Student Result", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)  
                    if op == True:
                        cur.execute("delete from result where rid=?", (self.var_id,))
                        con.commit()
                        messagebox.showinfo("Delete", "Result deleted successfully!", parent= self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

if __name__=="__main__":
    root=Tk()
    obj=ReportClass(root)
    root.mainloop()