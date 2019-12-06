from PIL import Image, ImageTk
import tkinter as tk
import threading
import time

pos_x = 126
pos_y = 48
img = "square.png"

def do_the_serial():
    global pos_x
    while (True):
        # pos_x += 1
        time.sleep(1/60)
        pass

def process_updates(root, state):
    global pos_x, pos_y
    canvas = tk.Canvas(root, width=768, height=385)
    canvas.pack()

    background = ImageTk.PhotoImage(file="layout.jpg")
    canvas.create_image(0, 0, image=background, anchor="nw")
 
    t = threading.Thread(target=do_the_serial)
    t.start()

    while True:
        trainimg = ImageTk.PhotoImage(file=img)
        train = canvas.create_image(pos_x, pos_y, image=trainimg, anchor="center")
       
        root.after_idle(state["next"])
        yield
        canvas.delete(train)

def show():
    root = tk.Tk()
    root.title('ECED4402 - Assigment 3 - Map')
    state = {}
    state["next"] = process_updates(root, state).__next__

    root.after(1, state["next"])
    root.mainloop()

show()

