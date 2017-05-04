from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import style
import logger
import main

# Construct logger
log = logger.SimpleLogger()

# Construct the window
root = Tk()
root.wm_title("WibTeX RMS")
root.resizable(width=False, height=False)
root.geometry("350x200")
root.configure(background='#2c5897')

# Construct labels
input_doc_label = Label(root, text="Input Document", fg='white', bg="#2c5897", font=("Calibri", 14))
input_bib_label = Label(root, text="Input Database", fg='white', bg="#2c5897", font=("Calibri", 14))
input_style_label = Label(root, text="Input Style", fg='white', bg="#2c5897", font=("Calibri", 14))
output_doc_label = Label(root, text="Output Document", fg='white', bg="#2c5897", font=("Calibri", 14))

input_doc_label.grid(row=0, sticky=W)
input_bib_label.grid(row=1, sticky=W)
input_style_label.grid(row=2, sticky=W)
output_doc_label.grid(row=3, sticky=W)

# Construct fields
input_doc_entry = Entry(root)
input_bib_entry = Entry(root)
output_doc_entry = Entry(root)

input_doc_entry.grid(row=0, column=1)
input_bib_entry.grid(row=1, column=1)
output_doc_entry.grid(row=3, column=1)

# Construct drop-down menu
initial = StringVar(root)
initial.set("")

drop_down = OptionMenu(root, initial, *style.get_valid_styles(log))
drop_down.grid(row=2, column=1, sticky=N) 

# Define functions
def browse_path(event, arg):
    path = filedialog.askopenfilename()
    arg.delete(0, END)
    arg.insert(0, path)
    return

def run(event, arg):

    # Verify input Word document
    if not input_doc_entry.get().endswith('.docx'):
        log.log_data("Error: Expected Word file extension '.docx' for first argument")
        showinfo("Window", "Expected Word file extension '.docx' for first argument")
        return

    # Verify BibTeX database
    if not input_bib_entry.get().endswith('.bib'):
        log.log_data("Error: Expected BibTeX file extension '.bib' for second argument")
        showinfo("Window", "Expected BibTeX file extension '.bib' for second argument")
        return

    # Verify output Word document
    if not output_doc_entry.get().endswith('.docx'):
        log.log_data("Error: Expected Word file extension '.docx' for fourth argument")
        showinfo("Window", "Expected Word file extension '.docx' for fourth argument")
        return

    main.execute(input_bib_entry.get(), input_doc_entry.get(), initial.get(), output_doc_entry.get(), log)
    showinfo("Window", "Execution is complete! :)")
    return

# Construct buttons
input_doc_button = Button(root, text="Browse", bg="grey", fg="white", font=("Calibri", 10))
input_bib_button = Button(root, text="Browse", bg="grey", fg="white", font=("Calibri", 10))
execute_button = Button(root, text="Run", bg="grey", fg="white", font=("Calibri", 10))

input_doc_button.bind("<Button-1>", lambda event, arg=input_doc_entry: browse_path(event, arg))
input_bib_button.bind("<Button-1>", lambda event, arg=input_bib_entry: browse_path(event, arg))
execute_button.bind("<Button-1>", lambda event, arg="": run(event, arg))

input_doc_button.grid(row=0, column=2, sticky=E)
input_bib_button.grid(row=1, column=2, sticky=E)
execute_button.grid(row=4, column=1, sticky=S)

root.grid_columnconfigure(4, minsize=100)

# Push window and loop
root.mainloop()