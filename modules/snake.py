import tkinter as tk
import time
import random
import sounddevice as sd
import numpy as np
import wavio

from PIL import Image, ImageTk
import random

import threading

# The __init__ function initializes the game by setting up the necessary variables and widgets. 
# It takes the master window, screen width, screen height, and cell size as parameters. 
# It creates a canvas with a specific width and height, sets the snake speed, initial snake positions, 
# and food position. It also binds the keyboard keys to the on_key_press method, loads the required images, 
# creates the snake and food objects on the canvas, and starts the game.
class SnakeGame(tk.Canvas): 
    def __init__(self, master, screen_width, screen_height, cell_size=20):
        self.width = screen_width // 2
        self.height = screen_height
        self.cell_size = cell_size
        super().__init__(master, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.snake_speed = 150
        self.snake_positions = [(50, 50), (40, 50), (30, 50), (20, 50)]
        self.food_position = self.get_random_food_position()
        self.direction = (10, 0)

        self.bind_all("<Key>", self.on_key_press)
        self.pack()
        self.load_assets()
        self.create_objects()
        self.start()

    # The load_assets function loads the snake body and food images from files and creates image objects using the Image and ImageTk modules.
    def load_assets(self):
        self.snake_body_image = Image.open("images/snake_body.png")
        self.snake_body = ImageTk.PhotoImage(self.snake_body_image.resize((self.cell_size, self.cell_size)))

        self.food_image = Image.open("images/food.png")
        self.food = ImageTk.PhotoImage(self.food_image.resize((self.cell_size, self.cell_size)))

    # The create_objects function creates the initial snake and food objects on the canvas. 
    # It creates image objects for the snake body and food using the loaded assets and places them at the specified positions.
    def create_objects(self):
        # self.create_text(
        #     self.width // 2, self.height // 2 - 50, text="Press any key to start", fill="#FFF", font=("Arial", 16), tag="start_text"
        # )

        for x, y in self.snake_positions:
            self.create_image(x, y, image=self.snake_body, tag="snake")

        x, y = self.food_position
        self.create_image(x, y, image=self.food, tag="food")

    # The start method starts the game loop by scheduling the perform_step method to be called 
    # after a specified delay (snake_speed).
    def start(self):
        self.after(self.snake_speed, self.perform_step)

    # The perform_step function is the main game loop. It updates the snake positions, 
    # checks for game over conditions, handles food consumption and snake growth, 
    # moves the snake on the canvas, and schedules the next step.
    def perform_step(self):
        self.snake_positions = self.get_new_snake_position()
        self.check_game_over()

        head_x, head_y = self.snake_positions[0]
        if (head_x, head_y) == self.food_position:
            self.food_position = self.get_random_food_position()
            self.snake_positions.append(self.snake_positions[-1])

        self.move_snake()
        self.after(self.snake_speed, self.perform_step)

    # on_key_press function handles the keypress events and updates the snake's direction 
    # based on the pressed key, while ensuring that the snake cannot reverse its direction.
    def on_key_press(self, e):
        key = e.keysym
        if key == "Up" and self.direction != (0, 10):
            self.direction = (0, -10)
        elif key == "Down" and self.direction != (0, -10):
            self.direction = (0, 10)
        elif key == "Left" and self.direction != (10, 0):
            self.direction = (-10, 0)
        elif key == "Right" and self.direction != (-10, 0):
            self.direction = (10, 0)

    # The move_snake function updates the snake's position on the canvas by 
    # deleting the previous snake objects and creating new ones at the updated positions.
    def move_snake(self):
        self.delete("snake")

        for x, y in self.snake_positions:
            self.create_image(x, y, image=self.snake_body, tag="snake")

        x, y = self.food_position
        self.coords("food", x, y)

    # The get_random_food_position method generates a random position for the food within 
    # the game grid by multiplying random integers with the cell size.
    def get_random_food_position(self):
        grid_width = max(self.width // self.cell_size, 3)
        grid_height = max(self.height // self.cell_size, 3)

        x = random.randrange(1, grid_width - 1) * self.cell_size
        y = random.randrange(1, grid_height - 1) * self.cell_size

        return (x, y)

    # The get_new_snake_position method calculates the new position of the snake's head 
    # based on the current direction and updates the snake's position list accordingly.
    def get_new_snake_position(self):
        head_x, head_y = self.snake_positions[0]
        new_head_x, new_head_y = head_x + self.direction[0], head_y + self.direction[1]
        return [(new_head_x, new_head_y)] + self.snake_positions[:-1]

    # The check_game_over method checks if the game is over by verifying if the snake's head has collided 
    # with the boundaries or its own body. If the game is over, it clears the canvas and displays a "Game Over" messag
    def check_game_over(self):
        head_x, head_y = self.snake_positions[0]
        if (
            head_x < 0
            or head_y < 0
            or head_x >= self.width
            or head_y >= self.height
            or (head_x, head_y) in self.snake_positions[1:]
        ):
            self.delete("all")
            self.create_text(
                self.width // 2, self.height // 2, text="Game Over", fill="#FFF", font=("Arial", 24)
            )