from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import os
import style
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
        def input_bib():
            path = filedialog.askopenfilename()
            e1.delete(0, END)  # Remove current text in entry
            e1.insert(0, path)  # Insert the 'path'
            # print path

        """
        Function to allow the user to browse their local directory for the
        Docx file and once selected it puts the file path into the e2 box
        """
        def input_doc():
            path = filedialog.askopenfilename()
            e2.delete(0, END)  # Remove current text in entry
            e2.insert(0, path)  # Insert the 'path'
            # print path

        """
        Function to allow the user to browse their local directory for the
        style file and once selected it puts the file path into the e3 box
        """
        """
        def callback3():
            path = filedialog.askopenfilename()
            e3.delete(0, END)  # Remove current text in entry
            e3.insert(0, path)  # Insert the 'path'
            # print path
        """
        
        """
        Function for the 'Run' Button to run the WibTeX program with the entry
        boxes used as the parameters for the program
        """
        def WibTeXrun():
            os.system('main.py')
            return

        def callstyles():
            """
            import main
            import style
            style.get_valid_styles()
            """
            return

        style_data = style.get_valid_styles()           

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
        
        """
        e3 = Entry(self, width=10)
        e3.pack()
        """
        
        """
        Places entry boxes in the GUI based on their position in the grid
        """
        e1.grid(row=1, column=2, sticky=W)
        e2.grid(row=2, column=2, sticky=W)
        """
        e3.grid(row=6, column=2, sticky=W)
        """

        
        """
        Provides the text on the GUI or 'Labels'
        These help the user identify which files go where
        """
        Label(self, text="BibTeX File:").grid(row=1, column=1, sticky=W)
        Label(self, text="Docx File:").grid(row=2, column=1, sticky=W)       
        Label(self, text="Choose Style:").grid(row=3, column=1, sticky=W)
        
        """
        Label(self, text="Other Style:").grid(row=6, column=1, sticky=W)
        """
        
        Label(self, text=" ").grid(row=1, column=4, sticky=W)
        Label(self, text=" ").grid(row=1, column=0, sticky=W)

        
        """
        Creates all of the buttons to browse for files in the local directory.
        Each button calls their own 'callback' function that is made only
        for that specific button's entry
        """
        self.button = Button(self, text="Browse", command=input_bib, width=5)
        self.button.grid(row=1, column=3, sticky=W)
        self.button = Button(self, text="Browse", command=input_doc, width=5)
        self.button.grid(row=2, column=3, sticky=W)
        var = StringVar(self)
        var.set("CCSC") # default value

        w = OptionMenu(self, var, *style_data)
        w.grid(row=3, column=2, sticky=W) 

        """
        Creates the run button to run the program, which will run the WibTeX program
        from its own defined function.
        """
        self.button = Button(self, text="Run", command=WibTeXrun, width=5)
        self.button.grid(row=3, column=3, sticky=E)


"""
Runs the GUI
"""

if __name__ == "__main__":
    MyFrame().mainloop()

