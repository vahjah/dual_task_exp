import tkinter as tk
import time
import random
import sounddevice as sd
import numpy as np
import wavio
import csv
import yaml
import os

try:
    import whisper as wp
    whisper_available = True
except ImportError:
    whisper_available = False


from PIL import Image, ImageTk
import random

import threading

import modules.snake as snake
from modules.color_match import ColorMatchGame
from modules.reaction_click import ReactionClickGame


# The DualTaskExperiment that inherits from tk.Tk - Tkinter library
# this provides a graphical user interface (GUI) library.
class DualTaskExperiment(tk.Tk):
    
    #The class constructor (__init__) initializes attributes and sets up the UI for the dual task experiment. 
    #It takes parameters, including master, word_list, settings_list, experiment_name, num_words, and game_type. 
    #It also creates a directory for output files based on the experiment name.
    def __init__(self, master, word_list, settings_list, experiment_name, num_words=5, game_type="click"): 
       
        self.master = master
        self.game_type = game_type
        self.experiment_name = experiment_name
        # Create a directory for output
        self.output_dir = self.create_output_directory(experiment_name)  
        #window parameters
        self.primary_task_left = True
        

        #primary task parameters
        self.word_list = word_list
        self.num_words = num_words
        self.word_index = 0
        self.start_time = time.time()
        self.word_times = []
        
        self.settings_list = settings_list

        # this code opens the YAML file so can assign the information to the variables
        with open(self.settings_list) as file:
            self.config = yaml.safe_load(file)

        # the below assigns values from the YAML file to variables
        self.window_settings = self.config['window_settings'] 
        self.next_word_key = self.window_settings['next_word_key']
        self.welcome_message = self.window_settings['Welcome_message']
        self.break_after = self.window_settings['break_after']
        
        self.color_match_settings = self.config['color_match_settings']
        self.num_colors = self.color_match_settings['num_colors']


        self.recording = None
        self.samplerate = 44100
        self.first_space_key_press = False
        # Call the 'setup_ui' method to set up the user interface
        self.setup_ui()
        self.on_break = False
        self.intro_message = None
        self.master.bind('<Return>', self.start_experiment)
        self.master.bind('t', self.show_break_message)

    # The setup_game method sets up the game based on the game_type provided. 
    # It creates different game objects (ReactionClickGame, RedButtonGame, ColorMatchGame, SnakeGame) 
    # within the game_frame based on the specified type.
    def setup_game(self):
        self.game_frame_width = self.game_frame.winfo_width()
        self.game_frame_height = self.game_frame.winfo_height()

        
        if self.game_type == "color_match":
            self.setup_color_match_game()
        elif self.game_type == "snake":
            self.setup_snake_game()

    # The setup_ui method configures the main window and creates two frames (game_frame and word_frame) 
    # uses the Grid manager. It also sets up the initial welcome message and hides the game and word frames.
    def setup_ui(self):

        self.reaction_click_settings = self.config['word_settings']
        self.word_size = self.reaction_click_settings['word_size']

        self.master.title(self.experiment_name)

        # Set the window size to the screen size
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")

        # Make the window full screen
        #self.master.attributes('-fullscreen', True)  #**comment out if this line crashes in freeze build**
        self.master.bind('<Escape>', lambda e: self.master.quit())  

        # Create two equally sized frames using the Grid manager
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        message = self.welcome_message
        self.intro_message = tk.Label(self.master, text=message, font=("Arial", 24), wraplength=900)
        self.intro_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.game_frame = tk.Frame(self.master, bg="#D8D8D8", width=screen_width//2, height=screen_height)
        self.game_frame.grid(row=0, column=1, sticky="nsew")
        self.game_frame.grid_propagate(False)  # Prevent child widgets from affecting frame size

        self.word_frame = tk.Frame(self.master, bg="#F0F0F0", width=screen_width//2, height=screen_height)
        self.word_frame.grid(row=0, column=0, sticky="nsew")
        self.word_frame.grid_propagate(False)  # Prevent child widgets from affecting frame size

        self.word_label = tk.Label(self.word_frame, text="", font=("Arial", self.word_size), bg="#F0F0F0")
        self.word_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.setup_game()
        self.game_frame.grid_remove()
        self.word_frame.grid_remove()

    # The show_break_message fuction creates a pop-up window
    # to display a message during breaks 
    def show_break_message(self, event=None):
        
        break_window = tk.Toplevel(self.master)
        break_window_width = int(self.master.winfo_screenwidth() / 2)
        break_window_height = int(self.master.winfo_screenheight() / 2)
        break_window.geometry(f"{break_window_width}x{break_window_height}")
        break_window.resizable(False, False)
        break_window.title("Take a Break")
        break_label = tk.Label(break_window, text="Time for a break, press any key to continue",font=("Arial", 25),wraplength=400)
        break_label.pack(padx=20,pady=100)
        
        # close the break_window and resume the experiment when any key is pressed
        break_window.bind("<Key>", lambda event: break_window.destroy())
        break_window.focus_set()

    # The show_finish_message function creates a pop-up windows 
    # to display when the experiment is finished
    def show_finish_message(self):
        
        finish_window = tk.Toplevel(self.master)
        finish_window_width = int(self.master.winfo_screenwidth())
        finish_window_height = int(self.master.winfo_screenheight())
        finish_window.geometry(f"{finish_window_width}x{finish_window_height}")
        finish_window.title("Finished")
        finish_window.attributes('-fullscreen', True)
        finish_label = tk.Label(finish_window, text="Thank you for completing the experiment, press enter to return to the main menu",font=("Arial", 25))
        finish_label.pack(padx=20,pady=200)
        finish_window.bind("<Return>", lambda event: self.master.destroy())
        finish_window.focus_set()
    
    # The start_experiment method is triggered when the user presses the Enter key. 
    # It starts recording audio and shows the game and word frames based on the configuration. 
    # It also binds the next word key to the show_next_word method.
    def start_experiment(self, event=None):
        if self.intro_message:
            self.intro_message.destroy()  # Remove the introductory message
            self.intro_message = None

        self.start_recording()
        
        if self.on_break:
            self.on_break = False  # End the break
        else:
            self.start_recording()  # Start recording

        self.frame_settings = self.config['window_settings']
        self.primary_task_side = self.frame_settings['p_task_side']

        if self.primary_task_side == "left":
            game_frame_column = 1
            word_frame_column = 0
        elif self.primary_task_side == "right":
            game_frame_column = 0
            word_frame_column = 1

        # Show the game and word frames
        self.game_frame.grid(row=0, column=game_frame_column, sticky="nsew")
        self.word_frame.grid(row=0, column=word_frame_column, sticky="nsew")
        self.master.bind(self.next_word_key, self.show_next_word)     
    
    # The setup_reaction_click_game, setup_red_button_game, setup_snake_game, 
    # and setup_color_match_game methods create game objects specific to each game type 
    # and pack them into the game_frame.
    def setup_reaction_click_game(self):
        reaction_game = ReactionClickGame(self.game_frame, config=self.config,
                                          screen_width=self.master.winfo_screenwidth(),
                                          screen_height=self.master.winfo_screenheight())
        self.reaction_click_game = reaction_game
        self.reaction_click_game.pack(fill=tk.BOTH, expand=True)
        
    def setup_snake_game(self):
        snake_game_obj = snake.SnakeGame(self.game_frame, screen_width=self.master.winfo_screenwidth(), screen_height=self.master.winfo_screenheight())
        self.snake_game = snake_game_obj
        self.snake_game.pack(fill=tk.BOTH, expand=True)

    def setup_color_match_game(self):
        #num_colors = self.num_colors
        color_game_obj = ColorMatchGame(self.game_frame, self.num_colors, screen_width=self.master.winfo_screenwidth(), screen_height=self.master.winfo_screenheight())
        self.color_match_game = color_game_obj
        self.color_match_game.pack(fill=tk.BOTH, expand=True)
    
    # The show_next_word method updates the word label with the next word from the word list. 
    # It also records the time between words and handles breaks and the end of the experiment.
    def show_next_word(self, event):
        if self.game_type == "reaction_click" and not self.first_space_key_press:
            self.setup_reaction_click_game()
            self.first_space_key_press = True


        if self.word_index < self.num_words:
            self.word_label.config(text=self.word_list[self.word_index])
            current_time = time.time()
            self.word_times.append(current_time - self.start_time)
            self.start_time = current_time
            if self.game_type == "reaction_click":
                self.reaction_click_game.events.append(("New word shown", current_time, None, self.word_list[self.word_index]))
            elif self.game_type == "red_button":
                self.red_button_game.events.append(("New word shown", current_time, None, self.word_list[self.word_index]))
            elif self.game_type == "color_match":
                self.color_match_game.events.append(("New word shown", current_time, None, self.word_list[self.word_index]))
            self.word_index += 1
  
        if self.word_index == self.break_after and not self.on_break:
            self.game_frame.grid_remove()
            self.word_frame.grid_remove()
            self.on_break = True
            self.show_break_message()
            return

        elif self.word_index == self.num_words:
            # If the user has already been shown all the words, show "Finished!" when they press to see the next word
            # self.reaction_click_game.events.append(("New word shown", current_time, None, self.word_list[self.word_index]))
            self.word_index += 1
        elif self.word_index == self.num_words + 1:
            # If the user presses to see the next word after all the words have been shown and "Finished!" has been displayed, show the finish message
            self.show_finish_message()
            print("Times between words:", [self.word_times[i] - self.word_times[i - 1] for i in range(1, len(self.word_times))])
            if self.game_type != "snake":  
                self.stop_recording_and_save()
                self.export_events_to_csv() 

    
    # The start_recording method starts recording audio using the sounddevice library.
    def start_recording(self):
        self.recording = sd.rec(int(self.samplerate * 100 * self.num_words), samplerate=self.samplerate, channels=1, blocking=False)

    # The stop_recording_and_save method stops the audio recording and saves the recording as a WAV file.
    def stop_recording_and_save(self):
        sd.stop()
        self.save_recording()

    # The create_output_directory method creates a directory for the experiment's output files.
    def create_output_directory(self, directory_name):
        
        # Create a directory called "Reports" that will host all files for differnet experiments
        reports_directory_path = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_directory_path, exist_ok=True)

        # Create a sub-directory under "Reports" based on user input for experiment name
        directory_path = os.path.join(reports_directory_path, directory_name)

        if os.path.exists(directory_path):
            suffix = 1
            new_directory_path = directory_path + f"_{suffix}"
            
            while os.path.exists(new_directory_path):
                suffix += 1
                new_directory_path = directory_path + f"_{suffix}"

            directory_path = new_directory_path

        os.makedirs(directory_path, exist_ok=True)
        return directory_path

    # The save_recording method normalizes the recorded audio, 
    # saves it as a WAV file, and calls the transcribe_audio 
    # method to transcribe the audio into text.
    def save_recording(self):
        if self.recording is not None:
            
            self.recording = self.recording / np.max(np.abs(self.recording))

            filename = "whole_session_audio.wav"  
            filepath = os.path.join(self.output_dir, filename)  
            wavio.write(filepath, self.recording, self.samplerate, sampwidth=2)
            print(f"Audio saved as {filename}")
            print(f"saved here {filepath}")

            self.transcribe_audio(filepath) 
    
    # The transcribe_audio method transcribes the audio using the Whisper ASR (Automatic Speech Recognition) library 
    # if available. It saves the transcription as a text file.
    def transcribe_audio(self, audio_file):
        #audio_file=audio_file
        print(f"Received by call {audio_file}")
        def transcribe():
            if whisper_available:
                model = wp.load_model("base")
                print("Transcribing audio...")
                result = model.transcribe(audio_file)
                print("Transcription successful!")
                text = result["text"]

                transcription_filename = "transcription.txt"
                transcription_filepath = os.path.join(self.output_dir, transcription_filename) 
                with open(transcription_filepath, "w") as f:
                    f.write(text)
                print("Transcription saved as transcription.txt")
            else:
                print("Warning: whisper module is not available. Skipping transcription.")

        # transcription performed in seperate thread for performance 
        thread = threading.Thread(target=transcribe)
        thread.start()

    # The export_events_to_csv method exports the events that occurred during the experiment to a CSV file.
    def export_events_to_csv(self):  
        if self.game_type == "reaction_click":
            events = self.reaction_click_game.events
        elif self.game_type == "red_button":
            events = self.red_button_game.events
        elif self.game_type == "color_match":
            events = self.color_match_game.events

        print("Events:", events)

        csv_filename = 'events.csv'
        csv_filepath = os.path.join(self.output_dir, csv_filename)
        with open(csv_filepath, 'w', newline='') as csvfile:
            fieldnames = ['Event', 'Timestamp', 'Reaction Time', 'Word']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for event_data in events:
                event, timestamp = event_data[:2]
                if event not in ["Button clicked", "New word shown", "Button shown", "Wrong key pressed"]:
                    continue
                reaction_time = event_data[2] if event == "Button clicked" else None
                word = event_data[3] if event == "New word shown" else None
                wrong_key = event_data[2] if event == "Wrong key pressed" else None
                writer.writerow({'Event': event, 'Timestamp': timestamp, 'Reaction Time': reaction_time, 'Word': word})

        print("Events exported to events.csv")

    # The increment_click_count method increments a click count attribute and updates the corresponding label.
    def increment_click_count(self):
        self.click_count += 1
        self.click_label.config(text=f"Clicks: {self.click_count}")
