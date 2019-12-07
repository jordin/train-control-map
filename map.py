from PIL import Image, ImageTk
from stations import stations
import tkinter as tk
import threading
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


send_queue = []

def do_the_serial():
    global ser, send_queue
    ser = serial.Serial('COM3', 115200, timeout = 0)
        
    while (ser.is_open):
        for i in send_queue:
            ser.write(i)
            print(i)
        send_queue.clear()
        while (ser.in_waiting):
            l = ser.read()
            n = int(l[0])
            if (n >= 1 and n <= 24):
                set_station(n)
        time.sleep(1 / 60)

def set_station(n):
    global stations, pos_x, pos_y, direction
    station = stations[n - 1]
    pos_x = x_padding + station[0]
    pos_y = y_padding + station[1]
    direction = station[2]

def go(n): 
    global send_queue
    print(n)
    # send_queue.append()


def process_updates(root, state):
    global pos_x, pos_y, direction, ser, var
    # canvas = tk.Canvas(root, width = 1366, height = 768)
    canvas = tk.Canvas(root, width = 600, height = 200)
    canvas.pack()

    # background = ImageTk.PhotoImage(file = "img/map.png")
    # canvas.create_image(x_padding, y_padding, image = background, anchor="nw")

    button = tk.Button(root, text = "Go", command = go, args = (5,))
    button.pack()

    t = threading.Thread(target = do_the_serial)
    t.start()

    try:
        while True:
            trainimg = ImageTk.PhotoImage(file = f"img/train-{direction}.png")
            train = canvas.create_image(pos_x, pos_y, image = trainimg, anchor = "center")
        
            root.after_idle(state["next"])
            yield
            canvas.delete(train)
    except:
        ser.close()
   

def show():
    root = tk.Tk()
    root.title('ECED4402 - Assigment 3 - Map')
    # root.attributes("-fullscreen", True)
    state = {}
    state["next"] = process_updates(root, state).__next__

    root.after(1, state["next"])
    root.mainloop()

show()
# do_the_serial()