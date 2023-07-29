import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import sys
import os
import subprocess


# select_word_file() function opens a file dialog for selecting a word file. 
# It checks whether the code is running in a frozen (compiled) executable or as a script. 
# It determines the appropriate folder path based on the execution context and returns the selected file path. 
# If no file is selected, it defaults to a predefined file path.
def select_word_file():
    if getattr(sys, 'frozen', False):
        folder = os.path.dirname(sys.executable)
        folder_path = os.path.join(folder, 'data')
    else:
        folder_path = 'data'

    file_path = askopenfilename(initialdir=folder_path)
    if file_path == "":
        file_path = os.path.join(folder_path, 'word_list.txt')
    return file_path


# select_settings_file() function handles the selection of a settings file.
def select_settings_file():
    if getattr(sys, 'frozen', False):
        folder = os.path.dirname(sys.executable)
        folder_path = os.path.join(folder, 'settings')
    else:
        folder_path = 'settings'

    file_path = askopenfilename(initialdir=folder_path)
    if file_path == "":
        file_path = os.path.join(folder_path, 'config.yaml')
    return file_path

# The select_report_file() function is responsible for opening a file dialog to select a report file. 
# It also checks the execution context and sets the appropriate folder path. 
# It opens the selected file using the default program associated with the file type on the operating system.
def select_report_file():
    if getattr(sys, 'frozen', False):
        folder = os.path.dirname(sys.executable)
        folder_path = os.path.join(folder, 'reports')
    else:
        folder_path = 'reports'

    try:
        if not os.path.exists(folder_path):
            raise OSError("Reports folder does not exist.")

        files = os.listdir(folder_path)

        selected_file = askopenfilename(
            initialdir=folder_path,
            title="Select a file to open",
            filetypes=[("All Files", "*.*")]
        )

        if selected_file:
            if sys.platform == 'darwin':
                subprocess.Popen(['open', selected_file])
            elif sys.platform == 'win32':
                os.startfile(selected_file)
            else:
                subprocess.Popen(['xdg-open', selected_file])

    except OSError as e:
        messagebox.showerror("Error", f"As you have not created any reports yet, the {str(e)}")

# The create_word_list_file() function creates a word list file with the given file name. 
# It determines the base path based on the execution context, joins it with the file name, 
# and writes the word list to the file.
def create_word_list_file(file_name):
    if getattr(sys, 'frozen', False):

        base_path = os.path.dirname(sys.executable)
    else:
        base_path = ''

    file_path = os.path.join(base_path, file_name)

    with open(file_path, "w") as file:
        word_list = add_word()
        file.write(word_list)

# The open_text_file() function opens a text file using the default program 
# associated with text files on the operating system. It takes a file name as input and determines 
# the base path based on the execution context. It then joins the base path with the file name and executes the file
def open_text_file(file_name):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = ''

    file_path = os.path.join(base_path, file_name)
    subprocess.run(["open", file_path])

# The read_file() function reads a file and returns a list of words. 
# It takes a file path as input and handles the execution context similar to other functions. 
# It reads the file contents and splits it into a list of words, which is then returned.
def read_file(file_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = ''

    file_path = os.path.join(base_path, file_path)

    if file_path == "":
        file_path = os.path.join(base_path, 'data/word_list.txt')

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Stripping leading/trailing whitespace from each line and ignoring lines with only whitespace
    word_list = [line.strip() for line in lines if line.strip() != '']
    return word_list

