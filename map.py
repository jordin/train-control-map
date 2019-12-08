from PIL import Image, ImageTk
from stations import stations
import tkinter as tk
import threading
import serial
import time
import sys

img_width = 1160
img_height = 566

x_padding = (1366 - img_width) / 2
y_padding = 10

pos_x = 100
pos_y = 100
direction = 'n'

send_queue = []

if len(sys.argv) < 2:
    print("Please specify a COM port")
    exit()

def do_the_serial():
    global ser, send_queue
    print("starting com")
    
    ser = serial.Serial(f'COM{sys.argv[1]}', 115200)
   
    print("com works")
    while (ser.is_open):
        for i in send_queue:
            s = str(i).encode()
            ser.write(s)
            ser.write(13)
            print(f"send: {s}")
        send_queue.clear()
        while (ser.in_waiting):
            l = ser.read()
            n = int(l[0])
            print(f"recv {n}")
            if (n >= 1 and n <= 24):
                set_station(n)
        time.sleep(0.01)

def set_station(n):
    global stations, pos_x, pos_y, direction
    station = stations[n - 1]
    pos_x = x_padding + station[0]
    pos_y = y_padding + station[1]
    direction = station[2]

def go(n): 
    global send_queue, drop_down
    send_queue.append(n)
    print(f"Q {n}")
    # set_station(n)

def process_updates(root, state):
    global pos_x, pos_y, direction, ser
    canvas = tk.Canvas(root, width = 1366, height = 768)
    canvas.pack()

    background = ImageTk.PhotoImage(file = "img/map.png")
    canvas.create_image(x_padding, y_padding, image = background, anchor="nw")

    for i in range(1, 25):
        station = stations[i - 1]
        button = tk.Button(root, text = f"{i}", command = lambda n=i: go(n))
        button.place(x = x_padding + station[0], y = y_padding + station[1], anchor="n")

    t = threading.Thread(target = do_the_serial)
    t.daemon = True
    t.start()
    set_station(1)
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
    global drop_down
    root = tk.Tk()
    root.title('ECED4402 - Assigment 3 - Map')
    # root.attributes("-fullscreen", True)

    """
    drop_down = tk.StringVar(root)
    drop_down.set("1")
    option = tk.OptionMenu(root, drop_down, "1", "2", "3", "4")
    option.pack()
    button = tk.Button(root, text = "Go!", command = go)
    button.pack()
    """
    state = {}
    state["next"] = process_updates(root, state).__next__

    root.after(1, state["next"])

    
    root.mainloop()

try:
    show()
except:
    pass