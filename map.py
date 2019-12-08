from PIL import Image, ImageTk
from stations import stations, station_ids
import serial.tools.list_ports
import threading, sys, os
import tkinter as tk
import serial
import time

port = None
baud_rate = 115200

img_width = 1160
img_height = 513

x_padding = 5
y_padding = 5
y_offset = 26

pos_x = 100
pos_y = 100
direction = 'n'

send_queue = []
if len(sys.argv) > 1:
    port = sys.argv[1]

if len(sys.argv) > 2:
    baud_rate = int(sys.argv[2])

def do_the_serial():
    global ser, send_queue, port
    if port is None:
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("No available COM port found. Aborting.")
            os._exit(1)
        print(f"Found: {' '.join(map(lambda p: p.device, ports))}")
        port = ports[0].device 

    print(f"Using {port} at {baud_rate} bits per second")
    
    ser = serial.Serial(port, baud_rate)

    while (ser.is_open):
        for i in send_queue:
            s = str(i).encode()
            ser.write(s)
            ser.write(0x0D)
            print(f"Sending: {s}")

        send_queue.clear()

        while (ser.in_waiting):
            l = ser.read()
            n = int(l[0])
            print(f"Received: {n}")
            set_station(n)

        time.sleep(0.01)

def set_station(n):
    global stations, station_ids, pos_x, pos_y, direction
    n = n - 1
    if n in station_ids:
        station = stations[n]
        pos_x = x_padding + station[0]
        pos_y = y_padding + station[1] - y_offset
        direction = station[2]

def go(n): 
    global send_queue
    send_queue.append(n)
    print(f"Going to: {n}")
    set_station(n)

def process_updates(root, state):
    global pos_x, pos_y, direction, ser, img_width, img_height
    canvas = tk.Canvas(root, width = img_width + 2 * x_padding, height = img_height + 2 * y_padding)
    canvas.pack()

    background = ImageTk.PhotoImage(file = "img/map.png")
    canvas.create_image(x_padding, y_padding, image = background, anchor="nw")

    btn_size = 32
    for i in range(1, 25):
        station = stations[i - 1]
        button = tk.Button(root, text = f"{i}", command = lambda n=i: go(n))
        button.place(x = x_padding + station[0], y = y_padding + station[1] - y_offset, anchor="center", height = btn_size, width = btn_size)

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
    pass