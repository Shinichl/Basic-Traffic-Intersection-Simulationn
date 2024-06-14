import random
import time
import threading
import pygame
import sys
import tkinter as tk

# Define global variables and constants

# Default values of signal timers
defaultGreen = {0: 10, 1: 10, 2: 10, 3: 10}
defaultRed = 150
defaultYellow = 5

# Other global variables...

# Initialize pygame
pygame.init()

# Define a function to toggle traffic lights
def toggleLights():
    global currentGreen, currentYellow, nextGreen, signals
    
    # Toggle the current green signal to red and vice versa
    signals[currentGreen].green = defaultGreen[currentGreen] if currentYellow == 0 else defaultYellow
    signals[currentGreen].red = defaultYellow if currentYellow == 0 else defaultRed
    currentYellow = 1 - currentYellow  # Toggle yellow status
    
    # Update current green and next green signals
    currentGreen = nextGreen
    nextGreen = (currentGreen + 1) % noOfSignals
    signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green  # Set next red time
    
    # Restart the timer loop
    repeat()

# Add a button to the tkinter window
root = tk.Tk()
button = tk.Button(root, text="Toggle Lights", command=toggleLights)
button.pack()

# Start the traffic light simulation
initialize()
root.mainloop()
