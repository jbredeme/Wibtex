from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import os

class MyFrame(Frame):

    """
    Creates the frame for the GUI
    """
    def __init__(self):
        root = Tk()
        Frame.__init__(self)
        var = IntVar()
        content = ''
        file_path = ''
        self.master.title("WibTeX Reference Management System")
        self.master.rowconfigure(5, weight=0)
        self.master.columnconfigure(5, weight=0)
        self.grid(sticky=W+E+N+S)
        

        """
        Function to allow the user to browse their local directory for the
        BibTeX file and once selected it puts the file path into the e1 box
        """
        def callback():
            path = filedialog.askopenfilename()
            e1.delete(0, END)  # Remove current text in entry
            e1.insert(0, path)  # Insert the 'path'
            # print path

        """
        Function to allow the user to browse their local directory for the
        Docx file and once selected it puts the file path into the e2 box
        """
        def callback2():
            path = filedialog.askopenfilename()
            e2.delete(0, END)  # Remove current text in entry
            e2.insert(0, path)  # Insert the 'path'
            # print path

        """
        Function to allow the user to browse their local directory for the
        style file and once selected it puts the file path into the e3 box
        """
        def callback3():
            path = filedialog.askopenfilename()
            e3.delete(0, END)  # Remove current text in entry
            e3.insert(0, path)  # Insert the 'path'
            # print path
            
        """
        Function for the 'Run' Button to run the WibTeX program with the entry
        boxes used as the parameters for the program
        """
        def WibTeXrun():
            return


        """
        Creates the Entry text boxes for the file path to be inserted into.
        There is a total of three entry areas in the GUI for the:
        BibTeX file
        Docx File
        Style File
        """
        e1 = Entry(self, width=10)
        e1.pack()
        e2 = Entry(self, width=10)
        e2.pack()
        e3 = Entry(self, width=10)
        e3.pack()
        
        """
        Places entry boxes in the GUI based on their position in the grid
        """
        e1.grid(row=1, column=2, sticky=W)
        e2.grid(row=2, column=2, sticky=W)
        e3.grid(row=6, column=2, sticky=W)

        
        """
        Provides the text on the GUI or 'Labels'
        These help the user identify which files go where
        """
        Label(self, text="BibTeX File:").grid(row=1, column=1, sticky=W)
        Label(self, text="Docx File:").grid(row=2, column=1, sticky=W)       
        Label(self, text="Choose Style:").grid(row=3, column=1, sticky=W)        
        Label(self, text="Other Style:").grid(row=6, column=1, sticky=W)
        Label(self, text=" ").grid(row=1, column=4, sticky=W)
        Label(self, text=" ").grid(row=1, column=0, sticky=W)

        
        """
        Creates all of the buttons to browse for files in the local directory.
        Each button calls their own 'callback' function that is made only
        for that specific button's entry
        """
        self.button = Button(self, text="Browse", command=callback, width=5)
        self.button.grid(row=1, column=3, sticky=W)
        self.button = Button(self, text="Browse", command=callback2, width=5)
        self.button.grid(row=2, column=3, sticky=W)
        self.button = Button(self, text="Browse", command=callback3, width=5)
        self.button.grid(row=6, column=3, sticky=W)
        
        """
        Creates the radio buttons for the style options
        There are a total of 5 buttons and 4 of them are styles built in and
        the fifth one is built for users choosing their own style file
        """
        R1 = Radiobutton(self, text = "ACM", variable = var, value = 1).grid(row=3, column=2, sticky=W)
        R2 = Radiobutton(self, text = "CCSC", variable = var, value = 2).grid(row=3, column=3, sticky=W)
        R3 = Radiobutton(self, text = "IEEE", variable = var, value = 3).grid(row=4, column=3, sticky=W)
        R4 = Radiobutton(self, text = "APA", variable = var, value = 4).grid(row=4, column=2, sticky=W)
        R5 = Radiobutton(self, text = "Other", variable = var, value = 5).grid(row=4, column=1, sticky=W)
        selection = var.get()
        
        """
        Creates the run button to run the program, which will run the WibTeX program
        from its own defined function.
        """
        self.button = Button(self, text="Run", command=WibTeXrun, width=5)
        self.button.grid(row=7, column=3, sticky=E)


"""
Runs the GUI
"""

if __name__ == "__main__":
    MyFrame().mainloop()

