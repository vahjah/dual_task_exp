import tkinter as tk
from tkmacosx import Button
import random
import time
import modules.integrated

#  ReactionClickGame inherits from the tk.Frame class. The code sets up the game environment, handles key presses, 
# shows and hides the button, tracks reaction times, and logs game events.
class ReactionClickGame(tk.Frame):
    def __init__(self, master, config, screen_width, screen_height):
        
        # __init__ initializes the game 
        # it takes the master (the parent widget), the YAML file config, screen_width, and screen_height as parameters. 
        # It sets the width and height of the game window based on the screen dimensions. 
        # It also initializes variables for storing timestamps and game events.
        self.master = master
        self.width = screen_width // 2
        self.height = screen_height
        
        self.wrong_key_timestamp = None

        self.reaction_click_settings = config['reaction_click_settings']
        self.button_color = self.reaction_click_settings['button_color']
        self.button_size = self.reaction_click_settings['button_size']
        self.delay_lowlimit = self.reaction_click_settings['delay_lowlimit']
        self.delay_highlimit = self.reaction_click_settings['delay_highlimit']
        self.key_press = self.reaction_click_settings['key_press']
        self.fix_centre = self.reaction_click_settings['fix_centre']

        self.window_settings = config['window_settings'] 
        self.next_word_key = self.window_settings['next_word_key']


        super().__init__(master, width=self.width, height=self.height)
        self.master = master
        self.reaction_start_time = 0
        self.reaction_times = []
        self.events = []

        self.reaction_click_button = Button(self,  bg=self.button_color)
        
        self.schedule_reaction_click_button()
        self.timer_id = None
        #self.master.bind(self.key_press, self.handle_key_press)
        self.master.bind('<Key>', self.handle_key_press)
        self.master.focus_set()
        
    def hide_button(self):
        self.reaction_click_button.place_forget()
    #The schedule_reaction_click_button function schedules the appearance of the reaction click 
    # button with a random delay within the specified limits.
    def schedule_reaction_click_button(self):
        if self.winfo_exists():
            delay = random.uniform(self.delay_lowlimit, self.delay_highlimit)
            self.timer_id = self.master.after(int(delay * 1000), self.show_reaction_click_button)

    def reset(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.schedule_reaction_click_button()
    
    # the handle_key_press function is responsible for handling key press events. 
    def handle_key_press(self, event):
        print(f"Key pressed: {event.keysym}")
        self.next_word_key = self.next_word_key.strip("<>")
 
        # If a wrong key is pressed, register the timestamp and log the event.
        if event.keysym != self.key_press and event.keysym != self.next_word_key and event.keysym != "Return":
            self.wrong_key_timestamp = time.time()
            self.events.append(("Wrong key pressed", self.wrong_key_timestamp, None, None))
            print("Wrong key pressed event added.")
            
        # Then, if the button is visible and the correct key is pressed, trigger the reaction click.
        elif self.reaction_click_button.winfo_viewable() and event.keysym == self.key_press:
            print("Correct key pressed.")
            self.reaction_click()

    # the show_reaction_click_button function shows the reaction click button on the screen. 
    # The size and position of the button are determined based on the game settings. 
    # The button is placed at a fixed center position or at a random position within the game window. 
    # The button's appearance and start time are recorded as game events.
    def show_reaction_click_button(self):

        self.reaction_click_button.place_forget()
        
        if self.button_size == "large":
            button_width = 200
            button_height = 60
        elif self.button_size == "medium":
            button_width = 100
            button_height = 30
        elif self.button_size == "small":
            button_width = 50
            button_height = 15
        else:
            button_width = 100
            button_height = 30


        self.master.update()  # Add this line to update the widget before getting its width
        if self.fix_centre == 1:
            x = self.winfo_width() // 2 - button_width // 2
            y = self.winfo_height() // 2 - button_height // 2
        else:
            x = random.randint(0, max(0, self.winfo_width() - button_width))  # Use max to prevent negative values
            y = random.randint(0, max(0, self.winfo_height() - button_height))  # Use max to prevent negative values
        

        self.reaction_click_button.place(x=x, y=y, width=button_width, height=button_height)
        self.reaction_click_button.config(bg=self.button_color)
        self.reaction_click_button.config(fg=self.button_color)
        self.reaction_start_time = time.time()
        self.events.append(("Button shown", self.reaction_start_time, None, None))

    # The reaction_click method is called when the button is clicked. 
    # It calculates the reaction time, logs the button click event and the reaction time event, 
    # and resets the wrong key timestamp if applicable. The button is then hidden, and the next 
    # appearance of the button is scheduled.
    def reaction_click(self):
        print("Reaction click triggered.")
        current_time = time.time()
        reaction_time = current_time - self.reaction_start_time
        self.reaction_times.append(reaction_time)
        self.events.append(("Button clicked", current_time, reaction_time, None))
        self.events.append(("Reaction time", reaction_time, None, None))
        self.reaction_click_button.place_forget()
        self.schedule_reaction_click_button()

    # The get_key_press method returns the key that needs to be pressed to trigger the button click event.
    def get_key_press(self):
        return self.key_press    
 
  
 
