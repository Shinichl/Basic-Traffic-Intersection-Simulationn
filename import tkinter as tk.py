import tkinter as tk

class TrafficLightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Light")

        self.canvas = tk.Canvas(root, width=100, height=300, bg='black')
        self.canvas.grid(row=0, column=0)

        # Draw the traffic lights
        self.red_light = self.canvas.create_oval(20, 20, 80, 80, fill='gray')
        self.green_light = self.canvas.create_oval(20, 220, 80, 280, fill='gray')

        self.current_light = 'red'
        self.canvas.itemconfig(self.red_light, fill='red')

        # Button to toggle the traffic light
        self.toggle_button = tk.Button(root, text="Toggle Light", command=self.toggle_light)
        self.toggle_button.grid(row=1, column=0)

    def toggle_light(self):
        if self.current_light == 'red':
            self.canvas.itemconfig(self.red_light, fill='gray')
            self.canvas.itemconfig(self.green_light, fill='green')
            self.current_light = 'green'
        else:
            self.canvas.itemconfig(self.red_light, fill='red')
            self.canvas.itemconfig(self.green_light, fill='gray')
            self.current_light = 'red'


