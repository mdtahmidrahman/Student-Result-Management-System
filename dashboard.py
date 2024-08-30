from tkinter import*
from PIL import Image, ImageTk
from course import CourseClass
from student import StudentClass
from result import ResultClass
from report import ReportClass
from tkinter import ttk, messagebox
import sqlite3

class RMS:
    def __init__(self, root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1920x785+0+0")
        self.root.config(bg="#f1f0e8")
        
        #icons
        self.logo_dash=ImageTk.PhotoImage(file="images/logo.png")


        #title
        title=Label(self.root, text="Student Result Management System",
                    padx=10, compound=LEFT, image=self.logo_dash, font=("arial", 20, "bold"), bg="#243c77", fg="white").place(x=0, y=0, relwidth=1, height=50)
        #menu
        M_Frame=LabelFrame(self.root, text="Menus",font=("times new roman", 18), bg="white")
        M_Frame.place(x=10, y=70, width=1514, height=80)

        btn_course=Button(M_Frame, text="Course", font=("arial", 14, "bold"), bg="#2b478c", fg="white", cursor="hand2", command=self.add_course).place(x=120, y=5, width=200, height=40)
        btn_student=Button(M_Frame, text="Student", font=("arial", 14, "bold"), bg="#2b478c", fg="white", cursor="hand2", command=self.add_student).place(x=480, y=5, width=200, height=40)
        btn_result=Button(M_Frame, text="Result", font=("arial", 14, "bold"), bg="#2b478c", fg="white", cursor="hand2", command=self.add_result).place(x=835, y=5, width=200, height=40)
        btn_view=Button(M_Frame, text="View Student Result", font=("arial", 14, "bold"), bg="#2b478c", fg="white", cursor="hand2", command=self.add_report).place(x=1190, y=5, width=200, height=40)
    
        #content_info
        self.bg_img=Image.open("images/bg.png")
        self.bg_img=self.bg_img.resize((1050, 400), Image.LANCZOS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg=Label(self.root, image=self.bg_img).place(x=243, y=180, width=1050, height=400)

        #update_details
        self.lbl_course=Label(self.root, text="Total Courses\n[ 0 ]", font=("montserrat", 20), bd=10, relief=RIDGE, bg="#d8653e", fg="white")
        self.lbl_course.place(x=200, y=600, width=300, height=100)

        self.lbl_student=Label(self.root, text="Total Students\n[ 0 ]", font=("montserrat", 20), bd=10, relief=RIDGE, bg="#697fe2", fg="white")
        self.lbl_student.place(x=600, y=600, width=300, height=100)

        self.lbl_result=Label(self.root, text="Total Results\n[ 0 ]", font=("montserrat", 20), bd=10, relief=RIDGE, bg="#03867a", fg="white")
        self.lbl_result.place(x=1030, y=600, width=300, height=100)


        #footer
        footer=Label(self.root, text="SRMS-Student Result Management System\nContact us for any Technical Support: 019xxxxx607",
                    font=("calibri light", 12), bg="#262626", fg="white").pack(side=BOTTOM, fill=X)
        self.update_details()

    def update_details(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from course")
            cr=cur.fetchall()
            self.lbl_course.config(text=f"Total Course\n[{(len(cr))}]")

            cur.execute("select * from student")
            cr=cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[{(len(cr))}]")

            cur.execute("select * from result")
            cr=cur.fetchall()
            self.lbl_result.config(text=f"Total Results\n[{(len(cr))}]")            

            self.lbl_course.after(200, self.update_details)
        except Exception as ex:
            messagebox.showerror("Error", f"Error duo to {str(ex)}")

    
    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CourseClass(self.new_win)
    
    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=StudentClass(self.new_win)

    def add_result(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ResultClass(self.new_win)

    def add_report(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ReportClass(self.new_win)

        
if __name__=="__main__":
    root=Tk()
    obj=RMS(root)
    root.mainloop()
