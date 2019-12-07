from PIL import Image, ImageTk
import tkinter as tk
import threading
from stations import stations
import serial
import time

img_width = 1160
img_height = 566

x_padding = (1366 - img_width) / 2
y_padding = 10

x_coord = -5.33
y_coord = -0.5

pos_x = -100
pos_y = -100
direction = 'n'

print(stations[0])

def do_the_serial():
    ser = serial.Serial('COM3', 115200, timeout = 0)
        
    while (ser.is_open):
        print(ser.readline())
        time.sleep(1/60)

def set_station(n):
    global stations, pos_x, pos_y, direction
    station = stations[n]
    pos_x = x_padding + station[0]
    pos_y = y_padding + station[1]
    direction = station[2]

def process_updates(root, state):
    global pos_x, pos_y, direction
    canvas = tk.Canvas(root, width = 1366, height = 768)
    canvas.pack()

    background = ImageTk.PhotoImage(file = "img/map.png")
    canvas.create_image(x_padding, y_padding, image = background, anchor="nw")
 
    t = threading.Thread(target = do_the_serial)
    t.start()

    while True:
        trainimg = ImageTk.PhotoImage(file = f"img/train-{direction}.png")
        train = canvas.create_image(pos_x, pos_y, image = trainimg, anchor = "center")
       
        root.after_idle(state["next"])
        yield
        canvas.delete(train)

def show():
    root = tk.Tk()
    root.title('ECED4402 - Assigment 3 - Map')
    # root.attributes("-fullscreen", True)
    state = {}
    state["next"] = process_updates(root, state).__next__

    root.after(1, state["next"])
    root.mainloop()

show()

