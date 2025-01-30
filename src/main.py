import time
from datetime import datetime
import pytz
import threading
from tkinter import *
from tkinter import ttk
import tkinter as tk


global root
def countdown_timer():
    global time_left, timer_running, enable_night
    while time_left > 0 and timer_running:
        hours, remainder = divmod(time_left, 3600)
        mins, secs = divmod(remainder, 60)
        timer_display = f"{hours:02d}:{mins:02d}:{secs:02d}"
        countdown_label.config(text=f"{timer_display}")
        root.update_idletasks()
        time.sleep(1)
        time_left -= 1

    if time_left == 0 and timer_running:
        countdown_label.configure(text="Time is Up")

    timer_running = False


def update_timer_display():

    hours, remainder = divmod(time_left, 3600)
    mins, secs = divmod(remainder, 60)
    countdown_label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")


def start_timer():
    global timer_running
    if not timer_running and time_left > 0:
        timer_running = True
        threading.Thread(target=countdown_timer, daemon=True).start()

def stop_timer():
    global timer_running
    timer_running = False


def increment_time():
    global time_left
    time_left += 5
    update_timer_display()

def decrement_time():
    global time_left
    if time_left > 5:
        time_left -= 5
    else:
        time_left = 0
    update_timer_display()




def brightness(bright):
        if bright == 1:
            print("Low brightness enabled.")
        elif bright == 2:
            print("Medium brightness enabled.")
        elif bright == 3:
            print("High brightness enabled.")
        else:
            print("Invalid input. Please enter 1, 2, or 3.")


def night_mode():
    global enable_night
    enable_night = True
    bright = 1

def clock():
    global RTclk
    if RTclk_label:
        pst = datetime.now(pytz.timezone('US/Pacific'))
        RTclk_label.config(text=f"{pst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    root.after(1000, clock)

def UI():
    global root, countdown_label, RTclk_label
    root = tk.Tk()
    frm = ttk.Frame(root, padding=500)
    frm.grid()
    countdown_label = ttk.Label(frm, text="00:00:00", font=("Times New Roman", 20))
    countdown_label.grid(column=1, row=1, columnspan=1)
    RTclk_label = ttk.Label(frm, text="Loading...", font=("Times New Roman", 10))
    RTclk_label.grid(column=1, row=15, columnspan=1)
    clock()
    ttk.Label(frm, text="Time Remaining").grid(column=0, row=1)
    ttk.Button(frm, text="Decrement time by 5", command=decrement_time).grid(column=1, row=2)
    ttk.Button(frm, text="Increment time by 5", command=increment_time).grid(column=1, row=0)
    ttk.Button(frm, text="Start Timer", command=start_timer).grid(column=3, row=1)
    ttk.Button(frm, text="Stop Timer", command=stop_timer).grid(column=3, row=2)
    ttk.Button(frm, text="\u2699", command=root.destroy).grid(column=5, row=0)
    root.mainloop()


# Main execution block
def main():
    global time_left
    time_left = 0
    global timer_running
    timer_running = False
    present_object = True
    trigger_sound = False
    global enable_night
    enable_night = False
    UI()
    bright = 2
    night_mode()
    brightness(bright)


if __name__ == "__main__":
    main()
