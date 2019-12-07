from PIL import Image, ImageTk
import tkinter as tk
import threading
import time
import serial

img_width = 1160
img_height = 566

x_padding = (1366 - img_width) / 2
y_padding = 10

x_coord = -5.33
y_coord = -0.5

pos_x = x_padding + 217
pos_y = y_padding + 496
direction = "w"

def do_the_serial():
    global pos_x
    ser = serial.Serial('COM3', 115200, timeout = 0)
    
    while (ser.is_open):
        print(ser.readline())
        # pos_x += 1
        time.sleep(1/60)
        pass

def process_updates(root, state):
    global pos_x, pos_y
    canvas = tk.Canvas(root, width = 1366, height = 768)
    canvas.pack()

    background = ImageTk.PhotoImage(file = "img/map.png")
    canvas.create_image(x_padding, y_padding, image=background, anchor="nw")
 
    t = threading.Thread(target=do_the_serial)
    t.start()

    while True:
        trainimg = ImageTk.PhotoImage(file = f"img/train-{direction}.png")
        train = canvas.create_image(pos_x, pos_y, image=trainimg, anchor="center")
       
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

