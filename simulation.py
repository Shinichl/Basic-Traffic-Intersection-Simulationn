import random
import time
import threading
import pygame
import sys

# Default values of signal timers
defaultGreen = {0: 10, 1: 10, 2: 10, 3: 10}
defaultRed = 45
defaultYellow = 5

signals = []
noOfSignals = 4
currentGreen = 0  # Indicates which signal is green currently
nextGreen = (currentGreen + 1) % noOfSignals  # Indicates which signal will turn green next
currentYellow = 0  # Indicates whether yellow signal is on or off

speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5}  # average speeds of vehicles

# Coordinates of vehicles' start positions
#x = {'right': [1, 1, 1], 'down': [510, 510, 540], 'left': [1000, 1000, 1000], 'up': [800, 430, 469]}
#y = {'right': [495, 430, 465], 'down': [180, 100, 190], 'left': [516, 516, 542], 'up': [914, 990, 900]}
x = {'right': [1, 1, 1], 'down': [800, 430, 469], 'left': [1000, 1000, 1000], 'up': [510, 510, 540]}
y = {'right': [516, 516, 542], 'down': [180, 100, 190], 'left': [495, 430, 465], 'up': [914, 990, 900]}
vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0}, 'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(360, 260), (590, 260), (585, 602), (365, 602)]
signalTimerCoods = [(419, 444), (520, 420), (532, 522), (453, 555)]

# Coordinates of stop lines
stopLines = {'right': 390, 'down': 400, 'left': 605, 'up': 600}
defaultStop = {'right': 380, 'down': 390, 'left': 615, 'up': 620}

# Gap between vehicles
stoppingGap = 10  # stopping gap
movingGap = 10  # moving gap

# Initialize pygame and sprite group
pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1

        # Load vehicle image with error handling
        try:
            path = "images/" + direction + "/" + vehicleClass + ".png"
            self.image = pygame.image.load(path)
        except pygame.error as e:
            print(f"Error loading image: {path}, {e}")
            self.image = pygame.Surface((50, 50))  # Default to a plain surface if image load fails

        # Determine stop position
        if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
            if direction == 'right':
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].image.get_rect().width - stoppingGap
            elif direction == 'left':
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].image.get_rect().width + stoppingGap
            elif direction == 'down':
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].image.get_rect().height - stoppingGap
            elif direction == 'up':
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]

        # Adjust start coordinates for new vehicle
        if direction == 'right':
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] -= temp
        elif direction == 'left':
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif direction == 'down':
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif direction == 'up':
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.direction == 'right':
            if self.crossed == 0 and self.x + self.image.get_rect().width > stopLines[self.direction]:
                self.crossed = 1
            if (self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (currentGreen == 0 and currentYellow == 0)) and (self.index == 0 or self.x + self.image.get_rect().width < (vehicles[self.direction][self.lane][self.index - 1].x - movingGap)):
                self.x += self.speed
        elif self.direction == 'down':
            if self.crossed == 0 and self.y + self.image.get_rect().height > stopLines[self.direction]:
                self.crossed = 1
            if (self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (currentGreen == 1 and currentYellow == 0)) and (self.index == 0 or self.y + self.image.get_rect().height < (vehicles[self.direction][self.lane][self.index - 1].y - movingGap)):
                self.y += self.speed
        elif self.direction == 'left':
            if self.crossed == 0 and self.x < stopLines[self.direction]:
                self.crossed = 1
            if (self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + movingGap)):
                self.x -= self.speed
        elif self.direction == 'up':
            if self.crossed == 0 and self.y < stopLines[self.direction]:
                self.crossed = 1
            if (self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][self.index - 1].image.get_rect().height + movingGap)):
                self.y -= self.speed
def initialize():
    """Initialize traffic signals with specified sequence."""
    totalCycleTime = sum(defaultGreen.values()) + defaultYellow * (noOfSignals - 1)

    # Create signals with correct red, yellow, green times
    for i in range(noOfSignals):
        green_time = 10  # All lights have a green time of 10 seconds
        yellow_time = 5   # All lights have a yellow time of 5 seconds
        red_time = totalCycleTime - (green_time + yellow_time)
        signal = TrafficSignal(red_time, yellow_time, green_time)
        signals.append(signal)

    # Set initial red times based on the specified sequence with a 2-second delay
    red_times = [45, 15, 15, 15]  # Initial red times for each signal
    delay = 2  # Delay before next light turns green after previous light turns red

    for i in range(noOfSignals):
        # Add the delay after the first light
        if i > 0:
            red_times[i] += delay

        signals[i].red = red_times[i]

    repeat() 

    
def repeat():
    """Continuously update the signal timers and manage transitions."""
    global currentGreen, currentYellow, nextGreen

    while True:
        updateValues()
        time.sleep(1)

def updateValues():
    """Update the timer values for each signal."""
    global currentGreen, currentYellow, nextGreen
    for i in range(noOfSignals):
        if i == currentGreen:
            if currentYellow == 0:
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1

    # If the green time for the current signal is over
    if signals[currentGreen].green == 0 and currentYellow == 0:
        currentYellow = 1
        signals[currentGreen].yellow = defaultYellow

    # If the yellow time for the current signal is over
    if currentYellow == 1 and signals[currentGreen].yellow == 0:
        currentYellow = 0
        currentGreen = nextGreen
        nextGreen = (currentGreen + 1) % noOfSignals

        # Set green time to the remaining time of the previous green signal
        signals[currentGreen].green = signals[currentGreen].red + signals[currentGreen].yellow
        signals[currentGreen].yellow = defaultYellow

        # Reset timers for the next signal
        for j in range(noOfSignals):
            signals[j].red = 15  # Start all red light timers at 15 seconds

        # Pause for 2 seconds before turning on the next red light
        time.sleep(2)

        # Add 15 seconds to the timer of the next green light
        signals[nextGreen].red += 15


def generateVehicles():
    """Generate vehicles randomly and add them to the simulation."""
    while True:
        vehicle_type = random.randint(0, 3)
        lane_number = random.randint(1, 2)
        temp = random.randint(0, 99)
        direction_number = 0
        dist = [25, 50, 75, 100]
        if temp < dist[0]:
            direction_number = 0
        elif temp < dist[1]:
            direction_number = 1
        elif temp < dist[2]:
            direction_number = 2
        elif temp < dist[3]:
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(1)

class Main:
    """Main class to handle the Pygame loop and rendering."""
    thread1 = threading.Thread(name="initialization", target=initialize)
    thread1.daemon = True
    thread1.start()

    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)

    screenWidth = 1000
    screenHeight = 1000
    screenSize = (screenWidth, screenHeight)

    try:
        background = pygame.image.load('images/intersection.png')
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        background = pygame.Surface((screenWidth, screenHeight))

    screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE) 
    pygame.display.set_caption("Traffic Light Simulation")

    try:
        redSignal = pygame.image.load('images/signals/red.png')
        yellowSignal = pygame.image.load('images/signals/yellow.png')
        greenSignal = pygame.image.load('images/signals/green.png')
        font = pygame.font.Font("digital.ttf", 30)
    except pygame.error as e:
        print(f"Error loading signal images or font: {e}")
        redSignal = yellowSignal = greenSignal = pygame.Surface((50, 50))
        font = pygame.font.SysFont(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles)
    thread2.daemon = True
    thread2.start()

    quit_font = pygame.font.Font("digital.ttf", 40)
    quit_surf = quit_font.render('Quit', True, 'white')
    quit_button = pygame.Rect(900, 10, 90, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(background, (0, 0))
        for i in range(noOfSignals):
            if i == currentGreen:
                if currentYellow == 1:
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                signals[i].signalText = signals[i].red
                screen.blit(redSignal, signalCoods[i])

            if 1 <= signals[i].signalText <= 10:
                signalColor = white
            else:
                signalColor = gray
            signalTexts = font.render(str(signals[i].signalText), True, signalColor, black)
            screen.blit(signalTexts, signalTimerCoods[i])

        for vehicle in simulation:  
            vehicle.render(screen)
            vehicle.move()

        d, c = pygame.mouse.get_pos()
        if quit_button.collidepoint(d, c):
            pygame.draw.rect(screen, (110, 90, 90), quit_button)
        else:
            pygame.draw.rect(screen, (250, 90, 90), quit_button)
        screen.blit(quit_surf, (quit_button.x + 14, quit_button.y + 8))

        pygame.display.update()

if __name__ == "__main__":
    Main()
