"""
Programmer: Jordin McEachern & Serge Toutsenko
Program: train machine map
Created on: 2019-12-06
File: map.py
Description: handles the gui and the serial connection
"""
from stations import stations, station_ids, station_offset
from PIL import Image, ImageTk
import serial.tools.list_ports
import threading, sys, os
import tkinter as tk
import serial
import time

port = None
baud_rate = 115200 # default baud rate

# map image dimensions
img_width = 1160
img_height = 513

# padding for map in the window
x_padding = 5
y_padding = 5

# fine-tuned positioning for the station buttons
y_offset = 26

# train position (initially off screen)
pos_x = -100
pos_y = -100
direction = 'n'

# pending outgoing messages
send_queue = []

# check for user-defined com port
if len(sys.argv) > 1:
    port = sys.argv[1]

# check for user-defined baud rate
if len(sys.argv) > 2:
    baud_rate = int(sys.argv[2])

# immediately prints a debug message
def log(msg):
    print(msg, flush=True)

# if required, dynamically find an available com port
# then uses serial to communicate to and from the train machine
def do_the_serial():
    global ser, send_queue, port
    if port is None: # dynamically find an available com port
        ports = serial.tools.list_ports.comports()
        if not ports: # no ports found
            log("No available COM port found. Aborting.")
            os._exit(1)
        log(f"Found: {' '.join(map(lambda p: p.device, ports))}")
        port = ports[0].device 

    log(f"Using {port} at {baud_rate} bits per second")
    
    # open desired serial port at the desired baud rate
    ser = serial.Serial(port, baud_rate)

    while (ser.is_open):
        # flush send queue
        for i in send_queue:
            s = str(i).encode()
            ser.write(s)
            ser.write(0x0D)
            log(f"Sending: {s}")

        send_queue.clear()

        # read in all data received
        while (ser.in_waiting):
            l = ser.read()
            n = int(l[0])
            log(f"Received: {n}")
            set_station(n)

        time.sleep(0.01)

    # ser.is_open = False
    # close application when serial port closes    
    os._exit(1)

# updates the map to reflect arriving at a station
def set_station(n):
    global stations, station_ids, pos_x, pos_y, direction
    n = n - 1 # station number n corresponds to station index n - 1
    if n in station_ids:
        station = stations[n] # (x, y, dir)
        pos_x = x_padding + station[0]
        pos_y = y_padding + station[1] - y_offset
        direction = station[2]

# queues a message to be sent via serial to indicate
# the next destination for the train machine
def go(n): 
    global send_queue, station_offset
    send_queue.append(n + station_offset)
    log(f"Going to: {n}")

# update the map window
def process_updates(root, state):
    global pos_x, pos_y, direction, ser, img_width, img_height
    # create window with appropriate size
    canvas = tk.Canvas(root, width = img_width + 2 * x_padding, height = img_height + 2 * y_padding)
    canvas.pack()

    background = ImageTk.PhotoImage(file = "img/map.png")
    canvas.create_image(x_padding, y_padding, image = background, anchor="nw")

    btn_size = 32

    # create buttons to choose the destination
    for i in range(1, 25):
        station = stations[i - 1]
        button = tk.Button(root, text = f"{i}", command = lambda n=i: go(n))
        button.place(x = x_padding + station[0], y = y_padding + station[1] - y_offset, anchor="center", height = btn_size, width = btn_size)

    # start serial thread
    t = threading.Thread(target = do_the_serial)
    t.daemon = True
    t.start()

    # start at station 1
    set_station(1)

    try:
        while True:
            # update train icon position
            trainimg = ImageTk.PhotoImage(file = f"img/train-{direction}.png")
            train = canvas.create_image(pos_x, pos_y, image = trainimg, anchor = "center")
        
            root.after_idle(state["next"])
            yield
            canvas.delete(train)
    except: # window closes (CONTROL+C or X button)
        # close serial port
        ser.close()
        os._exit(1)

# create the map window
def show():
    root = tk.Tk()
    root.title('ECED4402 - Assigment 3 - Map')
    # root.attributes("-fullscreen", True)
    state = {}
    state["next"] = process_updates(root, state).__next__

    root.after(1, state["next"])

    root.mainloop()

try:
    show()
except:
    os._exit(1)
