import time
from datetime import datetime
import pytz
import threading
import tkinter as tk
from tkinter import ttk

def countdown_timer():
    global time_left, timer_running
    while time_left > 0 and timer_running:
        update_timer_display()
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
    global timer_running, timer_stopped
    timer_running = False
    timer_stopped += 1
    stop_count_label.config(text=f"Timer Stops: {timer_stopped}")

def increment_sec():
    global time_left
    time_left += 1
    update_timer_display()

def increment_min():
    global time_left
    time_left += 60
    update_timer_display()

def increment_hr():
    global time_left
    time_left += 3600
    update_timer_display()

def decrement_sec():
    global time_left
    time_left = max(0, time_left - 1)
    update_timer_display()

def decrement_min():
    global time_left
    time_left = max(0, time_left - 60)
    update_timer_display()

def decrement_hr():
    global time_left
    time_left = max(0, time_left - 3600)
    update_timer_display()

def clock():
    pst = datetime.now(pytz.timezone('US/Pacific'))
    clock_label.config(text=f"{pst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    root.after(1000, clock)

def UI():
    global root, countdown_label, clock_label, stop_count_label
    root = tk.Tk()
    root.geometry("480x320")
    root.title("Raspberry Pi Timer")

    main_frame = ttk.Frame(root, padding=5)
    main_frame.pack(fill=tk.BOTH, expand=True)

    countdown_label = tk.Label(main_frame, text="00:00:00", font=("Arial", 40))
    countdown_label.grid(row=0, column=0, columnspan=4, pady=10)

    clock_label = tk.Label(main_frame, text="Loading...", font=("Arial", 14))
    clock_label.grid(row=1, column=0, columnspan=4, pady=5)

    stop_count_label = tk.Label(main_frame, text="Timer Stops: 0", font=("Arial", 12))
    stop_count_label.grid(row=2, column=0, columnspan=4, pady=5)
    
    # Timer controls
    tk.Button(main_frame, text="Start", command=start_timer, font=("Arial", 16)).grid(row=3, column=2, padx=5, pady=5, sticky='nsew')
    tk.Button(main_frame, text="Stop", command=stop_timer, font=("Arial", 16)).grid(row=3, column=3, padx=5, pady=5, sticky='nsew')

    # Increment/Decrement Time
    tk.Button(main_frame, text="+ Hr", command=increment_hr, font=("Arial", 16)).grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
    tk.Button(main_frame, text="+ Min", command=increment_min, font=("Arial", 16)).grid(row=4, column=1, padx=5, pady=5, sticky='nsew')
    tk.Button(main_frame, text="+ Sec", command=increment_sec, font=("Arial", 16)).grid(row=4, column=2, padx=5, pady=5, sticky='nsew')
    
    tk.Button(main_frame, text="- Hr", command=decrement_hr, font=("Arial", 16)).grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
    tk.Button(main_frame, text="- Min", command=decrement_min, font=("Arial", 16)).grid(row=5, column=1, padx=5, pady=5, sticky='nsew')
    tk.Button(main_frame, text="- Sec", command=decrement_sec, font=("Arial", 16)).grid(row=5, column=2, padx=5, pady=5, sticky='nsew')
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    clock()
    root.mainloop()

def main():
    global time_left, timer_running, timer_stopped
    time_left = 0
    timer_running = False
    timer_stopped = 0
    UI()

if __name__ == "__main__":
    main()