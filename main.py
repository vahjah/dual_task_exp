# -***- The main.py file generates the DiViDu-next graphical user interface and is the is the execution script for the program -***-

import tkinter as tk
import tkinter.messagebox
import customtkinter
import modules.integrated as integrated
import modules.word_list as word_list
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import sys
import os
import yaml
import multiprocessing
import ssl

# the main GUI uses customtkinter which provides a modern python library for developing user interfaces
# see https://customtkinter.tomschimansky.com for details

# this line is added to the code to avoide certificate errors on the target machine
ssl._create_default_https_context = ssl._create_unverified_context

# these two lines provide the default GUI appearance and button colour
# replacing "Dark" with "Light" will provide a default light colour mode
# replacing "green" with another colour, for example "blue" will change the button colours in the GUI
customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("green") 

# These are global variables used in the code "file1" and "file2" provide the folder location that the word list text files will be saved 
# and the location where the settings files will be saved, The reaming variables are initialised here and can be updated in the functions below
file1 = 'data/word_list.txt'
file2 = 'settings/config.yaml'
key_press = 'l'
next_word_key_press = '<space>'
welcome_text = 'Press enter key to start the experiment, then chosen key to reveal each new word and as each word displays please describe its meaning as clearly as you can'
experiment_name = 'no name'

# this "ToplevelWindow_1" class provides a "top level window" gui that will open over the top of the main GUI
# this class provides a GUI to create a new list of words, providing a window where words can be listed 
# and a function to save the file as a text file, including opening a dialogue box to enter a name for the saved file
class ToplevelWindow_1(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # these two lines obtain the screen width and height as part of enabling the top level GUI to be positioned
        # centrally on the screen
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # defines the size of the GUI
        self.window_width = 500 
        self.window_height = 800  
        
        # use the screen dimensions and the GUI dimensions to position the GUI in the centre
        # of the screen
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        # create a label st the top of the GUI window
        self.label = customtkinter.CTkLabel(self, text="Create new word list by adding each word on a new line")
        self.label.pack(padx=20, pady=20)
        
        # provide a text box in the centre of the top level GUI, the text box is given dimentions
        # for height and width and the "padx" and "pady" position the text box centrally
        self.text_box = customtkinter.CTkTextbox(self, height=600, width=460)
        self.text_box.insert("1.0","[Add Your Text Here]")
        self.text_box.pack(padx=20, pady=20)
        
        # create a tkinter button widget, labelled "save" and assigned with the save_file fundtion defined next
        self.main_button_1 = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"),text="Save", command=self.save_file)
        self.main_button_1.pack(padx=20, pady=20)

        # the save file function names the new word list file and saves to the data folder (defined in the file1 variable)
    def save_file(self):
        
        # opens a dialogue box and requests a file name input 
        file_name = customtkinter.CTkInputDialog(text="Enter a name for your file:", title="File Name")
        file_name = file_name.get_input()
        base_name =''
        ext = '.txt'
        
        # assigns the name the .txt suffix, unless the user did this already when naming the file
        if file_name:
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            
            # this refers to 'frozen' to detect hen running in a package and the data folder may not be
            # in the same directory as the main.py file
            if getattr(sys, 'frozen', False):
                folder = os.path.dirname(sys.executable)
                folder_path = os.path.join(folder, 'data')
            else:
                folder_path = 'data'
            
            # joins the file path and the file name into a new file path so can be saved to the data folder
            file_path = os.path.join(folder_path, file_name)
            
            # this part of the function checks if the file name input has been used before, to avoid overwritting the file
            # the function adds or increments a number to the end so saved as a seperate file, then closes the GUI
            if os.path.exists(file_path):
                index = 1
                base_name, ext = os.path.splitext(file_name)
                while os.path.exists(os.path.join(folder_path,f"{base_name}_{index}{ext}")):
                    index += 1
                file_name = f"{base_name}_{index}{ext}"
                file_path = os.path.join(folder_path, file_name)
            
            # opens the file path and writes the file to the path to save
            with open(file_path, "w") as file1:
                data = self.text_box.get("1.0", "end-1c")
                file1.write(data)
            print(f"File saved to '{file_path}'.")
        else:
            print("File save cancelled.")
        self.destroy()

# this "ToplevelWindow_2" class provides a "top level window" gui that will open over the top of the main GUI
# this class provides a GUI to edit a word file, providing a window where words int file will be displayed and can be edited
# provides a further function to save the edited file 
class ToplevelWindow_2(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # these two lines obtain the screen width and height as part of enabling the top level GUI to be positioned
        # centrally on the screen
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # defines the size of the GUI
        self.window_width = 500  
        self.window_height = 800  
        
        # use the screen dimensions and the GUI dimensions to position the GUI in the centre
        # of the screen
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        # create a label st the top of the GUI window
        self.label = customtkinter.CTkLabel(self, text="Edit word list, ensure each word is on a new line")
        self.label.pack(padx=20, pady=20)
        
        # provide a text box in the centre of the top level GUI, the text box is given dimentions
        # for height and width and the "padx" and "pady" position the text box centrally
        self.text_box = customtkinter.CTkTextbox(self, height=600, width=460)
        self.text_box.pack(padx=20, pady=20)
        
        # create a tkinter button widget, labelled "save" and assigned with the save_file fundtion defined next
        self.main_button_2 = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"),text="Save", command=self.save_file)
        self.main_button_2.pack(padx=20, pady=20)
        
        # calls open_file function below 
        self.open_file()

    def open_file(self):
        
        # opens a dialogue box displaying text files saved into the data folder 
        self.file_path = filedialog.askopenfilename(initialdir='data',filetypes=[("Text Files", "*.txt")])
        
        # opens the selected word list file, reads the contents and displays in the edit GUI
        if self.file_path:
            with open(self.file_path, "r") as file:
                text = file.read()
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, text)
        else:
            print("File open cancelled.")
            self.destroy()
        
    # function saves the information entered into the eidt GUI into the selected text file, replacing the previous content, then closes the GUI
    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                text = self.text_box.get("1.0", tk.END)
                file.write(text)
            print(f"File saved to '{self.file_path}'.")
        else:
            print("File save cancelled.")
        self.destroy()

# this "ToplevelWindow_3" class provides a "top level window" gui that will open over the top of the main GUI
# this class provides a GUI to edit the welcome message
class ToplevelWindow_3(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # the global key word is required to use the global variable
        global welcome_text
        
        # these two lines obtain the screen width and height as part of enabling the top level GUI to be positioned
        # centrally on the screen
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # defines the size of the GUI
        self.window_width = 500 
        self.window_height = 500  
        
        # use the screen dimensions and the GUI dimensions to position the GUI in the centre
        # of the screen
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        # create a label st the top of the GUI window
        self.label = customtkinter.CTkLabel(self, text="Edit the welcome screen message")
        self.label.pack(padx=20, pady=20)
        
        # provide a text box in the centre of the top level GUI, the text box is given dimentions
        # for height and width and the "padx" and "pady" position the text box centrally
        self.text_box = customtkinter.CTkTextbox(self, height=300, width=460)
        self.text_box.insert("1.0",welcome_text)
        self.text_box.pack(padx=20, pady=20)
        
        # create a tkinter button widget, labelled "save" and assigned with the save_file fundtion defined next
        self.main_button_1 = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"),text="Save", command=self.save_file)
        self.main_button_1.pack(padx=20, pady=20)

    # assigns the the changes to the welcome_text global variable and closes the GUI
    def save_file(self):
        global welcome_text
        welcome_text = self.text_box.get("0.0",tk.END)
        self.destroy()

# this class provides the main DiViDu-next user interface, it sets out the GUI using the "grid" function and "widgets" (Buttons, option menus, sliders etc)
# used to gather user input for the experiment and manage the settings
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # the global key word is required to use the global variable
        global file1
        global file2
        
        # this refers to 'frozen' to detect when running in a package to find the folder path
        # and ensure the folder locations for data and settings can be found
        if getattr(sys, 'frozen', False):
            application_path = sys.executable
        else:
            application_path = os.path.abspath(__file__)

        application_directory = os.path.dirname(application_path)

        file1 = os.path.join(application_directory, 'data/word_list.txt')
        file2 = os.path.join(application_directory, 'settings/config.yaml')

        # labels the DiViDu-next GUI at top of the GUI window
        self.title("DiViDu-next main menu")
        
        # these two lines obtain the screen width and height as part of enabling the top level GUI to be positioned
        # centrally on the screen
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # defines the size of the GUI
        self.window_width = 540
        self.window_height = 900  
        x = (self.screen_width // 2) - (self.window_width // 2)
        y = (self.screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    
        # this configures the grid layout of the GUI
        self.grid_columnconfigure((1,2,3), weight=1)
        self.grid_rowconfigure((1,2,3), weight=1)


                                             #********* SIDE BAR *************

        # This section of code creates the sidebar in the GUI that contains the start button, settings buttons, report button etc
        # the below lines create the side bar "frame" defining its size, the number of rows and providing a title to the side bar "DiViDu-next"
        self.sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="DiViDu-next", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # create the sidebar button widgets, the first line creates the button, places into the sideframe, assigns the function that will run when clicked and labels the button
        # the second line positions the button into a row in the frame and uses padx and pady to position the button
        self.sidebar_button_start = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_start, text="Start")
        self.sidebar_button_start.grid(row=1, column=0, padx=(20), pady=10)
        self.sidebar_button_settings = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_settings, text="Select settings")
        self.sidebar_button_settings.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_save = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_save, text="Save settings")
        self.sidebar_button_save.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_reports = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_reports, text="View reports")
        self.sidebar_button_reports.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_exit = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_exit, text="Exit")
        self.sidebar_button_exit.grid(row=5, column=0, padx=20, pady=10)

        # creates an option widget in the sidebard frame with a label above it, assigns a function to change the GUI appearance between light and dark
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance:")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="s")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, anchor="center")
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 20))

        # creates an option widget in the sidebard frame with a label above it, assigns a function to change the GUI scale
        # this function enables adjustment of the GUI to fit 
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="GUI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["70%", "80%", "90%", "100%", "110%", "120%", "130%"],
                                                               command=self.change_scaling_event,anchor="center")
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))


                                        #*********** TOP FRAME ***********
        
        # This section of code creates the top frame in the GUI that contains the buttons to change the main experiment settings that
        # apply regardless of which secondary task is chosen 
        # the code creates the "frame" defining its size, the number of rows.
        self.pt_button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.pt_button_frame.grid(row=0, column=1, rowspan=6, columnspan=1, sticky="nsew")
        self.pt_button_frame.grid_rowconfigure(10, weight=1)
        
        # adds an invisible button into row 0, without this the formating of the buttons will not line up with the main fram
        self.pt_button_0_label = customtkinter.CTkLabel(self.pt_button_frame, text="")
        self.pt_button_0_label.grid(row=0, column=1, padx=(10,10), pady=10, sticky="nsew")
        
        # -*- SELECT WORD LIST BUTTON -*-
        # creates button to select the word list, places into the button frame and assigns the function to command to search for the word list file
        self.pt_button_1 = customtkinter.CTkButton(master=self.pt_button_frame, command=self.pt_button_1_click, text="Select word list")
        self.pt_button_1.grid(row=1, column=2, columnspan=1, padx=(15,75), pady=10, sticky="nsew") 
        self.pt_button_1_label = customtkinter.CTkLabel(self.pt_button_frame, text="Select word list")
        self.pt_button_1_label.grid(row=1, column=1, padx=(40,10), pady=10, sticky="e")

        # -*- CREATE WORD LIST BUTTON -*-
        # creates button to create the word list, places into the button frame and assigns the function to command to create a new word list file
        self.pt_button_2 = customtkinter.CTkButton(master=self.pt_button_frame, command=self.pt_button_2_click, text="Create word list")
        self.pt_button_2.grid(row=2, column=2, columnspan=1, padx=(15,75), pady=10, sticky="nsew")
        self.pt_button_2_label = customtkinter.CTkLabel(self.pt_button_frame, text="Create word list")
        self.pt_button_2_label.grid(row=2, column=1, padx=(40,10), pady=10, sticky="e")

        # -*- EDIT WORD LIST BUTTON -*-
        # creates button to edit a word list, places into the button frame and assigns the function to command to open and edit a word list file through the GUI
        self.pt_button_3 = customtkinter.CTkButton(master=self.pt_button_frame, command=self.pt_button_3_click, text="Edit word list")
        self.pt_button_3.grid(row=3, column=2, columnspan=1, padx=(15,75), pady=10, sticky="nsew")
        self.pt_button_3_label = customtkinter.CTkLabel(self.pt_button_frame, text="Edit word list")
        self.pt_button_3_label.grid(row=3, column=1, padx=(40,10), pady=10, sticky="e")

        # -*- CHANGE WORD FONT SIZE OPTION -*-
        # creates button to change the primary task font size, 
        #places into the button frame and assigns to a variable
        self.st_options_2 = ["large", "medium", "small"]
        self.st_var_2 = customtkinter.StringVar(self)
        self.st_var_2.set(self.st_options_2[0])
        self.st_option_2 = customtkinter.CTkOptionMenu(master=self.pt_button_frame, values=self.st_options_2, variable=self.st_var_2,anchor="center")
        self.st_option_2.grid(row=4, column=2, columnspan=1,padx=(15, 75), pady=10, sticky="nsew")
        self.st_option_2_label = customtkinter.CTkLabel(master=self.pt_button_frame, text="Word font size", anchor="n")
        self.st_option_2_label.grid(row=4, column=1, padx=(40,10), pady=(14,6), sticky="e")

        # -*- EDIT WELCOME SCREEN MESSAGE BUTTON -*-
        # creates button to edit the welcome screen, places into the button frame and assigns the function to command to open a top level window to edit
        self.pt_button_4 = customtkinter.CTkButton(master=self.pt_button_frame, text="Edit welcome", command=self.pt_button_4_click)
        self.pt_button_4.grid(row=6, column=2, padx=(15, 75), pady=10, sticky="nsew")
        self.pt_button_4_label = customtkinter.CTkLabel(master=self.pt_button_frame, text="Edit welcome screen")
        self.pt_button_4_label.grid(row=6, column=1, padx=10, pady=10, sticky="e")
       
        # -*- SELECT WORD KEY BUTTON -*-
        # creates button to select the key the progresses words through in the experiment
        # places into the button frame and assigns the function to command to open a dialog box to capture the chosen letter
        self.pt_button_5 = customtkinter.CTkButton(master=self.pt_button_frame, text="Word key", command=self.open_input_dialog_event_next_word)
        self.pt_button_5.grid(row=5, column=2, padx=(15, 75), pady=10, sticky="nsew")
        self.pt_button_5_label = customtkinter.CTkLabel(master=self.pt_button_frame, text="Select next word key")
        self.pt_button_5_label.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        # -*- SLECT PRIMARY TASK SCREEN SIDE OPTION -*-
        # creates option widget to select the side for the primary task
        # places into the button frame and assigns to a variable
        self.st_options_1 = ["left", "right"]
        self.st_var_1 = customtkinter.StringVar(self)
        self.st_var_1.set(self.st_options_1[0])
        self.st_option_1 = customtkinter.CTkOptionMenu(master=self.pt_button_frame, values=self.st_options_1, variable=self.st_var_1,anchor="center")
        self.st_option_1.grid(row=7, column=2, columnspan=1, padx=(15,75), pady=10, sticky="nsew")
        self.st_option_1_label = customtkinter.CTkLabel(master=self.pt_button_frame, text="Select primary side", anchor="n")
        self.st_option_1_label.grid(row=7, column=1, columnspan=1, padx=10, pady=10, sticky="e")
        
        # -*- SCHEDULE TASK BREAK OPTION -*-
        # creates option widget to set a time for a break period
        self.optionmenu_5 = customtkinter.CTkOptionMenu(master=self.pt_button_frame, values=["5","10","15","20","25","30","35","40","45","50"],anchor="center")
        self.optionmenu_5.grid(row=8, column=2, columnspan=1, padx=(15,75), pady=10, sticky="nsew")
        self.label_optionmenu_5 = customtkinter.CTkLabel(master=self.pt_button_frame, text="Break after 'n' words", anchor="n")
        self.label_optionmenu_5.grid(row=8, column=1, columnspan=1, padx=10, pady=10, sticky="e")

        # -*- SELECT SECONDARY TASK OPTION -*-
        # creates option widget to select the secondary task
        # places into the button frame and assigns to a variable
        self.st_options_3 = ["reaction_click", "color_match", "snake"]
        self.st_var_3 = customtkinter.StringVar(self)
        self.st_var_3.set(self.st_options_3[0])
        self.st_option_3 = customtkinter.CTkOptionMenu(master=self.pt_button_frame, values=self.st_options_3, variable=self.st_var_3,anchor="center")
        self.st_option_3.grid(row=9, column=2, padx=(15,75), pady=10, sticky="nsew")
        self.st_option_3_label = customtkinter.CTkLabel(master=self.pt_button_frame, text="Select task", anchor="n")
        self.st_option_3_label.grid(row=9, column=1, columnspan=1, padx=10, pady=10, sticky="e")
    
        
                                            #**********TAB VIEW*************
        
        # This section of code creates the tab frame in the GUI that contains the widgets 
        # to change the secondary task settings 
        # the code creates the "tab frame" with a tab for each game and places into the GUI grid.
        self.tabview = customtkinter.CTkTabview(self, width=80)
        self.tabview.grid(row=7, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("reaction_click")
        self.tabview.add("color_match")
        self.tabview.add("snake")
        self.tabview.tab("reaction_click").grid_columnconfigure(0, weight=1) 
        self.tabview.tab("color_match").grid_columnconfigure(0, weight=1)
        self.tabview.tab("snake").grid_columnconfigure(0, weight=1)

                                             # *** REACTION CLICK TAB ***

        # -*- SELECT BOX COLOUR OPTION -*-
        # creates option widget to select the reaction click secondary task box colour
        # places into the reaction click tab 
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("reaction_click"), dynamic_resizing=False, values=["red", "yellow", "green", "blue", "black"],anchor="center")
        self.optionmenu_1.grid(row=1, column=1, padx=(20, 30), pady=(10, 10))
        self.label_optionmenu_1 = customtkinter.CTkLabel(self.tabview.tab("reaction_click"), text="Box color")
        self.label_optionmenu_1.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="e")
        
        # -*- SELECT BOX SIZE OPTION -*-
        # creates option widget to select the reaction click secondary task box size
        # places into the reaction click tab 
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("reaction_click"), values=["large", "medium", "small"],anchor="center")
        self.optionmenu_2.grid(row=2, column=1, padx=(20, 30), pady=(10, 10))
        self.label_optionmenu_2 = customtkinter.CTkLabel(self.tabview.tab("reaction_click"), text="Box size")
        self.label_optionmenu_2.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="e")

        # -*- SELECT REACTION KEY TO PRESS -*-
        # creates button widget to open a dialogue box to enter the reaction click key to press to dismiss the box
        # places into the reaction click tab 
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("reaction_click"), text="Key to press", command=self.open_input_dialog_event)
        self.string_input_button.grid(row=3, column=1, padx=(20, 30), pady=(10, 10))
        self.label_string_input_button = customtkinter.CTkLabel(self.tabview.tab("reaction_click"), text="Set key")
        self.label_string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="e")

        # -*- SLIDER WIDGET MINIMUM DELAY -*-
        # creates slider widget to set a value between 0 and 10 seconds for the minimum time after the box is 
        # dismissed before will reappear and places into the reaction click tab 
        self.label_delay_setting_1 = customtkinter.CTkLabel(self.tabview.tab("reaction_click"), text="Box appear minimum (sec)")
        self.label_delay_setting_1.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="nsew")
        self.slider_1 = customtkinter.CTkSlider(self.tabview.tab("reaction_click"), from_=0, to=10, number_of_steps=20)
        self.slider_1.grid(row=5, column=0, columnspan=2, padx=(20, 10), pady=(0, 10), sticky="ew")
        
        # -*- SLIDER WIDGET MAXIMUM DELAY -*-
        # creates slider widget to set a value between 0 and 10 seconds for the maximum time after the box is 
        # dismissed before will reappear and places into the reaction click tab 
        self.label_delay_setting_2 = customtkinter.CTkLabel(self.tabview.tab("reaction_click"), text="Box appear maximum (sec)")
        self.label_delay_setting_2.grid(row=6, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="nsew")
        self.slider_2 = customtkinter.CTkSlider(self.tabview.tab("reaction_click"), from_=0, to=10, number_of_steps=20)
        self.slider_2.grid(row=7, column=0, columnspan=2, padx=(20, 10), pady=(0, 10), sticky="ew")

        
        # this function configures slider_1 (minimum) to adjust the value of slider_2
        # so that is cannot exceed the value of slider_2 (maximum)
        def adjust_slider_1_value(value):
            if self.slider_2.get() < float(value):
                self.slider_2.set(float(value))
                self.label_delay_setting_2.configure(text=f"Box appear maximum (sec) {value}")
           
            self.label_delay_setting_1.configure(text=f"Box appear minimum (sec) {value}")
        self.slider_1.configure(command=adjust_slider_1_value)

        # this function configures slider_2 (maximum) to adjust the value of slider_2
        # so that is cannot be set below the value of slider_1 (minimum)
        def adjust_slider_2_value(value):
            if self.slider_1.get() > float(value):
                self.slider_1.set(float(value))
                self.label_delay_setting_1.configure(text=f"Box appear minimum (sec) {value}")
            
            self.label_delay_setting_2.configure(text=f"Box appear maximum (sec) {value}")
        self.slider_2.configure(command=adjust_slider_2_value)

        # -*- SWITCH WIDGET FIX REACTION CLICK BOX TO CENTRE -*-
        # creates slider widget to set a value between 0 and 10 seconds for the maximum time after the box is 
        # dismissed before will reappear and places into the reaction click tab 
        self.label_switch = customtkinter.CTkLabel(self.tabview.tab("reaction_click"), text="Fix box to centre")
        self.label_switch.grid(row=8, column=0, columnspan=2, padx=20, pady=(20, 20), sticky="w")
        self.switch = customtkinter.CTkSwitch(self.tabview.tab("reaction_click"), text="Fixed")
        self.switch.grid(row=8, column=1, columnspan=2, padx=(10, 10), pady=(20, 20), sticky="e")
        
                                             # *** COLOR MATCH TAB ***

        # -*- SELECT NUMBER OF COLOURS -*-
        # creates option widget to select the number of colours for the colour match task
        # places into the color match tab
        self.optionmenu_4 = customtkinter.CTkOptionMenu(self.tabview.tab("color_match"), dynamic_resizing=False, values=["5","10","15","20"],anchor="center")
        self.optionmenu_4.grid(row=1, column=1, padx=(10, 30), pady=(10, 10))
        self.label_optionmenu_4 = customtkinter.CTkLabel(self.tabview.tab("color_match"), text="Number colors")
        self.label_optionmenu_4.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="e")


        # -*- SLIDER WIDGET DURATION -*-
        # creates slider widget to set a value between 0 and 10 seconds for the duration  
        self.label_speed_setting_1 = customtkinter.CTkLabel(self.tabview.tab("color_match"), text="Duration")
        self.label_speed_setting_1.grid(row=2, column=0, columnspan=2,  padx=20, pady=(10, 0), sticky="nsew")
        self.slider_5 = customtkinter.CTkSlider(self.tabview.tab("color_match"), from_=0, to=10, number_of_steps=10)
        self.slider_5.grid(row=3, column=0, columnspan=2, padx=(20, 10), pady=(0, 10), sticky="ew")
        
        # -*- SLIDER WIDGET INCREMENT -*-
        # creates slider widget to set a value between 0 and 10 seconds for the increment
        self.label_length_setting_2 = customtkinter.CTkLabel(self.tabview.tab("color_match"), text="Increment")
        self.label_length_setting_2.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="nsew")
        self.slider_6 = customtkinter.CTkSlider(self.tabview.tab("color_match"), from_=0, to=10, number_of_steps=10)
        self.slider_6.grid(row=5, column=0, columnspan=2, padx=(20, 10), pady=(0, 174), sticky="ew")

        # function to set the slider value
        def adjust_slider_5_value(value):
            self.label_speed_setting_1.configure(text=f"Duration {value}")

        self.slider_5.configure(command=adjust_slider_5_value)

        # function to set the slider value
        def adjust_slider_6_value(value):
            self.label_length_setting_2.configure(text=f"Increment {value}")
        
        self.slider_6.configure(command=adjust_slider_6_value)

                                                    # *** SNAKE TAB ***

        # -*- SELECT FOOD COLOUR -*-
        # creates option widget to select the food colour
        # places into the snake tab
        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.tabview.tab("snake"), dynamic_resizing=False, values=["red", "yellow", "green", "blue", "black"],anchor="center")
        self.optionmenu_3.grid(row=1, column=1, padx=(10, 30), pady=(10, 10))
        self.label_optionmenu_3 = customtkinter.CTkLabel(self.tabview.tab("snake"), text="Food color")
        self.label_optionmenu_3.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="e")

        # -*- SLIDER WIDGET SPEED -*-
        # creates slider widget to set a value between 0 and 10 seconds for the snake speed
        self.label_speed_setting_2 = customtkinter.CTkLabel(self.tabview.tab("snake"), text="Speed")
        self.label_speed_setting_2.grid(row=2, column=0, columnspan=2,padx=20, pady=(10, 0), sticky="nsew")
        self.slider_3 = customtkinter.CTkSlider(self.tabview.tab("snake"), from_=0, to=10, number_of_steps=10)
        self.slider_3.grid(row=3, column=0, columnspan=2, padx=(20, 10), pady=(0, 10), sticky="ew")
        
        # -*- SLIDER WIDGET SPEED -*-
        # creates slider widget to set a value between 0 and 10 seconds for the snake initial length
        self.label_length_setting_3 = customtkinter.CTkLabel(self.tabview.tab("snake"), text="Initial length")
        self.label_length_setting_3.grid(row=4, column=0, columnspan=2,padx=20, pady=(10, 0), sticky="nsew")
        self.slider_4 = customtkinter.CTkSlider(self.tabview.tab("snake"), from_=0, to=10, number_of_steps=10)
        self.slider_4.grid(row=5, column=0, columnspan=2, padx=(20, 10), pady=(0, 174), sticky="ew")

        # function to set the slider value
        def adjust_slider_3_value(value):
            self.label_speed_setting_2.configure(text=f"Duration {value}")

        self.slider_3.configure(command=adjust_slider_3_value)

        # function to set the slider value
        def adjust_slider_4_value(value):
            self.label_length_setting_3.configure(text=f"Increment {value}")
        
        self.slider_4.configure(command=adjust_slider_4_value)

        #general settings
        self.toplevel_window_1 = None
        self.toplevel_window_2 = None
        self.toplevel_window_3 = None
  
        #set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.optionmenu_1.set('red')
        self.optionmenu_2.set('medium')
        self.slider_1.set(1)
        self.slider_2.set(5)
        self.scaling_optionemenu.set("100%")
        self.switch.deselect()
        self.slider_3.set(3)
        self.slider_4.set(3)
        self.optionmenu_3.set("red")
        self.optionmenu_5.set("15")
        self.optionmenu_4.set(5)
        self.slider_5.set(5)
        self.slider_6.set(5)
        self.st_option_2.set("medium")
        self.st_option_1.set("left")

    
                                    # ***** FUNCTIONS CREATED FOR THE WIDGETS *****

    # function to create a pop up dialog box for the reaction click key
    def open_input_dialog_event(self):
        global key_press
        dialog = customtkinter.CTkInputDialog(text="Type in a key:", title="DiViDu setting")
        key_press = dialog.get_input()

    # function to create a pop up dialog box for the progress word list key
    def open_input_dialog_event_next_word(self):
        global next_word_key_press
        dialog = customtkinter.CTkInputDialog(text="Type in a key for next word:", title="DiViDu setting")
        next_word_key_press = dialog.get_input()    

    # function to change the appearance colour
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # function to adjust the GUI scaling
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # function to open top level window for "create word list"
    def open_toplevel_1(self):
        if self.toplevel_window_1 is None or not self.toplevel_window_1.winfo_exists():
            self.toplevel_window_1 = ToplevelWindow_1(self)  
        else:
            self.toplevel_window_1.focus()  

    # function to open top level window for "edit word list"
    def open_toplevel_2(self):
        if self.toplevel_window_2 is None or not self.toplevel_window_2.winfo_exists():
            self.toplevel_window_2 = ToplevelWindow_2(self)  
        else:
            self.toplevel_window_2.focus()  

    # function to open top level window for "edit welcome message"
    def open_toplevel_3(self):
        if self.toplevel_window_3 is None or not self.toplevel_window_3.winfo_exists():
            self.toplevel_window_3 = ToplevelWindow_3(self)  
        else:
            self.toplevel_window_3.focus()          

    # select word list function assigned to select word list button
    def pt_button_1_click(self):
        global file1 
        file1 = word_list.select_word_file()

    # assigned to create word list button
    def pt_button_2_click(self):
        self.open_toplevel_1()

    # assigned to edit word list button
    def pt_button_3_click(self):
        self.open_toplevel_2()

    # assigned to edit welcome message
    def pt_button_4_click(self):
        self.open_toplevel_3()
     
    # function that is assigned to the start button widget
    def sidebar_button_start(self):
        
        #  updates the experiment_name global variable with a numer entered in a dialogue box
        # if no name is provided will name the expeirment "no name"
        global experiment_name
        experiment_name = customtkinter.CTkInputDialog(text="Enter a name for this experiment:", title="Experiment name")
        experiment_name = experiment_name.get_input()
        if experiment_name == "":
            experiment_name = "no name"
        
        # calls the DualTaskExperiment class, passing the selected secondary task, the word list file. the number of
        # words in the word list file and the experiment name
        game_type = self.st_var_3.get()
        words = word_list.read_file(file1)
        integrated.random.shuffle(words)
        num_words = int(len(words))
        root = tk.Toplevel()
        integrated.DualTaskExperiment(root, words, file2, experiment_name, num_words=num_words, game_type=game_type)

    # function that is assigned to the select settings button widget
    # opens a settings file and sets each of the GUI widgets to the values 
    def sidebar_button_settings(self):
        global file2 
        file2 = word_list.select_settings_file()

        with open(file2) as file:
            self.config = yaml.safe_load(file)
   
        self.window_settings = self.config['window_settings']
        self.st_option_1.set(self.window_settings['p_task_side'])
        self.optionmenu_5.set(self.window_settings['break_after'])

        self.word_settings = self.config['word_settings']
        if self.word_settings['word_size'] == 20:
            self.st_option_2.set('small')
        elif self.word_settings['word_size'] == 25:
            self.st_option_2.set('medium')
        elif self.word_settings['word_size'] == 30:
            self.st_option_2.set('large')
        else:
            self.st_option_2.set('')

        self.reaction_click_settings = self.config['reaction_click_settings']
        self.optionmenu_1.set(self.reaction_click_settings['button_color'])
        self.optionmenu_2.set(self.reaction_click_settings['button_size'])
        value1 = (self.reaction_click_settings['delay_lowlimit'])
        value2 = (self.reaction_click_settings['delay_highlimit'])
        self.slider_1.set(value1)
        self.slider_2.set(value2)
        
        if self.reaction_click_settings['fix_centre'] == 1:   
            self.switch.select()
        else:
            self.switch.deselect()

        self.color_match_settings = self.config['color_match_settings']
        self.optionmenu_4.set(self.color_match_settings['num_colors'])
        self.slider_5.set(self.color_match_settings['color_duration'])
        self.slider_6.set(self.color_match_settings['score_increment'])

        self.snake_settings = self.config['snake_settings']
        self.optionmenu_3.set(self.snake_settings['food_color'])
        self.slider_3.set(self.snake_settings['snake_speed'])
        self.slider_4.set(self.snake_settings['initial_length'])

    # function that is assigned to the save settings button widget
    def sidebar_button_save(self):
        global file2
        global key_press
        global welcome_text
        global next_word_key_press

        # retrives the value that each widget in the GUI is currently set to
        reaction_click_button_color = self.optionmenu_1.get()
        reaction_click_button_size = self.optionmenu_2.get()
        reaction_click_delay_lowlimit = self.slider_1.get()
        reaction_click_delay_lowlimit = round(reaction_click_delay_lowlimit)
        reaction_click_delay_highlimit = self.slider_2.get()
        reaction_click_delay_highlimit = round(reaction_click_delay_highlimit)
        reaction_click_key_press = key_press
        reaction_click_fix_switch = self.switch.get()

        window_settings_next_word_key = next_word_key_press

        snake_snake_speed = self.slider_3.get()
        snake_snake_speed = round(snake_snake_speed)
        snake_initial_length = self.slider_4.get()
        snake_initial_length = round(snake_initial_length)
        snake_food_color = self.optionmenu_3.get()

        color_match_num_colors = self.optionmenu_4.get()
        color_match_num_colors = int(color_match_num_colors)
        color_match_color_duration = self.slider_5.get()
        color_match_color_duration = round(color_match_color_duration)
        color_match_score_increment = self.slider_6.get()
        color_match_score_increment = round(color_match_score_increment)

        # convert the font input into an integer to set font
        word_word_size = self.st_option_2.get()
        if word_word_size == "small":
            word_word_size = 20
        elif word_word_size == "medium":
            word_word_size = 25
        elif word_word_size == "large":
            word_word_size = 30

        window_settings_p_task_side = self.st_option_1.get()
        window_settings_welcome_message = welcome_text
        window_settings_break_after = self.optionmenu_5.get()
        window_settings_break_after = int(window_settings_break_after)

        # creates key value pairs for the settings YAML file
        settings = {
            "reaction_click_settings": {
                "button_color": reaction_click_button_color,
                "button_size": reaction_click_button_size,
                "delay_lowlimit": reaction_click_delay_lowlimit,
                "delay_highlimit": reaction_click_delay_highlimit,
                "key_press": reaction_click_key_press,
                "fix_centre": reaction_click_fix_switch
            },
            "snake_settings": {
                "snake_speed": snake_snake_speed,
                "initial_length": snake_initial_length,
                "food_color": snake_food_color
            },
            "color_match_settings": {
                "num_colors": color_match_num_colors,
                "color_duration": color_match_color_duration,
                "score_increment": color_match_score_increment
            },
            "word_settings": {
                "word_size": word_word_size
            },
            "window_settings": {
                "next_word_key": window_settings_next_word_key,
                "p_task_side": window_settings_p_task_side,
                "Welcome_message": window_settings_welcome_message,
                "break_after": window_settings_break_after
            }
        }

        # opens dialogue box, requests name for the settings file and adds yaml suffix
        file_name = customtkinter.CTkInputDialog(text="Enter a name for these saved settings:", title="File Name")
        file_name = file_name.get_input()
        base_name = ''
        ext = '.yaml'
        if file_name:
            if not file_name.endswith(".yaml"):
                file_name += ".yaml"
            # creates a path to save the new file into a folder
            folder_path = 'settings'
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                index = 1
                base_name, ext = os.path.splitext(file_name)
                while os.path.exists(os.path.join(folder_path, f"{base_name}_{index}{ext}")):
                    index += 1
                file_name = f"{base_name}_{index}{ext}"
                file_path = os.path.join(folder_path, file_name)
            # saves the key:value pairs defined in settings list to new YAML file
            with open(file_path, "w") as file:
                yaml.dump(settings, file)
            file2 = file_path
            print(f"File saved to '{file_path}'.")
        else:
            print("File save cancelled.")

    # function assigned to view reports button widget, opens reports folder
    def sidebar_button_reports(self):
        word_list.select_report_file()
    
    # function assigned to exit button widget, closes the GUI
    def sidebar_button_exit(self):
        root = tk._default_root
        root.destroy()




if __name__ == "__main__":
    
    # mulitprocessing is required to stop an issue with the packaging of DiViDu-next resulting in
    # multiple instances of the GUI opening
    multiprocessing.freeze_support()
    
    app = App()
    app.mainloop()
