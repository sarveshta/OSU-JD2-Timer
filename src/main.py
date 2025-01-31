import time
from datetime import datetime
import pytz
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk

def countdown_timer():
    global time_left, timer_running, enable_night
    while time_left > 0 and timer_running:  # update clock while running and time remains
        update_timer_display()
        root.update_idletasks()  # update the ui clock
        time.sleep(1)  # update every sec
        time_left -= 1
    if time_left == 0 and timer_running:
        countdown_label.configure(text="Time is Up")
    timer_running = False


def update_timer_display():
    # implement countdown label funct to be manipulated by buttons
    hours, remainder = divmod(time_left, 3600)
    mins, secs = divmod(remainder, 60)
    countdown_label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")


def start_timer():
    global timer_running
# if timer start button pressed, and time > 0, update bool, run timer
    if not timer_running and time_left > 0:
        timer_running = True
        threading.Thread(target=countdown_timer, daemon=True).start()

def stop_timer():
    global timer_running
    timer_running = False  # if timer stop button is pressed, update bool


def increment_sec():
    global time_left
    time_left += 1  # add 1
    update_timer_display()

def increment_min():
    global time_left
    time_left += 60  # add 60
    update_timer_display()

def increment_hr():
    global time_left  # add 3600
    time_left += 3600
    update_timer_display()


def decrement_sec():
    global time_left
    if time_left > 1:  # if time is >1, subtract 1, else 0
        time_left -= 1
    else:
        time_left = 0
    update_timer_display()

def decrement_min():
    global time_left
    if time_left > 60:  # if time is >60, subtract 60, else 0
        time_left -= 60
    else:
        time_left = 0
    update_timer_display()

def decrement_hr():
    global time_left
    if time_left > 3600:  # if time is >3600, subtract 3600, else 0
        time_left -= 3600
    else:
        time_left = 0
    update_timer_display()

def dark_bright():
    global bright
    bright = 1  # set brightness to 1 (min value)
    print("dark mode")
def medium_bright():
     global bright
     bright = 2  # set brightness to 2 (middle value)
     print("medium bright")

def full_bright():
    global bright
    bright = 3  # set brightness to 3 (max value)
    print("full bright")


def night_mode():
    global bright, trigger_sound
    trigger_sound = False  # turn off sound device
    bright = 1  # set brightness to a minimum


def enable_NM():
    # if night mode enabled, change all backgrounds to gray18, foreground to green
    global enable_night
    if not enable_night:  # if night mode is off and user enables
        enable_night = True  # set to on, call night mode
        night_mode()
        style = ttk.Style()
        style.configure("TFrame", background="gray18")
        for widget in frm.winfo_children():  # see source list for making all backgrounds change
            if isinstance(widget, tk.Button):  # calls all except clock widgets to get changed to night mode
                widget.config(bg="gray18", fg="green")
    elif enable_night:  # if night mode is on and user enables
        enable_night = False  # set to on, call night mode
        style = ttk.Style()
        style.configure("TFrame", background="white")
        for widget in frm.winfo_children():
            if isinstance(widget, tk.Button):  # calls all except clock widgets to get changed to day mode
                widget.config(bg="white", fg="black")

    else:
        night_mode()  # backup case, should never be used

def clock():
    global RTclk
    if RTclk_label:
        # implement pacific time date and time from pytz
        pst = datetime.now(pytz.timezone('US/Pacific'))
        RTclk_label.config(text=f"{pst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        # update every second
    root.after(1000, clock)

def BrightnessUI():
    # creation of brightness page, management of button spacing
    global root3  # create a new frame to display brightness ui
    root3 = tk.Tk()
    frm3 = ttk.Frame(root3, padding = 50)
    frm3.grid()
    tk.Label(frm3, text="Set Brightness Level: ").grid(column=0, row=1)  # create label for brightness setting
    tk.Button(frm3, text="Dark", command=dark_bright).grid(column=0, row=2)  # create buttons for brightness settings
    tk.Button(frm3, text="Medium", command=medium_bright).grid(column=0, row=3)
    tk.Button(frm3, text="Bright", command=full_bright).grid(column=0, row=4)

def SettingsUI():
    # creation of timer page, management of button spacing
    global root2  # create a new frame to display settings ui
    root2 = tk.Tk()
    frm2 = ttk.Frame(root2, padding = 50)
    frm2.grid()
    tk.Label(frm2, text="Night Mode: ").grid(column=0, row=1)  # create buttons and labels for brightness settings
    tk.Button(frm2, text="ON/OFF", command=enable_NM).grid(column=1, row=1)
    tk.Label(frm2, text="Brightness: ").grid(column=0, row=2)
    tk.Button(frm2, text="Set", command=BrightnessUI).grid(column=1, row=2)
    tk.Button(frm2, text="Back", command=root2.destroy).grid(column=1, row=5)


def UI():
    # creation of timer page, management of button spacing
    global root, countdown_label, RTclk_label, frm
    root = tk.Tk()
    frm = ttk.Frame(root, padding=20)
    frm.grid()
    countdown_label = tk.Label(frm, text="00:00:00", font=("Times New Roman", 100))  # initial clock labels
    countdown_label.grid(column=0, row=1, columnspan=3)
    RTclk_label = tk.Label(frm, text="Loading...", font=("Times New Roman", 25))
    RTclk_label.grid(column=1, row=15, columnspan=1)
    clock()
    tk.Button(frm, text="-", command=decrement_sec).grid(column=2, row=2)  # arrangement of buttons and names
    tk.Button(frm, text="+", command=increment_sec).grid(column=2, row=0)
    tk.Button(frm, text="-", command=decrement_min).grid(column=1, row=2)
    tk.Button(frm, text="+", command=increment_min).grid(column=1, row=0)
    tk.Button(frm, text="-", command=decrement_hr).grid(column=0, row=2)
    tk.Button(frm, text="+", command=increment_hr).grid(column=0, row=0)
    tk.Button(frm, text="Start Timer", command=start_timer).grid(column=4, row=2)
    tk.Button(frm, text="Stop Timer", command=stop_timer).grid(column=4, row=3)
    tk.Button(frm, text="\u2699", command=SettingsUI).grid(column=5, row=0)
    root.mainloop()  # loop window until power off



# Main execution
def main():
    # list of global variables
    global root, time_left, bright, timer_running, present_object, trigger_sound, enable_night
    time_left = 0
    bright = 2
    timer_running = False
    present_object = True
    trigger_sound = False
    enable_night = False
    UI()  # run user interface command


if __name__ == "__main__":
    main()
