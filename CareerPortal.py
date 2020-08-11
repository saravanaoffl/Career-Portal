import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import sys
import os


HEADING_FONT = ("Verdana", 25)
LARGE_FONT = ("Helvetica", 18)
NAME = None

conn = sqlite3.connect('jobportal.db')
c = conn.cursor()

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def create_job_table():
    c.execute('CREATE TABLE IF NOT EXISTS Job(Id INTEGER PRIMARY KEY, Code VARCHAR NOT NULL, Role VARCHAR NOT NULL, Employer VARCHAR NOT NULL) ')

def create_employer_table():
    c.execute('CREATE TABLE IF NOT EXISTS Employer(Id INTEGER PRIMARY KEY, Name VARCHAR NOT NULL, GST VARCHAR NOT NULL, About VARCHAR NOT NULL) ')

def create_applicant_table():
    c.execute('CREATE TABLE IF NOT EXISTS Applicant(Id INTEGER PRIMARY KEY, Name VARCHAR NOT NULL, Age INTEGER NOT NULL, Contact VARCHAR NOT NULL, Code VARCHAR NOT NULL) ')


def create_status_table():
    c.execute('CREATE TABLE IF NOT EXISTS Status(Id INTEGER PRIMARY KEY, Name VARCHAR NOT NULL, Code VARCHAR NOT NULL, Message VARCHAR NOT NULL) ')


def insert_applicant( name, age, contact, code):
    c.execute('INSERT INTO Applicant(Name, Age, Contact, Code) VALUES(?,?,?,?)',(name, age, contact, code,))
    conn.commit()
    messagebox.showinfo(title = "Success", message = "Job Application to Employer successfuly sent")

def insert_employer(name, gst, about):
    c.execute('INSERT INTO Employer(Name, GST, About) VALUES(?,?,?)',(name, gst, about,))
    conn.commit()
    messagebox.showinfo(title = "Success", message = "New Employer was successfully added")
    restart_program()

def insert_job(code, role, employer):
    c.execute('INSERT INTO Job(Code, Role, Employer) VALUES(?,?,?)',(code, role, employer,))
    conn.commit()
    messagebox.showinfo(title = "Success", message = "New Job was successfully added")
    restart_program()

def insert_status(name, code, message):
    c.execute('INSERT INTO Status(Name, Code, Message) VALUES(?,?,?)',(name, code, message,))
    conn.commit()
    restart_program()

def update_status(name, code, message):
    c.execute("""UPDATE Status SET Message = ? WHERE Name = ? AND Code = ? """,(message, name, code,))
    conn.commit()
    messagebox.showinfo(title = "Success", message = "Message sent to Applicant")
    restart_program()


class JobPortal(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "JobPortal")

        container = tk.Frame(self)
        container.pack(side="top", fill ="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for page in (MainPage, ApplicantPage, EmployerPage, ViewAllJobPage, ViewStatusPage, ViewSpecificJobPage, ApplyPage, RegisterPage, PostJobPage, ViewApplicantPage, ContactApplicantPage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)
        
    def dynamic_page(self, page, parent, var):
        if var is not None:
            self.frames[page] = page(parent, self, var)
        
    def show_frame(self, cont):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cont]
        frame.grid()
        frame.tkraise()



class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self, text="MAIN MENU", font = HEADING_FONT)
        option1 = tk.Label(self, text="- APPLICANT PORTAL", font = HEADING_FONT)
        option2 = tk.Label(self, text="- EMPLOYER PORTAL", font = HEADING_FONT)
        

        label.grid(row=0, columnspan= 2,padx = 40, pady=40)
        option1.grid(row=1,column=1,padx = 40, pady=40)
        option2.grid(row=2,column=1,padx = 40, pady=40)
        
        button1 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ApplicantPage))
        button1.grid(row=1, column=2, sticky = "es",padx = 40, pady=40 )
        button2 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(EmployerPage))
        button2.grid(row=2, column=2, sticky = "es",padx = 40, pady=40 )

        
class ApplicantPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="APPLICANT PORTAL", font = HEADING_FONT)
        option1 = tk.Label(self, text="- APPLY FOR A JOB", font = LARGE_FONT)
        option2 = tk.Label(self, text="- VIEW ALL JOBS", font = LARGE_FONT)
        option3 = tk.Label(self, text="- VIEW SPECIFIC JOBS", font = LARGE_FONT)
        option4 = tk.Label(self, text="- VIEW APPLICATION STATUS", font = LARGE_FONT)

        label.grid(row=1, column=1,columnspan=2, padx = 20, pady=20)
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)
        option4.grid(row=5,column=1,padx = 20, pady=20)
        
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(MainPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button2 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ApplyPage))
        button2.grid(row=2, column = 2, sticky = "es",padx = 20, pady=20 )
        button3 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ViewAllJobPage))
        button3.grid(row=3, column = 2, sticky = "es",padx = 20, pady=20 )
        button4 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ViewSpecificJobPage))
        button4.grid(row=4, column = 2, sticky = "es",padx = 20, pady=20 )
        button5 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ViewStatusPage))
        button5.grid(row=5, column = 2, sticky = "es",padx = 20, pady=20 )



class ApplyPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(name, age, contact, code):
            c.execute('SELECT * FROM Job WHERE Code = ?',(code.get(),))
            info = c.fetchall()
            if len(info) == 0:
                messagebox.showinfo(title = "Caution", message = "No such job exists")
                controller.show_frame(ApplyPage)
            else:
                insert_applicant( name.get(), age.get(), contact.get(), code.get())
                message =  "Not Yet Viewed"
                insert_status(name.get(), code.get(), message)
                
        option1 = tk.Label(self, text="- NAME ", font = LARGE_FONT)
        option2 = tk.Label(self, text="- AGE", font = LARGE_FONT)
        option3 = tk.Label(self, text="- CONTACT", font = LARGE_FONT)
        option4 = tk.Label(self, text="- CODE", font = LARGE_FONT)
        
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)
        option4.grid(row=5,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=2,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=3,column=2,padx = 20, pady=20)
        entry3 = tk.Entry(self)
        entry3.grid(row=4,column=2,padx = 20, pady=20)
        entry4 = tk.Entry(self)
        entry4.grid(row=5,column=2,padx = 20, pady=20)
    
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(ApplicantPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Store",
                            command= lambda: wrapper(entry1, entry2, entry3, entry4))
        button1.grid(row=6, columnspan = 3, padx = 20, pady=20 )



class ViewSpecificJobPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(entry):
            c.execute('SELECT * FROM Job WHERE Role = ?',(entry.get(),))
            info = c.fetchall()
            c.execute('SELECT * FROM Job WHERE Employer = ?',(entry.get(),))
            info2 = c.fetchall()
            c.execute('SELECT * FROM Job WHERE Code = ?',(entry.get(),))
            info3 = c.fetchall()
            if len(info) == 0 & len(info2) == 0 & len(info3) == 0:
                messagebox.showinfo(title = "Caution", message = "No such job exists")
            else:
                ROW = info
                ROW.extend(info2)
                ROW.extend(info3)
                controller.dynamic_page(DisplaySpecific, parent, ROW)
                controller.show_frame(DisplaySpecific)


        query = tk.Label(self, text="- ENTER ROLE / EMPLOYER / CODE: ", font = LARGE_FONT)
        option1 = tk.Label(self, text="ID", font = LARGE_FONT)
        option2 = tk.Label(self, text="CODE", font = LARGE_FONT)
        option3 = tk.Label(self, text="ROLE", font = LARGE_FONT)
        option4 = tk.Label(self, text="EMPLOYER", font = LARGE_FONT)

        query.grid(row=1,column=1,columnspan = 2,padx = 20, pady=20)
        option1.grid(row=2,column=0,padx = 20, pady=20)
        option2.grid(row=2,column=1,padx = 20, pady=20)
        option3.grid(row=2,column=2,padx = 20, pady=20)
        option4.grid(row=2,column=3,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=1,column=3,padx = 20, pady=20)
  
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(ApplicantPage))
        button1.grid(row=0, columnspan = 2, padx = 20, pady=20 )
        button2 = ttk.Button(self, text="Fetch",
                            command= lambda: wrapper(entry1))
        button2.grid(row=1, column = 4, padx = 20, pady=20 )



class DisplaySpecific(tk.Frame):

    def __init__(self, parent, controller, ROW):
        tk.Frame.__init__(self,parent)

        option1 = tk.Label(self, text="ID", font = LARGE_FONT)
        option2 = tk.Label(self, text="CODE", font = LARGE_FONT)
        option3 = tk.Label(self, text="ROLE", font = LARGE_FONT)
        option4 = tk.Label(self, text="EMPLOYER", font = LARGE_FONT)

        option1.grid(row=1,column=0,padx = 20, pady=20)
        option2.grid(row=1,column=1,padx = 20, pady=20)
        option3.grid(row=1,column=2,padx = 20, pady=20)
        option4.grid(row=1,column=3,padx = 20, pady=20)

        index=2
        
        for row in ROW:
            tk.Label(self, text=row[0], font = LARGE_FONT).grid(row=index, column=0,padx = 20, pady=20)
            tk.Label(self, text=row[1], font = LARGE_FONT).grid(row=index, column=1,padx = 20, pady=20)
            tk.Label(self, text=row[2], font = LARGE_FONT).grid(row=index, column=2,padx = 20, pady=20)
            tk.Label(self, text=row[3], font = LARGE_FONT).grid(row=index, column=3,padx = 20, pady=20)
            index+=1
        
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(ApplicantPage))
        button1.grid(row=0,column = 1,columnspan = 2, padx = 20, pady=20 )
        


class ViewStatusPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(entry1, entry2):
            c.execute('SELECT * FROM Status WHERE Name = ? AND Code = ?',(entry1.get(),entry2.get(),))
            info = c.fetchall()
            if len(info) == 0:
                messagebox.showinfo(title = "Caution", message = "No such application was submitted")
            else:
                ROW = info[0]
                controller.dynamic_page(DisplayStatus, parent, ROW)
                controller.show_frame(DisplayStatus)


        query1 = tk.Label(self, text="- ENTER YOUR NAME: ", font = LARGE_FONT)
        query2 = tk.Label(self, text="- ENTER JOB CODE: ", font = LARGE_FONT)

        query1.grid(row=1,column=1,padx = 20, pady=20)
        query2.grid(row=2,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=1,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=2,column=2,padx = 20, pady=20)
  
  
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(ApplicantPage))
        button1.grid(row=0, columnspan = 2, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Fetch",
                            command= lambda: wrapper(entry1,entry2))
        button1.grid(row=3, columnspan = 2, padx = 20, pady=20 )



class DisplayStatus(tk.Frame):

    row = None
    
    def __init__(self, parent, controller, ROW):
        tk.Frame.__init__(self,parent)
        row = ROW
       
        option2 = tk.Label(self, text="NAME :", font = LARGE_FONT)
        option3 = tk.Label(self, text="JOB CODE :", font = LARGE_FONT)
        option4 = tk.Label(self, text="STATUS :", font = LARGE_FONT)
        
        option2.grid(row=1,column=1,padx = 20, pady=20)
        option3.grid(row=2,column=1,padx = 20, pady=20)
        option4.grid(row=3,column=1,padx = 20, pady=20)

        tk.Label(self, text=row[1], font = LARGE_FONT).grid(row=1, column=2,padx = 20, pady=20)
        tk.Label(self, text=row[2], font = LARGE_FONT).grid(row=2, column=2,padx = 20, pady=20)
        tk.Label(self, text=row[3], font = LARGE_FONT).grid(row=3, column=2,padx = 20, pady=20)
               
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(ApplicantPage))
        button1.grid(row=0, columnspan = 2, padx = 20, pady=20 )
        



        
class ViewAllJobPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        option1 = tk.Label(self, text="ID", font = LARGE_FONT)
        option2 = tk.Label(self, text="CODE", font = LARGE_FONT)
        option3 = tk.Label(self, text="ROLE", font = LARGE_FONT)
        option4 = tk.Label(self, text="EMPLOYER", font = LARGE_FONT)

        option1.grid(row=1,column=0,padx = 20, pady=20)
        option2.grid(row=1,column=1,padx = 20, pady=20)
        option3.grid(row=1,column=2,padx = 20, pady=20)
        option4.grid(row=1,column=3,padx = 20, pady=20)


        with conn:
            c = conn.cursor()
            c.execute('SELECT * FROM Job')
            index=2
            for row in c.fetchall():
                tk.Label(self, text=row[0], font = LARGE_FONT).grid(row=index, column=0,padx = 20, pady=20)
                tk.Label(self, text=row[1], font = LARGE_FONT).grid(row=index, column=1,padx = 20, pady=20)
                tk.Label(self, text=row[2], font = LARGE_FONT).grid(row=index, column=2,padx = 20, pady=20)
                tk.Label(self, text=row[3], font = LARGE_FONT).grid(row=index, column=3,padx = 20, pady=20)
                index+=1
        
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(ApplicantPage))
        button1.grid(row=0,column = 1,columnspan = 2, padx = 20, pady=20 )




class EmployerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="EMPLOYER PORTAL", font = HEADING_FONT)
        option1 = tk.Label(self, text="- REGISTER NEW EMPLOYER", font = LARGE_FONT)
        option2 = tk.Label(self, text="- POST A JOB", font = LARGE_FONT)
        option3 = tk.Label(self, text="- VIEW APPLICANTS", font = LARGE_FONT)
        option4 = tk.Label(self, text="- CONTACT AN APPLICANT", font = LARGE_FONT)
        
        label.grid(row=1, column=1,columnspan=2, padx = 20, pady=20)
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)
        option4.grid(row=5,column=1,padx = 20, pady=20)
                
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(MainPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button2 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(RegisterPage))
        button2.grid(row=2, column = 2, sticky = "es",padx = 20, pady=20 )
        button3 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(PostJobPage))
        button3.grid(row=3, column = 2, sticky = "es",padx = 20, pady=20 )
        button4 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ViewApplicantPage))
        button4.grid(row=4, column = 2, sticky = "es",padx = 20, pady=20 )
        button5 = ttk.Button(self, text="...",
                            command= lambda: controller.show_frame(ContactApplicantPage))
        button5.grid(row=5, column = 2, sticky = "es",padx = 20, pady=20 )


class ViewApplicantPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(entry):
            c.execute('SELECT * FROM Employer WHERE Name = ?',(entry.get(),))
            info = c.fetchall()
            if len(info) == 0:
                messagebox.showinfo(title = "Caution", message = "No such Employer exists")
            else:
                controller.dynamic_page(ViewApplicant, parent, entry.get())
                controller.show_frame(ViewApplicant)


        query = tk.Label(self, text="- ENTER EMPLOYER NAME: ", font = LARGE_FONT)
        option1 = tk.Label(self, text="ID", font = LARGE_FONT)
        option2 = tk.Label(self, text="NAME", font = LARGE_FONT)
        option3 = tk.Label(self, text="AGE", font = LARGE_FONT)
        option4 = tk.Label(self, text="CONTACT", font = LARGE_FONT)
        option5 = tk.Label(self, text="CODE", font = LARGE_FONT)


        query.grid(row=1,column=1,columnspan = 2,padx = 20, pady=20)
        option1.grid(row=2,column=0,padx = 20, pady=20)
        option2.grid(row=2,column=1,padx = 20, pady=20)
        option3.grid(row=2,column=2,padx = 20, pady=20)
        option4.grid(row=2,column=3,padx = 20, pady=20)
        option5.grid(row=2,column=4,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=1,column=3,padx = 20, pady=20)
  
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(EmployerPage))
        button1.grid(row=0, columnspan = 2, padx = 20, pady=20 )
        button2 = ttk.Button(self, text="Fetch",
                            command= lambda: wrapper(entry1))
        button2.grid(row=1, column = 4, padx = 20, pady=20 )


class ViewApplicant(tk.Frame):

    def __init__(self, parent, controller, employer):
        tk.Frame.__init__(self,parent)

        option1 = tk.Label(self, text="ID", font = LARGE_FONT)
        option2 = tk.Label(self, text="NAME", font = LARGE_FONT)
        option3 = tk.Label(self, text="AGE ", font = LARGE_FONT)
        option4 = tk.Label(self, text="CONTACT ", font = LARGE_FONT)
        option5 = tk.Label(self, text="CODE ", font = LARGE_FONT)

        option1.grid(row=1,column=0,padx = 20, pady=20)
        option2.grid(row=1,column=1,padx = 20, pady=20)
        option3.grid(row=1,column=2,padx = 20, pady=20)
        option4.grid(row=1,column=3,padx = 20, pady=20)
        option5.grid(row=1,column=4,padx = 20, pady=20)


        c.execute('SELECT Applicant.Id, Applicant.Name, Applicant.Age, Applicant.Contact, Applicant.Code FROM Applicant INNER JOIN Job ON Applicant.Code = Job.Code WHERE Job.Employer = ?',(employer,))
        index=2
        for row in c.fetchall():
            tk.Label(self, text=row[0], font = LARGE_FONT).grid(row=index, column=0,padx = 20, pady=20)
            tk.Label(self, text=row[1], font = LARGE_FONT).grid(row=index, column=1,padx = 20, pady=20)
            tk.Label(self, text=row[2], font = LARGE_FONT).grid(row=index, column=2,padx = 20, pady=20)
            tk.Label(self, text=row[3], font = LARGE_FONT).grid(row=index, column=3,padx = 20, pady=20)
            tk.Label(self, text=row[4], font = LARGE_FONT).grid(row=index, column=4,padx = 20, pady=20)
            index+=1
        
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(EmployerPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )


class RegisterPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
                
        option1 = tk.Label(self, text="- NAME ", font = LARGE_FONT)
        option2 = tk.Label(self, text="- GST", font = LARGE_FONT)
        option3 = tk.Label(self, text="- ABOUT", font = LARGE_FONT)
        
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=2,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=3,column=2,padx = 20, pady=20)
        entry3 = tk.Entry(self)
        entry3.grid(row=4,column=2,padx = 20, pady=20)
    
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(EmployerPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Store",
                            command= lambda: insert_employer(entry1.get(), entry2.get(), entry3.get(),))
        button1.grid(row=6, columnspan = 3, padx = 20, pady=20 )        



class PostJobPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
                
        option1 = tk.Label(self, text="- CODE ", font = LARGE_FONT)
        option2 = tk.Label(self, text="- ROLE", font = LARGE_FONT)
        option3 = tk.Label(self, text="- EMPLOYER", font = LARGE_FONT)
        
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=2,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=3,column=2,padx = 20, pady=20)
        entry3 = tk.Entry(self)
        entry3.grid(row=4,column=2,padx = 20, pady=20)
    
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(EmployerPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Store",
                            command= lambda: insert_job(entry1.get(), entry2.get(), entry3.get(),))
        button1.grid(row=6, columnspan = 3, padx = 20, pady=20 )        

class ContactApplicantPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def wrapper(name, code, message):
            c.execute('SELECT * FROM Status WHERE Name = ? AND Code = ?',(name.get(), code.get(),))
            info = c.fetchall()
            if len(info) == 0:
                messagebox.showinfo(title = "Caution", message = "No such Application Exists")
            else:
                update_status( name.get(), code.get(), message.get())
                messagebox.showinfo(title = "Success", message = "Message Sent Successfully")
                controller.show_frame(EmployerPage)

                
        option1 = tk.Label(self, text="- NAME ", font = LARGE_FONT)
        option2 = tk.Label(self, text="- CODE", font = LARGE_FONT)
        option3 = tk.Label(self, text="- MESSAGE", font = LARGE_FONT)
        
        option1.grid(row=2,column=1,padx = 20, pady=20)
        option2.grid(row=3,column=1,padx = 20, pady=20)
        option3.grid(row=4,column=1,padx = 20, pady=20)

        entry1 = tk.Entry(self)
        entry1.grid(row=2,column=2,padx = 20, pady=20)
        entry2 = tk.Entry(self)
        entry2.grid(row=3,column=2,padx = 20, pady=20)
        entry3 = tk.Entry(self)
        entry3.grid(row=4,column=2,padx = 20, pady=20)
    
        button1 = ttk.Button(self, text="Back",
                            command= lambda: controller.show_frame(EmployerPage))
        button1.grid(row=0, columnspan = 3, padx = 20, pady=20 )
        button1 = ttk.Button(self, text="Store",
                            command= lambda: wrapper(entry1, entry2, entry3))
        button1.grid(row=6, columnspan = 3, padx = 20, pady=20 )


        
create_employer_table()
create_status_table()
create_job_table()
create_applicant_table()
app = JobPortal()
app.mainloop()
