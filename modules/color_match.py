"""
Master Computing and Innovation
MCI-Projects-2023
Developing and application for cognitive research

Richard Hill (a1756449), Vahid Jahangirov (a1845737), Hanbo Pu (a1807267)

"""

import tkinter as tk
import random
import time

# The __init__ method initializes the game by setting up the necessary variables and widgets. 
# It takes the master window, the number of colors, screen width, and screen height as parameters. 
# It creates a frame with a specific width and height, sets up labels for the score and time, 
# and creates canvases for the color bar and color wheel. 
# It also generates a list of colors using the generate_colors method and creates color canvases on the color wheel for each color.
class ColorMatchGame(tk.Frame):
    def __init__(self, master, num_colors, screen_width, screen_height):
        self.width = screen_width // 2
        self.height = screen_height
        super().__init__(master, width=self.width, height=self.height)
        self.master = master
        self.colors = self.generate_colors(num_colors)
        self.num_colors = len(self.colors)
        self.score = 0
        self.time_start = time.time()
        self.events = []

        self.score_label = tk.Label(self)#, text=f"Score: {self.score}")
        self.score_label.pack(pady=10)

        self.time_label = tk.Label(self)#, text="Time: 0.0s")
        self.time_label.pack(pady=10)

        self.color_bar_width = int(0.999 * self.width)
        self.color_bar_height = int(0.1 * self.height)
        self.color_bar = tk.Canvas(self, width=self.color_bar_width, height=self.color_bar_height)
        self.color_bar.pack(padx=(20, 0), pady=(self.height - self.color_bar_height) // 8)

        self.color_wheel_width = int(0.999 * self.width)
        self.color_wheel_height = int(0.999 * self.height)
        self.color_wheel = tk.Canvas(self, width=self.color_wheel_width, height=self.color_wheel_height)
        self.color_wheel.pack()

        self.color_canvas_width = int(self.width / 12)
        self.color_canvas_height = int(self.height / 24)
        self.color_canvas_padding = int(self.width / 60)

        self.color_canvases = []
        for i, color in enumerate(self.colors):
            color_canvas = tk.Canvas(
                self.color_wheel,
                width=self.color_canvas_width,
                height=self.color_canvas_height,
                bg=color
            )
            x = (
                ((i % 5) * (self.color_canvas_width + self.color_canvas_padding))
                + (self.color_canvas_width / 2)
                + (2 * self.color_canvas_padding)
                + (self.width - self.color_wheel_width) / 2
                + (self.color_bar_width - self.color_wheel_width) / 2
            )
            y = (
                ((i // 5) * (self.color_canvas_height + self.color_canvas_padding))
                + (self.color_canvas_height / 2)
                + (2 * self.color_canvas_padding)
            )
            color_canvas.place(x=x, y=y, anchor="center")
            color_canvas.bind("<Button-1>", self.check_match)
            self.color_canvases.append(color_canvas)

        self.refresh_color()

    # The generate_colors method generates a list of random colors. 
    # It takes the number of colors as a parameter and generates random RGB values for each color. 
    # The colors are represented as hexadecimal strings and added to the colors list, which is then returned.
    def generate_colors(self, num_colors):
        colors = []
        for i in range(num_colors):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = f"#{r:02x}{g:02x}{b:02x}"
            colors.append(color)
        return colors

    # The refresh_color method selects a new color for the color bar. 
    # It removes the previous color from the color bar and selects a new color from the colors list. 
    # The new color is drawn on the color bar canvas, and the reaction start time is recorded.
    def refresh_color(self):
        self.color_bar.delete("all")
        prev_color = self.current_color if hasattr(self, "current_color") else None
        while True:
            self.current_color = random.choice(self.colors)
            if prev_color is None or self.current_color != prev_color:
                break
        self.color_bar.create_rectangle(0, 0, 300, 50, fill=self.current_color)
        self.reaction_start_time = time.time()
        self.events.append(("Button shown", self.reaction_start_time, None, None))

    # The check_match method is called when a color canvas is clicked. 
    # It compares the selected color with the current color displayed in the color bar. 
    # If they match, the score is incremented, the button clicked event is logged, a new color is selected, 
    # and the time is updated.
    def check_match(self, event):
        selected_color = event.widget["bg"]
        if self.current_color == selected_color:
            self.score += 1
            #self.score_label.config(text=f"Score: {self.score}")
            current_time = time.time()
            reaction_time = current_time - self.reaction_start_time
            self.events.append(("Button clicked", current_time, reaction_time, None))
            self.refresh_color()
            self.update_time()

    # The update_time method calculates and updates the elapsed time and reaction time labels. 
    # It calculates the elapsed time since the game started and the reaction time since the last color was displayed.
    def update_time(self):
        elapsed_time = time.time() - self.time_start
        #self.time_label.config(text=f"Time: {elapsed_time:.1f}s")
        reaction_time = elapsed_time - (self.reaction_start_time if hasattr(self, "reaction_start_time") else 0)
        self.events.append(("Reaction time", reaction_time, None, None))

