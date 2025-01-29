import time
from datetime import datetime
import pytz
import threading
#from tkinter import *
from tkinter import ttk
import tkinter as tk



def countdown_timer(t, enable_night):
    global time_left, timer_running

    while time_left > 0 and timer_running:
        hours, remainder = divmod(time_left, 3600)
        mins, secs = divmod(remainder, 60)
        timer_display = f"{hours:02d}:{mins:02d}:{secs:02d}"
        countdown_label.configure(text=f"Time Remaining: {timer_display}")
        root.update_idletasks()
        time.sleep(1)
        time_left -= 1

    if time_left == 0 and timer_running:
        countdown_label.configure(text="Study time complete!")

    timer_running = False

def start_timer():
    global timer_running
    if not timer_running and time_left > 0:
        timer_running = True
        threading.Thread(target=countdown_timer, daemon=True).start()


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
def update_timer_display():
    hours, remainder = divmod(time_left, 3600)
    mins, secs = divmod(remainder, 60)
    countdown_label.configure(text=f"Time Remaining: {hours:02d}:{mins:02d}:{secs:02d}")


# Function to set the timer
def time_set():
    while True:
        try:
            user_set = int(input("Set study timer in sec: "))
            if user_set > 0:
                return user_set
            else: #ensure positive ints only
                print("Please enter a positive number.")
        except ValueError: #deny non-numerical inputs
            print("Invalid input. Please enter a valid number.")

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
    enable_night = True
    bright = 1

def clock():
    time.sleep(5)
    while (1):
        aware = datetime.now(pytz.utc)
        pst = datetime.now(pytz.timezone('US/Pacific'))
        print('r', 'Date, Time', f'\r{pst}', end='')
        time.sleep(1)

def UI():

    root = Tk()
    frm = ttk.Frame(root, padding=500)
    frm.grid()
    ttk.Label(frm, text="Time Remaining").grid(column=0, row=1)
    ttk.Button(frm, text="Decrement time by 5", command=root.destroy).grid(column=1, row=10)
    ttk.Button(frm, text="Increment time by 5", command=root.destroy).grid(column=1, row=0)
    #ttk.Label(frm, text=countdown_timer(t, enable_night=False).grid(column=0, row=0))
    ttk.Button(frm, text="Stop Timer", command=root.destroy).grid(column=2, row=1)
    ttk.Button(frm, text="\u2699", command=root.destroy).grid(column=3, row=0)
    root.mainloop()


# Main execution block
def main():
    present_object = True
    trigger_sound = False
    enable_night = False
    countdown_label = tk.Label(root, text="Time Remaining: 00:00:00", font=("Arial", 14))
    UI()
    # if present_object:
    #     study_time = time_set()  # Get the user input for the timer
    #     countdown_timer_thread = threading.Thread(target=countdown_timer, args=(study_time, enable_night), daemon=True)
    #     countdown_timer_thread.start()
    #     countdown_timer_thread.join()
    bright = 2
    night_mode()
    brightness(bright)

    clock_thread = threading.Thread(target=clock, daemon=True)
    clock_thread.start()


if __name__ == "__main__":
    main()
