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
    global enable_night
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
    global timer_running, timer_stopped
    timer_running = False  # if timer stop button is pressed, update bool
    timer_stopped += 1
    print(timer_stopped)
    Timer_stop_count = tk.Label(frm, text="Timer Stops: " + str(timer_stopped)).grid(column=5, row=3)


def increment_sec():
    global time_left
    time_left += 1  # add 1
    update_timer_display()

def increaseTimeBy(time):
    for i in range(time):
        increment_sec()

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
    global bright, settings_menu
    bright = 1  # set brightness to 1 (min value)
    style = ttk.Style()
    style.configure("TFrame", background="gray26")
    for widget in frm.winfo_children():  # see source list for making all backgrounds change
        if isinstance(widget, tk.Button):  # calls all except clock widgets to get changed to night mode
            widget.config(bg="gray18", fg="gray45")
            countdown_label.config(bg="gray18", fg="gray45") #call the label update too
            RTclk_label.config(bg="gray18", fg="gray45")
            Timer_stop_count.config(bg="gray18", fg="gray45")
            #settings_menu.config(bg="gray18", fg="gray45")
def medium_bright():
     global bright, settings_menu
     bright = 2  # set brightness to 2 (middle value)
     style = ttk.Style()
     style.configure("TFrame", background="gray45")
     for widget in frm.winfo_children():  # see source list for making all backgrounds change
         if isinstance(widget, tk.Button):  # calls all except clock widgets to get changed to night mode
             widget.config(bg="gray45", fg="gray80") #updayte labels
             countdown_label.config(bg="gray45", fg="gray80")
             RTclk_label.config(bg="gray45", fg="gray80")
             Timer_stop_count.config(bg="gray45", fg="gray80")
            # settings_menu.config(bg="gray45", fg="gray80")

def full_bright():
    global bright, settings_menu
    style = ttk.Style()
    style.configure("TFrame", background="white")
    for widget in frm.winfo_children():  # see source list for making all backgrounds change
        if isinstance(widget, tk.Button):  # calls all except clock widgets to get changed to night mode
            widget.config(bg="white", fg="black") # update labels
            countdown_label.config(bg="white", fg="black")
            RTclk_label.config(bg="white", fg="black")
            Timer_stop_count.config(bg="white", fg="black")
            #settings_menu.config(bg="white", fg="black")


def night_mode():
    global bright, trigger_sound
    trigger_sound = False  # turn off sound device
    bright = 1  # set brightness to a minimum

def getNightMode():
    global enable_night
    return enable_night

def enable_NM():
    # if night mode enabled, change all backgrounds to gray18, foreground to green
    global enable_night
    if not enable_night:  # if night mode is off and user enables
        enable_night = True  # set to on, call night mode
        night_mode()
        dark_bright()
    elif enable_night:  # if night mode is on and user enables
        enable_night = False  # set to on, call night mode
        full_bright()
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

def SettingsUI():
    # creation of timer page, management of button spacing
      # create a window to display settings
    global settings_menu
    window_height = 400 # hardcode in height to match frame
    settings_menu = tk.Frame(root)
    settings_menu.place(x=475, y=0, height = window_height, width = 175)
    tk.Label(settings_menu, text="Night Mode: ").grid(column=0, row=1)  # create buttons and labels for brightness settings
    tk.Button(settings_menu, text="ON/OFF", command=enable_NM).grid(column=1, row=1)
    tk.Label(settings_menu, text="Brightness: ").grid(column=0, row=3)
    tk.Button(settings_menu, text="Dark", command=dark_bright).grid(column=1, row=3)  # create buttons for brightness settings
    tk.Button(settings_menu, text="Medium", command=medium_bright).grid(column=1, row=4)
    tk.Button(settings_menu, text="Bright", command=full_bright).grid(column=1, row=5)
    tk.Label(settings_menu, text="Return:").grid(column=0, row=6)
    tk.Button(settings_menu, text="Back", command=settings_menu.destroy).grid(column=1, row=6)



def UI():
    # creation of timer page, management of button spacing
    global root, countdown_label, RTclk_label, frm, timer_stopped, Timer_stop_count
    root = tk.Tk()
    frm = ttk.Frame(root, padding=100)
    frm.grid()
    countdown_label = tk.Label(frm, text="00:00:00", font=("Times New Roman", 100))  # initial clock labels
    countdown_label.grid(column=0, row=1, columnspan=3)
    RTclk_label = tk.Label(frm, text="Loading...", font=("Times New Roman", 25))
    RTclk_label.grid(column=1, row=15, columnspan=1)
    Timer_stop_count = tk.Label(frm, text="Timer Stops: " + str(timer_stopped))
    Timer_stop_count.grid(column=4, row=4)
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
    global time_left, bright, timer_running, present_object, trigger_sound, enable_night, timer_stopped
    timer_stopped = 0
    time_left = 0
    bright = 2
    timer_running = False
    present_object = True
    trigger_sound = False
    enable_night = False
    UI()  # run user interface command

def setTimerRunning(timerEnabled):
    global timer_running
    timer_running = timerEnabled

if __name__ == "__main__":
    main()