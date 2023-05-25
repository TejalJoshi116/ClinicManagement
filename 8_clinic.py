# Mini Project
import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3
from datetime import date
from reportlab.pdfgen import canvas
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


def center_window(window, width, height):
    # Retrieve the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window position to center
    window.geometry(f"{width}x{height}+{x}+{y}")

class Database:
    def __init__(self):
        self.dbConnection = sqlite3.connect("clinicdb.db")
        self.dbCursor = self.dbConnection.cursor()
        self.dbCursor.execute(
            """CREATE TABLE IF NOT EXISTS patient_table (
                id PRIMARYKEY text, firstname text, lastname text, dateOfBirth text, monthOfBirth text, 
                yearOfBirth text, gender text, address text, contactNumber text, bloodType text, 
                 symptom text, rubric text, medicine text, notes text, amount int)""")

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def Insert(self, id, firstname, lastname, dateOfBirth, monthOfBirth, yearOfBirth, gender, address, contactNumber, bloodType, symptom, rubric, medicine, notes, amount):
        self.dbCursor.execute("INSERT INTO patient_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        id, firstname, lastname, dateOfBirth, monthOfBirth, yearOfBirth, gender, address, contactNumber, bloodType,  symptom, rubric, medicine, notes, amount))
        self.dbConnection.commit()

    def Update(self, firstname, lastname, dateOfBirth, monthOfBirth, yearOfBirth, gender, address, contactNumber, bloodType, id, symptom, rubric, medicine, notes, amount):
        self.dbCursor.execute(
            "UPDATE patient_table SET firstname = ?, lastname = ?, dateOfBirth = ?, monthOfBirth = ?, yearOfBirth = ?, gender = ?, address = ?, contactNumber = ?, bloodType = ?, symptom = ?, rubric = ?, medicine = ?, notes = ?, amount = ? WHERE id = ?",
            (firstname, lastname, dateOfBirth, monthOfBirth, yearOfBirth, gender, address, contactNumber, bloodType, symptom, rubric, medicine, notes, amount, id))
        self.dbConnection.commit()

    def SearchByName(self, name):
        self.dbCursor.execute("SELECT * FROM patient_table WHERE firstname = ?", (name,))
        searchResults = self.dbCursor.fetchall()
        return searchResults

    def UpdateByName(self, firstname, lastname, dateOfBirth, monthOfBirth, yearOfBirth, gender, address, contactNumber, bloodType, name, symptom, rubric, medicine, notes, amount):
        self.dbCursor.execute(
            "UPDATE patient_table SET firstname = ?, lastname = ?, dateOfBirth = ?, monthOfBirth = ?, yearOfBirth = ?, gender = ?, address = ?, contactNumber = ?, bloodType = ?, symptom = ?, rubric = ?, medicine = ?, notes = ?, amount = ? WHERE firstname = ?",
            (firstname, lastname, dateOfBirth, monthOfBirth, yearOfBirth, gender, address, contactNumber, bloodType,
            symptom, rubric, medicine, notes, amount, name))
        self.dbConnection.commit()  

    def SearchByName(self, firstname, lastname):
        wildcard_firstname = f"%{firstname}%"
        wildcard_lastname = f"%{lastname}%"
        self.dbCursor.execute("SELECT * FROM patient_table WHERE firstname LIKE ? AND lastname LIKE ?", (wildcard_firstname, wildcard_lastname))
        searchResults = self.dbCursor.fetchall()
        return searchResults

    def DeleteByName(self, firstname, lastname):
        wildcard_firstname = f"%{firstname}%"
        wildcard_lastname = f"%{lastname}%"
        self.dbCursor.execute("DELETE FROM patient_table WHERE firstname LIKE ? AND lastname LIKE ?", (wildcard_firstname, wildcard_lastname))
        tkinter.messagebox.showinfo("Deleted data", "Successfully Deleted the Patient data in the database")
        self.dbConnection.commit()
  

    def Search(self, id):
        self.dbCursor.execute("SELECT * FROM patient_table WHERE id = ?", (id,))
        searchResults = self.dbCursor.fetchall()
        return searchResults

    def Delete(self, id):
        self.dbCursor.execute("DELETE FROM patient_table WHERE id = ?", (id,))
        tkinter.messagebox.showinfo("Deleted data", "Successfully Deleted the Patient data in the database")
        self.dbConnection.commit()

    def Display(self):
        self.dbCursor.execute("SELECT * FROM patient_table")
        records = self.dbCursor.fetchall()
        return records


class Values:
    def Validate(self, firstname, lastname, contactNumber):
        if not (firstname.isalpha()):
            return "firstname"
        elif not (lastname.isalpha()):
            return "lastname"
        elif not (contactNumber.isdigit() and (len(contactNumber) == 10)):
            return "contactNumber"
        else:
            return "SUCCESS"


class InsertWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("Insert Patient Data")
        self.window.geometry("800x600")
        bg_color = "Blue"
        fg_color = "white"

        # Frame setup
        self.frame = tkinter.Frame(self.window)
        self.frame.pack()

        self.userdata_frame_1 = tkinter.LabelFrame(self.frame)
        self.userdata_frame_1.grid(row=0, column=0, padx=20, pady=10)

        self.userdata_frame_2 = tkinter.LabelFrame(self.frame)
        self.userdata_frame_2.grid(row=1, column=0, padx=20, pady=10)

        self.doctor_frame = tkinter.LabelFrame(self.frame)
        self.doctor_frame.grid(row=2, column=0, padx=20, pady=10)


        # Variables
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.contactNumber = tkinter.StringVar()
        self.symptom = tkinter.StringVar()
        self.rubric = tkinter.StringVar()
        self.notes = tkinter.StringVar()
        self.medicine = tkinter.StringVar()
        self.amount = tkinter.StringVar()

        self.genderType = ["Male", "Female", "Transgender", "Other"]
        self.dateType = list(range(1, 32))
        self.monthType = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                          "October", "November", "December"]
        self.yearType = list(range(1900, 2023))
        self.bloodListType = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        # userdata_frame_1
        tkinter.Label(self.userdata_frame_1, text="Patient First Name", font=("times new roman", 10, "bold")).grid(row=0, column=0)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Patient Last Name").grid( row=0, column=1)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Patient Gender").grid(row=0, column=2)
        self.firstnameEntry = tkinter.Entry(self.userdata_frame_1, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.userdata_frame_1, textvariable=self.lastname)
        self.firstnameEntry.grid(column=0, row=1)
        self.lastnameEntry.grid(column=1, row=1)

        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Date of Birth").grid(row=2,column=0)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Month of Birth").grid(row=2,column=1)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Year of Birth").grid(row=2, column=2)
        

        # Combobox aka dropdown menu widgets
        self.dateOfBirthBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.dateType)
        self.monthOfBirthBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.monthType, width=25)
        self.yearOfBirthBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.yearType, width=25)
        self.genderBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.genderType, width=25)
        

        self.dateOfBirthBox.grid(column=0, row=3)
        self.monthOfBirthBox.grid(column=1, row=3)
        self.yearOfBirthBox.grid(column=2, row=3)
        self.genderBox.grid(column=2, row=1)
        

        for widget in self.userdata_frame_1.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # userdata_frame_2
        tkinter.Label(self.userdata_frame_2, font=("times new roman", 10, "bold"), text="Patient Blood Type").grid(row=0, column=0)
        tkinter.Label(self.userdata_frame_2, font=("times new roman", 10, "bold"), text="Contact Number").grid(column=2, row=0)
        tkinter.Label(self.userdata_frame_2, font=("times new roman", 10, "bold"), text="Patient Address").grid(column=0, row=1, sticky="E")

        self.bloodListBox = tkinter.ttk.Combobox(self.userdata_frame_2, values=self.bloodListType)
        self.bloodListBox.grid(column=1, row=0, sticky="W")

        self.addressEntry = tkinter.Entry(self.userdata_frame_2, textvariable=self.address, width=65)
        self.contactNumberEntry = tkinter.Entry(self.userdata_frame_2, textvariable=self.contactNumber)
        
        self.contactNumberEntry.grid(column=3, row=0)
        self.addressEntry.grid(column=1, row=1, sticky="W", columnspan=3)
        

        for widget in self.userdata_frame_2.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        

        self.symptomEntry = tkinter.Entry(self.doctor_frame, textvariable=self.symptom, width=50)
        self.rubricEntry = tkinter.Entry(self.doctor_frame, textvariable=self.rubric, width=50)
        self.medicineEntry = tkinter.Entry(self.doctor_frame, textvariable=self.medicine, width=50)
        self.notesEntry = tkinter.Text(self.doctor_frame, height=3, width=50)

        self.amountEntry = tkinter.Entry(self.doctor_frame, textvariable=self.amount)

        self.symptomEntry.grid(column=1, row=0, sticky="W")
        self.rubricEntry.grid(column=1, row=1, sticky="W")
        self.medicineEntry.grid(column=1, row=2, sticky="W")
        self.notesEntry.grid(column=1, row=4, rowspan=3, sticky="W")
        self.amountEntry.grid(column=1, row=3, sticky="W")

        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Symptoms").grid(column=0, row=0, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Rubrics").grid(column=0, row=1, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Medicine").grid(column=0, row=2, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Amount paid").grid(column=0, row=3, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Doctors Notes :").grid(column=0, row=4, sticky="E")


        for widget in self.doctor_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Button widgets
        self.end_frame = tkinter.Frame(self.window)
        self.end_frame.pack()

        tkinter.Button(self.end_frame, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Insert", command=self.Insert).grid(pady=15, padx=5, column=1, row=0)
        tkinter.Button(self.end_frame, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=0)
        tkinter.Button(self.end_frame, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3, row=0)

        self.window.mainloop()

    def Insert(self):
        self.values = Values()
        self.database = Database()
        # Generate a unique ID for the patient
        generated_id = self.generate_unique_id()
        
        self.test = self.values.Validate(self.firstnameEntry.get(), self.lastnameEntry.get(),self.contactNumberEntry.get())

        if self.test == "SUCCESS":
            self.database.Insert(
                                generated_id, self.firstnameEntry.get(), self.lastnameEntry.get(),
                                self.dateOfBirthBox.get(), self.monthOfBirthBox.get(), self.yearOfBirthBox.get(),
                                self.genderBox.get(), self.addressEntry.get(), self.contactNumberEntry.get(),
                                self.bloodListBox.get(), self.symptomEntry.get(), self.rubricEntry.get(),
                                self.medicineEntry.get(), self.notesEntry.get("1.0", tkinter.END), self.amountEntry.get()
    )
            tkinter.messagebox.showinfo("Inserted data", "Successfully inserted the above data in the database")
        else:
            self.valueErrorMessage = "Invalid input in field " + self.test
            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

    def generate_unique_id(self):
        
        connection = sqlite3.connect("clinicdb.db")
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(id) FROM patient_table")
        result = cursor.fetchone()[0]
        if result is not None:
            return int(result) + 1
        else:
            return 1
    def Reset(self):
        self.idEntry.delete(0, tkinter.END)
        self.firstnameEntry.delete(0, tkinter.END)
        self.lastnameEntry.delete(0, tkinter.END)
        self.dateOfBirthBox.set("")
        self.monthOfBirthBox.set("")
        self.yearOfBirthBox.set("")
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.contactNumberEntry.delete(0, tkinter.END)
        self.bloodListBox.set("")  
        self.symptomEntry.delete(0, tkinter.END)
        self.rubricEntry.delete(0, tkinter.END)
        self.medicineEntry.delete(0, tkinter.END)
        self.notesEntry.delete(0, tkinter.END)
        self.amountEntry.delete(0, tkinter.END)
        

class UpdateClass():
    def __init__(self,data):
        self.window = tkinter.Tk()
        self.window.wm_title("Update Patient Data")
        self.window.geometry("800x600")
        bg_color = "Blue"
        fg_color = "white"

        # Frame setup
        self.frame = tkinter.Frame(self.window)
        self.frame.pack()

        self.userdata_frame_1 = tkinter.LabelFrame(self.frame)
        self.userdata_frame_1.grid(row=0, column=0, padx=20, pady=10)

        self.userdata_frame_2 = tkinter.LabelFrame(self.frame)
        self.userdata_frame_2.grid(row=1, column=0, padx=20, pady=10)

        self.doctor_frame = tkinter.LabelFrame(self.frame)
        self.doctor_frame.grid(row=2, column=0, padx=20, pady=10)

        # Variables
        self.id = tkinter.StringVar()
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.contactNumber = tkinter.StringVar()
        self.symptom = tkinter.StringVar()
        self.rubric = tkinter.StringVar()
        self.notes = tkinter.StringVar()
        self.medicine = tkinter.StringVar()
        self.amount = tkinter.StringVar()

        self.genderType = ["Male", "Female", "Transgender", "Other"]
        self.dateType = list(range(1, 32))
        self.monthType = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                          "October", "November", "December"]
        self.yearType = list(range(1900, 2023))
        self.bloodListType = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        # userdata_frame_1
        tkinter.Label(self.userdata_frame_1, text="Patient First Name", font=("times new roman", 10, "bold")).grid(row=0, column=0)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Patient Last Name").grid( row=0, column=1)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Patient Gender").grid(row=0, column=2)
        self.firstnameEntry = tkinter.Entry(self.userdata_frame_1, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.userdata_frame_1, textvariable=self.lastname)
        self.firstnameEntry.grid(column=0, row=1)
        self.lastnameEntry.grid(column=1, row=1)

        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Date of Birth").grid(row=2,column=0)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Month of Birth").grid(row=2,column=1)
        tkinter.Label(self.userdata_frame_1, font=("times new roman", 10, "bold"), text="Year of Birth").grid(row=2, column=2)
        

        # Combobox aka dropdown menu widgets
        self.dateOfBirthBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.dateType)
        self.monthOfBirthBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.monthType, width=25)
        self.yearOfBirthBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.yearType, width=25)
        self.genderBox = tkinter.ttk.Combobox(self.userdata_frame_1, values=self.genderType, width=25)
        

        self.dateOfBirthBox.grid(column=0, row=3)
        self.monthOfBirthBox.grid(column=1, row=3)
        self.yearOfBirthBox.grid(column=2, row=3)
        self.genderBox.grid(column=2, row=1)
        

        for widget in self.userdata_frame_1.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # userdata_frame_2
        tkinter.Label(self.userdata_frame_2, font=("times new roman", 10, "bold"), text="Patient Blood Type").grid(row=0, column=0)
        tkinter.Label(self.userdata_frame_2, font=("times new roman", 10, "bold"), text="Contact Number").grid(column=2, row=0)
        tkinter.Label(self.userdata_frame_2, font=("times new roman", 10, "bold"), text="Patient Address").grid(column=0, row=1, sticky="E")

        self.bloodListBox = tkinter.ttk.Combobox(self.userdata_frame_2, values=self.bloodListType)
        self.bloodListBox.grid(column=1, row=0, sticky="W")

        self.addressEntry = tkinter.Entry(self.userdata_frame_2, textvariable=self.address, width=65)
        self.contactNumberEntry = tkinter.Entry(self.userdata_frame_2, textvariable=self.contactNumber)
        
        self.contactNumberEntry.grid(column=3, row=0)
        self.addressEntry.grid(column=1, row=1, sticky="W", columnspan=3)
        

        for widget in self.userdata_frame_2.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        

        self.symptomEntry = tkinter.Entry(self.doctor_frame, textvariable=self.symptom, width=50)
        self.rubricEntry = tkinter.Entry(self.doctor_frame, textvariable=self.rubric, width=50)
        self.medicineEntry = tkinter.Entry(self.doctor_frame, textvariable=self.medicine, width=50)
        self.notesEntry = tkinter.Text(self.doctor_frame, height=3, width=50)

        self.amountEntry = tkinter.Entry(self.doctor_frame, textvariable=self.amount)

        self.symptomEntry.grid(column=1, row=0, sticky="W")
        self.rubricEntry.grid(column=1, row=1, sticky="W")
        self.medicineEntry.grid(column=1, row=2, sticky="W")
        self.notesEntry.grid(column=1, row=4, rowspan=3, sticky="W")
        self.amountEntry.grid(column=1, row=3, sticky="W")

        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Symptoms").grid(column=0, row=0, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Rubrics").grid(column=0, row=1, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Medicine").grid(column=0, row=2, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Amount paid").grid(column=0, row=3, sticky="E")
        tkinter.Label(self.doctor_frame, font=("times new roman", 10, "bold"), text="Doctors Notes :").grid(column=0, row=4, sticky="E")


        for widget in self.doctor_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)
        
        self.firstname.set(data[0])
        self.lastname.set(data[1])
        self.genderBox.set(data[2])
        dob = data[3].split("/")
        self.dateOfBirthBox.set(dob[0])
        self.monthOfBirthBox.set(dob[1])
        self.yearOfBirthBox.set(dob[2])
        self.bloodListBox.set(data[4])
        self.address.set(data[5])
        self.contactNumber.set(data[6])
        self.symptom.set(data[7])
        self.rubric.set(data[8])
        self.medicine.set(data[9])
        self.notes.set(data[10])
        self.amount.set(data[11])

        # Button widgets
        self.end_frame = tkinter.Frame(self.window)
        self.end_frame.pack()


        # Buttons
        tkinter.Button(self.end_frame, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Update", command= self.updateData).grid(pady=15, padx=5, column=1, row=0)
        tkinter.Button(self.end_frame, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=0)
        tkinter.Button(self.end_frame, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3, row=0)

        
        self.root.mainloop()

    def Reset(self):
        self.idEntry.delete(0, tkinter.END)
        self.firstnameEntry.delete(0, tkinter.END)
        self.lastnameEntry.delete(0, tkinter.END)
        self.dateOfBirthBox.set("")
        self.monthOfBirthBox.set("")
        self.yearOfBirthBox.set("")
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.contactNumberEntry.delete(0, tkinter.END)
        self.bloodListBox.set("")
        
        self.symptomEntry.delete(0, tkinter.END)
        self.rubricEntry.delete(0, tkinter.END)
        self.medicineEntry.delete(0, tkinter.END)
        self.notesEntry.delete(0, tkinter.END)
        self.amountEntry.delete(0, tkinter.END)

    def updateData(self):
        firstname = self.firstname.get()
        lastname = self.lastname.get()
        gender = self.genderCombo.get()
        dob = f"{self.dateCombo.get()}/{self.monthCombo.get()}/{self.yearCombo.get()}"
        blood_group = self.bloodCombo.get()
        address = self.address.get()
        contact_number = self.contactNumber.get()
        symptoms = self.symptom.get()
        rubric = self.rubric.get()
        notes = self.notes.get()
        medicine = self.medicine.get()
        amount = self.amount.get()

        
        # Display success message
        tkinter.messagebox.showinfo("Success", "Data updated successfully.")

        self.destroyWindow()


class SearchDeleteWindow:
    def __init__(self, task):
        self.window = tkinter.Toplevel()
        self.window.wm_title(task + " data")

        # Initializing all the variables
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.heading = "Please enter the patient name to " + task

        tkinter.Label(self.window, text=self.heading, width=50).grid(pady=20, row=1)
        tkinter.Label(self.window, text="First Name", width=10).grid(pady=5, row=2)
        tkinter.Label(self.window, text="Last Name", width=10).grid(pady=5, row=3)

        self.firstnameEntry = tkinter.Entry(self.window, width=20, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.window, width=20, textvariable=self.lastname)

        self.firstnameEntry.grid(pady=5, row=2, column=1)
        self.lastnameEntry.grid(pady=5, row=3, column=1)

        # Buttons
        if task == "Search":
            tkinter.Button(self.window, width=20, text=task, command=self.Search).grid(pady=15, padx=5, column=1, row=14)
        elif task == "Delete":
            tkinter.Button(self.window, width=20, text=task, command=self.Delete).grid(pady=15, padx=5, column=1, row=14)
        elif task == "Update":
            tkinter.Button(self.window, width=20, text=task, command=self.Update).grid(pady=15, padx=5, column=1, row=14)

    def Search(self):
        self.database = Database()
        self.data = self.database.SearchByName(self.firstnameEntry.get(), self.lastnameEntry.get())
        self.databaseView = DatabaseView(self.data)

    def Delete(self):
        self.database = Database()
        self.database.DeleteByName(self.firstnameEntry.get(), self.lastnameEntry.get())

    def Update(self):
        self.database = Database()
        self.data = self.database.SearchByName(self.firstnameEntry.get(), self.lastnameEntry.get())
        if self.data:
            self.updateDataView = UpdateDataView(self.data)
        else:
            tkinter.messagebox.showinfo("Entry not found", "No matching entry found in the database.")


class DatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.geometry("1200x600")
        self.databaseViewWindow.wm_title("Database View")

        # Label widget
        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).pack(pady=5)

        # Create a frame for the treeview
        self.tree_frame = tkinter.Frame(self.databaseViewWindow)
        self.tree_frame.pack(pady=20)

        # Scrollbars
        self.tree_scroll_y = tkinter.ttk.Scrollbar(self.tree_frame)
        self.tree_scroll_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree_scroll_x = tkinter.ttk.Scrollbar(self.databaseViewWindow, orient=tkinter.HORIZONTAL)
        self.tree_scroll_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        # Create the treeview
        self.databaseView = tkinter.ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )
        self.databaseView.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = (
            "id", "firstname", "lastname", "dateOfBirth", "monthOfBirth",
            "yearOfBirth", "gender", "address", "contactNumber", "bloodType",
            "symptom", "rubric", "medicine", "notes", "amount"
        )
        self.tree_scroll_y.config(command=self.databaseView.yview)
        self.tree_scroll_x.config(command=self.databaseView.xview)

        # Treeview column headings
        self.databaseView.heading("id", text="ID", command=lambda: self.sort_column("id", False))
        self.databaseView.heading("firstname", text="First Name", command=lambda: self.sort_column("firstname", True))
        self.databaseView.heading("lastname", text="Last Name", command=lambda: self.sort_column("lastname", True))
        self.databaseView.heading("dateOfBirth", text="BirthDate", command=lambda: self.sort_column("dateOfBirth", False))
        self.databaseView.heading("monthOfBirth", text="Month", command=lambda: self.sort_column("monthOfBirth", False))
        self.databaseView.heading("yearOfBirth", text="Year", command=lambda: self.sort_column("yearOfBirth", False))
        self.databaseView.heading("gender", text="Gender", command=lambda: self.sort_column("gender", True))
        self.databaseView.heading("address", text="Home Address", command=lambda: self.sort_column("address", True))
        self.databaseView.heading("contactNumber", text="Contact Number", command=lambda: self.sort_column("contactNumber", True))
        self.databaseView.heading("bloodType", text="Blood Type", command=lambda: self.sort_column("bloodType", True))
        self.databaseView.heading("symptom", text="Symptoms", command=lambda: self.sort_column("symptom", True))
        self.databaseView.heading("rubric", text="Rubrics", command=lambda: self.sort_column("rubric", True))
        self.databaseView.heading("medicine", text="Medicine", command=lambda: self.sort_column("medicine", True))
        self.databaseView.heading("notes", text="Notes", command=lambda: self.sort_column("notes", True))
        self.databaseView.heading("amount", text="Amount Paid", command=lambda: self.sort_column("amount", False))

        column_widths = {
            "id": 50,
            "firstname": 200,
            "lastname": 200,
            "dateOfBirth": 50,
            "monthOfBirth": 100,
            "yearOfBirth": 100,
            "gender": 100,
            "address": 200,
            "contactNumber": 150,
            "bloodType": 50,
            "symptom": 200,
            "rubric": 200,
            "medicine": 150,
            "notes": 200,
            "amount": 100
        }

        for column, width in column_widths.items():
            self.databaseView.column(column, width=width, minwidth=50)

        for record in data:
            self.databaseView.insert("", "end", values=record)


        # Bind the double-click event to handle row selection
        self.databaseView.bind("<Double-1>", self.on_row_selected)

        self.databaseViewWindow.mainloop()


    def sort_column(self, column, reverse):
        # Get the column data
        data = [(self.databaseView.set(child, column), child) for child in self.databaseView.get_children("")]

        # Sort the data
        data.sort(key=lambda x: x[0], reverse=reverse)

        # Rearrange the rows based on the sorted data
        for index, (value, child) in enumerate(data):
            self.databaseView.move(child, "", index)

        # Reverse the sorting order for the next click
        self.databaseView.heading(column, command=lambda: self.sort_column(column, not reverse))

    def generate_pdf(self, values):
        # Create the PDF document
        pdf = canvas.Canvas(r"C:\Users\joshi\Desktop\pdfs\patient_report.pdf")

        # Set the font and font size
        pdf.setFont("Helvetica", 12)

        # Set the y position for the first line
        y_position = 750

        # Write the data to the PDF
        pdf.drawString(50, y_position, f"ID: {str(values[0])}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Name: {values[1]} {values[2]}")
        y_position -= 20
        pdf.drawString(50, y_position, f"DOB: {values[3]}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Gender: {values[6]}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Symptoms: {values[10]}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Rubrics: {values[11]}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Medicine: {values[12]}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Notes: {values[13]}")

        # Save the PDF document
        pdf.save()

        # Provide feedback to the user
        tkinter.messagebox.showinfo("PDF Created", "The PDF report has been created successfully.")



    def on_row_selected(self, event):
        # Get the selected row
        selected_item = self.databaseView.selection()
        values = self.databaseView.item(selected_item)["values"]

        # Open a new window with the report for the selected patient
        report_window = tkinter.Toplevel(self.databaseViewWindow)
        report_window.title("Patient Report")
        
        report_window.geometry("500x600")

        # Display the report
        current_date = date.today().strftime("%B %d, %Y")

        # Heading and date
        heading_label = tkinter.Label(report_window, text="Patient Report", font=("Arial", 16, "bold"))
        heading_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")  # Centered at the top

        # Center the label horizontally by spanning across both columns
        report_window.grid_columnconfigure(0, weight=1)
        report_window.grid_columnconfigure(1, weight=1)

        date_label = tkinter.Label(report_window, text=current_date, font=("Arial", 10), anchor="e")
        date_label.grid(row=1, column=0, columnspan=2, padx=15, sticky="e")  # Centered to the right

        # Doctor's information
        doctor_name = "Dr. Deepa Joshi"
        credentials = "Homeopath"
        clinic_address = "123 Main Street, City"
        phone_number = "123-456-7890"

        doctor_label = tkinter.Label(report_window, text=f"Doctor: {doctor_name}", font=("Arial", 10, "bold"), anchor="e")
        doctor_label.grid(row=2, column=0,columnspan=2, padx=15, sticky="e")  # Right-aligned

        credentials_label = tkinter.Label(report_window, text=f"Credentials: {credentials}", font=("Arial", 10), anchor="e")
        credentials_label.grid(row=3, column=0, columnspan=2, padx=15, sticky="e")  # Right-aligned

        address_label = tkinter.Label(report_window, text=f"Clinic Address: {clinic_address}", font=("Arial", 10), anchor="e")
        address_label.grid(row=4, column=0, columnspan=2, padx=15,  sticky="e")  # Right-aligned

        phone_label = tkinter.Label(report_window, text=f"Phone Number: {phone_number}", font=("Arial", 10), anchor="e")
        phone_label.grid(row=5, column=0, columnspan=2, padx=15, sticky="e")  # Right-aligned

        # Patient data
        data_labels = ["ID:", "Name:", "DOB:", "Gender:", "Symptoms:", "Rubrics:", "Medicine:", "Notes:"]
        data_values = [values[0], f"{values[1]} {values[2]}", values[3], values[6], values[10], values[11], values[12], values[13]]

        report_row = 8

        report_window.grid_columnconfigure(0, minsize=50)
        report_window.grid_columnconfigure(1, minsize=300)

        for label, value in zip(data_labels, data_values):
            data_label = tkinter.Label(report_window, text=label, font=("Arial", 10, "bold"))
            data_label.grid(row=report_row, column=0, sticky="w", padx=10)  # Adjust the padx value to reduce the space

            data_value = tkinter.Label(report_window, text=value, font=("Arial", 10))
            data_value.grid(row=report_row, column=1, sticky="w", padx=(0, 10))  # Adjust the padx value to reduce the space

            report_row += 1

        # Signature space for the doctor
        signature_label = tkinter.Label(report_window, text="Doctor's Signature:", font=("Arial", 10, "bold"))
        signature_label.grid(row=17, column=0, columnspan=2, pady=10,padx=10, sticky="w")  # Left-aligned

        pdf_button = tkinter.Button(report_window, text="Download PDF", command=lambda: self.generate_pdf(values))
        pdf_button.grid(row=18, column=0, columnspan=2, pady=10)


class UpdateDataView:
    def __init__(self, data):
        self.updateDataViewWindow = tkinter.Tk()
        self.updateDataViewWindow.geometry("1200x600")
        self.updateDataViewWindow.wm_title("Database View")

        # Label widget
        tkinter.Label(self.updateDataViewWindow, text="Database View Window", width=25).pack(pady=5)

        # Create a frame for the treeview
        self.tree_frame = tkinter.Frame(self.updateDataViewWindow)
        self.tree_frame.pack(pady=20)

        # Scrollbars
        self.tree_scroll_y = tkinter.ttk.Scrollbar(self.tree_frame)
        self.tree_scroll_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree_scroll_x = tkinter.ttk.Scrollbar(self.updateDataViewWindow, orient=tkinter.HORIZONTAL)
        self.tree_scroll_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        # Create the treeview
        self.updateDataViewWindow = tkinter.ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )
        self.updateDataViewWindow.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.updateDataViewWindow["show"] = "headings"
        self.updateDataViewWindow["columns"] = (
            "id", "firstname", "lastname", "dateOfBirth", "monthOfBirth",
            "yearOfBirth", "gender", "address", "contactNumber", "bloodType",
            "symptom", "rubric", "medicine", "notes", "amount"
        )
        self.tree_scroll_y.config(command=self.updateDataViewWindow.yview)
        self.tree_scroll_x.config(command=self.updateDataViewWindow.xview)

        # Treeview column headings
        self.updateDataViewWindow.heading("id", text="ID", command=lambda: self.sort_column("id", False))
        self.updateDataViewWindow.heading("firstname", text="First Name", command=lambda: self.sort_column("firstname", True))
        self.updateDataViewWindow.heading("lastname", text="Last Name", command=lambda: self.sort_column("lastname", True))
        self.updateDataViewWindow.heading("dateOfBirth", text="BirthDate", command=lambda: self.sort_column("dateOfBirth", False))
        self.updateDataViewWindow.heading("monthOfBirth", text="Month", command=lambda: self.sort_column("monthOfBirth", False))
        self.updateDataViewWindow.heading("yearOfBirth", text="Year", command=lambda: self.sort_column("yearOfBirth", False))
        self.updateDataViewWindow.heading("gender", text="Gender", command=lambda: self.sort_column("gender", True))
        self.updateDataViewWindow.heading("address", text="Home Address", command=lambda: self.sort_column("address", True))
        self.updateDataViewWindow.heading("contactNumber", text="Contact Number", command=lambda: self.sort_column("contactNumber", True))
        self.updateDataViewWindow.heading("bloodType", text="Blood Type", command=lambda: self.sort_column("bloodType", True))
        self.updateDataViewWindow.heading("symptom", text="Symptoms", command=lambda: self.sort_column("symptom", True))
        self.updateDataViewWindow.heading("rubric", text="Rubrics", command=lambda: self.sort_column("rubric", True))
        self.updateDataViewWindow.heading("medicine", text="Medicine", command=lambda: self.sort_column("medicine", True))
        self.updateDataViewWindow.heading("notes", text="Notes", command=lambda: self.sort_column("notes", True))
        self.updateDataViewWindow.heading("amount", text="Amount Paid", command=lambda: self.sort_column("amount", False))

        column_widths = {
            "id": 50,
            "firstname": 200,
            "lastname": 200,
            "dateOfBirth": 50,
            "monthOfBirth": 100,
            "yearOfBirth": 100,
            "gender": 100,
            "address": 200,
            "contactNumber": 150,
            "bloodType": 50,
            "symptom": 200,
            "rubric": 200,
            "medicine": 150,
            "notes": 200,
            "amount": 100
        }

        for column, width in column_widths.items():
            self.updateDataViewWindow.column(column, width=width, minwidth=50)

        for record in data:
            self.updateDataViewWindow.insert("", "end", values=record)


        # Bind the double-click event to handle row selection
        self.updateDataViewWindow.bind("<Double-1>", self.on_row_selected)

        self.updateDataViewWindowWindow.mainloop()


    def sort_column(self, column, reverse):
        # Get the column data
        data = [(self.updateDataViewWindow.set(child, column), child) for child in self.updateDataViewWindow.get_children("")]

        # Sort the data
        data.sort(key=lambda x: x[0], reverse=reverse)

        # Rearrange the rows based on the sorted data
        for index, (value, child) in enumerate(data):
            self.updateDataViewWindow.move(child, "", index)

        # Reverse the sorting order for the next click
        self.updateDataViewWindow.heading(column, command=lambda: self.sort_column(column, not reverse))

    


    def on_row_selected(self, event):
        selected_item = self.updateDataView.focus()  # Get the selected item
        if selected_item:
            data = self.updateDataViewW.item(selected_item, "values")  # Get the data of the selected item
            self.updateWindow = UpdateClass(data) 
        



class HomePage:
    
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.title("Patient Management System")
        self.homePageWindow.geometry("800x600")
        self.homePageWindow.config(bg='#F8F8F8')
        font = ("Arial", 14)

        # Title
        tkinter.Label(self.homePageWindow, text="Patient Management System", font=("Arial", 30, "bold"), fg="#333", bg='#F8F8F8').pack(pady=50)

        # Buttons
        insert_button = tkinter.Button(self.homePageWindow, width=20, text="Add Patient", font=font, command=self.Insert, bg='#2196f3', fg='#fff', borderwidth=0)
        update_button = tkinter.Button(self.homePageWindow, width=20, text="Update Patient", font=font, command=self.Update, bg='#2196f3', fg='#fff', borderwidth=0)
        search_button = tkinter.Button(self.homePageWindow, width=20, text="Search Patients", font=font, command=self.Search, bg='#2196f3', fg='#fff', borderwidth=0)
        delete_button = tkinter.Button(self.homePageWindow, width=20, text="Delete Patient", font=font, command=self.Delete, bg='#2196f3', fg='#fff', borderwidth=0)
        display_button = tkinter.Button(self.homePageWindow, width=20, text="Display Patients", font=font, command=self.Display, bg='#2196f3', fg='#fff', borderwidth=0)
        exit_button = tkinter.Button(self.homePageWindow, width=20, text="Exit", font=font, command=self.homePageWindow.destroy, bg='#2196f3', fg='#fff', borderwidth=0)

        # Place buttons in a grid layout
        insert_button.pack(pady=10)
        update_button.pack(pady=10)
        search_button.pack(pady=10)
        delete_button.pack(pady=10)
        display_button.pack(pady=10)
        exit_button.pack(pady=10)

        self.homePageWindow.mainloop()

    def Insert(self):
        self.insertWindow = InsertWindow()

    def Update(self):
        self.updateWindow = SearchDeleteWindow("Update")

    # def updateName(self):
    #     if self.nameEntry.get():
    #         self.updateWindow = UpdateWindow(self.nameEntry.get())
    #         self.updateWindow.destroy(self)
    #     else:
    #         tkinter.messagebox.showwarning("Invalid Input", "Please enter a name.")
    

    def Search(self):
        self.searchWindow = SearchDeleteWindow("Search")

    def Delete(self):
        self.deleteWindow = SearchDeleteWindow("Delete")

    def Display(self):
        self.database = Database()
        self.data = self.database.Display()
        self.displayWindow = DatabaseView(self.data)    


HomePage = HomePage()




# class UpdateWindow:
#     def __init__(self, id):
#         self.window = tkinter.Tk()
#         self.window.geometry("800x600")
#         self.window.wm_title("Update data")
#         bg_color = "Blue"
#         fg_color = "white"

#         # Initializing all the variables
#         self.id = id

#         self.firstname = tkinter.StringVar()
#         self.lastname = tkinter.StringVar()
#         self.address = tkinter.StringVar()
#         self.contactNumber = tkinter.StringVar()
#         
        

#         self.genderType = ["Male", "Female", "Transgender", "Other"]
#         self.dateType = list(range(1, 32))
#         self.monthType = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
#                           "October", "November", "December"]
#         self.yearType = list(range(1900, 2020))
#         self.bloodListType = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

#         # Labels
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Patient Id", font=("times new roman", 10, "bold"),
#                       width=25).grid(pady=5, column=1, row=1)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Patient First Name",
#                       font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Patient Last Name", width=25).grid(pady=5, column=1, row=3)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"), text="Date of Birth",
#                       width=25).grid(pady=5, column=1, row=4)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Month of Birth", width=25).grid(pady=5, column=1, row=5)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"), text="Year of Birth",
#                       width=25).grid(pady=5, column=1, row=6)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Patient Gender", width=25).grid(pady=5, column=1, row=7)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Patient Address", width=25).grid(pady=5, column=1, row=8)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Patient Contact Number", width=25).grid(pady=5, column=1, row=9)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Patient Blood Type", width=25).grid(pady=5, column=1, row=11)
#         
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Symptoms", width=25).grid(pady=5, column=1, row=13)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Rubrics", width=25).grid(pady=5, column=1, row=14)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Medicine given", width=25).grid(pady=5, column=1, row=15)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Doctor notes", width=25).grid(pady=5, column=1, row=16)
#         tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                       text="Amount paid", width=25).grid(pady=5, column=1, row=17)

#         # Set previous values
#         self.database = Database()
#         self.searchResults = self.database.Search(id)

#         tkinter.Label(self.window, text=self.searchResults[0][1], width=25).grid(pady=5, column=2, row=2)
#         tkinter.Label(self.window, text=self.searchResults[0][2], width=25).grid(pady=5, column=2, row=3)
#         tkinter.Label(self.window, text=self.searchResults[0][3], width=25).grid(pady=5, column=2, row=4)
#         tkinter.Label(self.window, text=self.searchResults[0][4], width=25).grid(pady=5, column=2, row=5)
#         tkinter.Label(self.window, text=self.searchResults[0][5], width=25).grid(pady=5, column=2, row=6)
#         tkinter.Label(self.window, text=self.searchResults[0][6], width=25).grid(pady=5, column=2, row=7)
#         tkinter.Label(self.window, text=self.searchResults[0][7], width=25).grid(pady=5, column=2, row=8)
#         tkinter.Label(self.window, text=self.searchResults[0][8], width=25).grid(pady=5, column=2, row=9)
#         tkinter.Label(self.window, text=self.searchResults[0][9], width=25).grid(pady=5, column=2, row=10)
#         tkinter.Label(self.window, text=self.searchResults[0][10], width=25).grid(pady=5, column=2, row=11)
#         tkinter.Label(self.window, text=self.searchResults[0][11], width=25).grid(pady=5, column=2, row=12)
#         tkinter.Label(self.window, text=self.searchResults[0][12], width=25).grid(pady=5, column=2, row=13)
#         tkinter.Label(self.window, text=self.searchResults[0][13], width=25).grid(pady=5, column=2, row=14)
#         tkinter.Label(self.window, text=self.searchResults[0][14], width=25).grid(pady=5, column=2, row=15)
#         tkinter.Label(self.window, text=self.searchResults[0][15], width=25).grid(pady=5, column=2, row=16)
#         tkinter.Label(self.window, text=self.searchResults[0][16], width=25).grid(pady=5, column=2, row=17)
        

#         self.idEntry = tkinter.Entry(self.window, width=25, textvariable=self.id)
#         self.firstnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.firstname)
#         self.lastnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.lastname)
#         self.addressEntry = tkinter.Entry(self.window, width=25, textvariable=self.address)
#         self.contactNumberEntry = tkinter.Entry(self.window, width=25, textvariable=self.contactNumber)
#         self.historyEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)
#         self.doctorEntry = tkinter.Entry(self.window, width=25, textvariable=self.doctor)
#         self.symptomEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)
#         self.rubricEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)
#         self.medicineEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)
#         self.notesEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)
#         self.amountEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)


#         self.idEntry.grid(pady=5, column=3, row=1)
#         self.firstnameEntry.grid(pady=5, column=3, row=2)
#         self.lastnameEntry.grid(pady=5, column=3, row=3)
#         self.addressEntry.grid(pady=5, column=3, row=8)
#         self.contactNumberEntry.grid(pady=5, column=3, row=9)
#         self.historyEntry.grid(pady=5, column=3, row=11)
#         self.symptomEntry.grid(pady=5, column=3, row=12)
#         self.rubricEntry.grid(pady=5, column=3, row=13)
#         self.medicineEntry.grid(pady=5, column=3, row=14)
#         self.notesEntry.grid(pady=5, column=3, row=15)
#         self.amountEntry.grid(pady=5, column=3, row=16)

#         # Combobox
#         self.dateOfBirthBox = tkinter.ttk.Combobox(self.window, values=self.dateType, width=20)
#         self.monthOfBirthBox = tkinter.ttk.Combobox(self.window, values=self.monthType, width=20)
#         self.yearOfBirthBox = tkinter.ttk.Combobox(self.window, values=self.yearType, width=20)
#         self.genderBox = tkinter.ttk.Combobox(self.window, values=self.genderType, width=20)
#         self.bloodListBox = tkinter.ttk.Combobox(self.window, values=self.bloodListType, width=20)

#         self.dateOfBirthBox.grid(pady=5, column=3, row=4)
#         self.monthOfBirthBox.grid(pady=5, column=3, row=5)
#         self.yearOfBirthBox.grid(pady=5, column=3, row=6)
#         self.genderBox.grid(pady=5, column=3, row=7)
#         self.bloodListBox.grid(pady=5, column=3, row=11)


        
        
#         # Button
#         tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                        text="Update", command=self.Update).grid(pady=15, padx=5, column=1,
#                                                                 row=14)
#         tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                        text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=14)
#         tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
#                        text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3,
#                                                                        row=14)

#         self.window.mainloop()

#     def Update(self):
#         self.database = Database()
#         self.database.Update(self.firstnameEntry.get(), self.lastnameEntry.get(), self.dateOfBirthBox.get(), self.monthOfBirthBox.get(),
#                              self.yearOfBirthBox.get(), self.genderBox.get(), self.addressEntry.get(), self.contactNumberEntry.get(),
#                              self.bloodListBox.get(), self.historyEntry.get(), self.symptomEntry.get(), self.rubricEntry.get(), 
#                              self.medicineEntry.get(), self.notesEntry.get(), self.amountEntry.get(), self.id)
#         tkinter.messagebox.showinfo("Updated data", "Successfully updated the above data in the database")

#     def Reset(self):
#         self.idEntry.delete(0, tkinter.END)
#         self.firstnameEntry.delete(0, tkinter.END)
#         self.lastnameEntry.delete(0, tkinter.END)
#         self.dateOfBirthBox.set("")
#         self.monthOfBirthBox.set("")
#         self.yearOfBirthBox.set("")
#         self.genderBox.set("")
#         self.addressEntry.delete(0, tkinter.END)
#         self.contactNumberEntry.delete(0, tkinter.END)
#         self.bloodListBox.set("")
#         self.historyEntry.delete(0, tkinter.END)
#         self.symptomEntry.delete(0, tkinter.END)
#         self.rubricEntry.delete(0, tkinter.END)
#         self.medicineEntry.delete(0, tkinter.END)
#         self.notesEntry.delete(0, tkinter.END)
#         self.amountEntry.delete(0, tkinter.END)
        
