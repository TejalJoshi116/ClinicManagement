import tkinter as tk
from reportlab.pdfgen import canvas
from docx import Document
import sqlite3

class PatientManagementSystem:
    def __init__(self):
        self.connection = sqlite3.connect("clinic.db")
        self.cursor = self.connection.cursor()

        self.window = tk.Tk()
        self.window.title("Patient Management System")
        self.window.geometry("400x200")

        self.generate_pdf_button = tk.Button(self.window, text="Generate PDF Report", command=self.generate_pdf_report)
        self.generate_pdf_button.pack(pady=10)

        self.view_word_button = tk.Button(self.window, text="View Data in Word", command=self.view_data_in_word)
        self.view_word_button.pack(pady=10)

    def generate_pdf_report(self):
        self.cursor.execute("SELECT * FROM patient_table")
        data = self.cursor.fetchall()

        pdf = canvas.Canvas("patient_report.pdf")
        # Add content, tables, and formatting to the PDF document based on the retrieved data
        # ...
        # Modify this section to design the PDF report as per your requirements
        pdf.save()
        print("PDF report generated.")

    def view_data_in_word(self):
        self.cursor.execute("SELECT * FROM patient_table")
        data = self.cursor.fetchall()

        # Create a Word document
        doc = Document()
        # Add content, tables, and formatting to the Word document based on the retrieved data
        # ...
        # Modify this section to design the Word document as per your requirements
        doc.save("patient_data.docx")
        print("Patient data saved in Word document.")

    def run(self):
        self.window.mainloop()

# Create an instance of the PatientManagementSystem class and run the application
pms = PatientManagementSystem()
pms.run()
