import tkinter as tk
import os
import threading
import time

def open_simulation():
    os.system("python simulation.py")

def close_app():
    root.destroy()

def simulate_traffic_light():
    # Simulate traffic light
    for _ in range(20):  # Example simulation loop
        time.sleep(1)
        print("Simulating traffic light...")

def unblur_simulation():
    root.attributes('-alpha', 1.0)  # Unblur the simulation window

def start_simulation():
    t1 = threading.Thread(target=simulate_traffic_light)
    t1.start()
    t2 = threading.Thread(target=unblur_simulation)
    t2.start()

root = tk.Tk()
root.title("Homepage")

# Create buttons
btn_open_simulation = tk.Button(root, text="Open Simulation", command=open_simulation)
btn_open_simulation.pack(pady=10)

btn_start_simulation = tk.Button(root, text="Start Simulation", command=start_simulation)
btn_start_simulation.pack(pady=10)

btn_close_app = tk.Button(root, text="Close Application", command=close_app)
btn_close_app.pack(pady=10)

# Embed simulation window (Replace 'simulation.py' with your simulation script)
simulation_frame = tk.Frame(root, width=800, height=600)
simulation_frame.pack(pady=20)

root.attributes('-alpha', 0.3)  # Initial blur effect

root.mainloop()
