import time
from datetime import datetime
import pytz
import threading
import tkinter as tk
from tkinter import ttk

# Global variables (preserved from original code)
time_left = 0
timer_running = False
timer_stopped = 0
bright = 2
present_object = True
trigger_sound = False
enable_night = False
confidence_threshold = 20

# Global widget references
root = None
frm = None
RTclk_label = None
hour_label = None
minute_label = None
second_label = None
Timer_stop_count = None
confidence_label = None
timer_spacers = []  # new global list for spacer labels

def countdown_timer():
    global time_left, timer_running
    while time_left > 0 and timer_running:
        update_timer_display()
        root.update_idletasks()
        time.sleep(1)
        time_left -= 1
    if time_left == 0 and timer_running:
        # When timer expires, display "Time is Up" split across the three labels
        hour_label.configure(text="Time")
        minute_label.configure(text="is")
        second_label.configure(text="Up")
    timer_running = False

def update_timer_display():
    hours, remainder = divmod(time_left, 3600)
    mins, secs = divmod(remainder, 60)
    # Update the three labels with two-digit formatting
    hour_label.config(text=f"{hours:02d}")
    minute_label.config(text=f"{mins:02d}")
    second_label.config(text=f"{secs:02d}")

def start_timer():
    global timer_running
    if not timer_running and time_left > 0:
        timer_running = True
        threading.Thread(target=countdown_timer, daemon=True).start()

def stop_timer():
    global timer_running, timer_stopped
    timer_running = False
    timer_stopped += 1
    print(timer_stopped)
    Timer_stop_count.config(text="Timer Stops: " + str(timer_stopped))

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
    if time_left > 1:
        time_left -= 1
    else:
        time_left = 0
    update_timer_display()

def decrement_min():
    global time_left
    if time_left > 60:
        time_left -= 60
    else:
        time_left = 0
    update_timer_display()

def decrement_hr():
    global time_left
    if time_left > 3600:
        time_left -= 3600
    else:
        time_left = 0
    update_timer_display()

def increaseTimeBy(time_delta):
    global time_left
    time_left += time_delta
    update_timer_display()

def dark_bright():
    global bright, timer_frame
    bright = 1
    style = ttk.Style()
    style.configure("TFrame", background="gray26")

    # Update all buttons in the main frame
    for widget in frm.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg="gray18", fg="gray45")

    # Update timer digit labels and other labels
    hour_label.config(bg="gray26", fg="gray45")
    minute_label.config(bg="gray26", fg="gray45")
    second_label.config(bg="gray26", fg="gray45")
    RTclk_label.config(bg="gray26", fg="gray45")
    Timer_stop_count.config(bg="gray26", fg="gray45")

    if confidence_label:
        confidence_label.config(bg="gray26", fg="gray45")

    # Update static colons, increment/decrement buttons, and spacers
    for widget in timer_frame.winfo_children():
        if isinstance(widget, tk.Label):  # This includes colons and spacers
            widget.config(bg="gray26", fg="gray45")
        elif isinstance(widget, tk.Button):  # Includes + and - buttons
            widget.config(bg="gray18", fg="gray45")

    # Update spacer labels separately to be sure:
    for spacer in timer_spacers:
        spacer.config(bg="gray26", fg="gray45")

def medium_bright():
    global bright, timer_frame
    bright = 2
    style = ttk.Style()
    style.configure("TFrame", background="gray45")

    for widget in frm.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg="gray45", fg="gray80")

    hour_label.config(bg="gray45", fg="gray80")
    minute_label.config(bg="gray45", fg="gray80")
    second_label.config(bg="gray45", fg="gray80")
    RTclk_label.config(bg="gray45", fg="gray80")
    Timer_stop_count.config(bg="gray45", fg="gray80")

    if confidence_label:
        confidence_label.config(bg="gray45", fg="gray80")

    # Update static colons, increment/decrement buttons, and spacers
    for widget in timer_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg="gray45", fg="gray80")
        elif isinstance(widget, tk.Button):
            widget.config(bg="gray45", fg="gray80")

    for spacer in timer_spacers:
        spacer.config(bg="gray45", fg="gray80")

def full_bright():
    global bright, timer_frame
    bright = 3
    style = ttk.Style()
    style.configure("TFrame", background="white")

    for widget in frm.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg="white", fg="black")

    hour_label.config(bg="white", fg="black")
    minute_label.config(bg="white", fg="black")
    second_label.config(bg="white", fg="black")
    RTclk_label.config(bg="white", fg="black")
    Timer_stop_count.config(bg="white", fg="black")

    if confidence_label:
        confidence_label.config(bg="white", fg="black")

    # Update static colons, increment/decrement buttons, and spacers
    for widget in timer_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg="white", fg="black")
        elif isinstance(widget, tk.Button):
            widget.config(bg="white", fg="black")

    for spacer in timer_spacers:
        spacer.config(bg="white", fg="black")

def night_mode():
    global bright, trigger_sound
    trigger_sound = False
    bright = 1

def getNightMode():
    global enable_night
    return enable_night

def enable_NM():
    global enable_night
    if not enable_night:
        enable_night = True
        night_mode()
        dark_bright()
    elif enable_night:
        enable_night = False
        full_bright()
    else:
        night_mode()

def clock():
    if RTclk_label:
        pst = datetime.now(pytz.timezone('US/Pacific'))
        RTclk_label.config(text=f"{pst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    root.after(1000, clock)

# Confidence threshold functions (preserved)
def increment_confidence():
    global confidence_threshold
    confidence_threshold = min(100, confidence_threshold + 10)
    confidence_label.config(text=f"{confidence_threshold}%")

def decrement_confidence():
    global confidence_threshold
    confidence_threshold = max(0, confidence_threshold - 10)
    confidence_label.config(text=f"{confidence_threshold}%")

def getConfidenceThreshold():
    global confidence_threshold
    return confidence_threshold

def SettingsUI():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("300x280")
    settings_frame = ttk.Frame(settings_win, padding=10)
    settings_frame.pack(fill=tk.BOTH, expand=True)
    # For this window, we now configure three columns (for confidence controls)
    for i in range(8):
        settings_frame.rowconfigure(i, weight=1)
    for j in range(3):
        settings_frame.columnconfigure(j, weight=1)

    tk.Label(settings_frame, text="Night Mode:", font=("Times New Roman", 16, "bold"))\
        .grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    tk.Button(settings_frame, text="ON / OFF", command=enable_NM, font=("Times New Roman", 16, "bold"))\
        .grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

    tk.Label(settings_frame, text="Brightness:", font=("Times New Roman", 16, "bold"))\
        .grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=(15,5))
    tk.Button(settings_frame, text="Dark", command=dark_bright, font=("Times New Roman", 16, "bold"))\
        .grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    tk.Button(settings_frame, text="Medium", command=medium_bright, font=("Times New Roman", 16, "bold"))\
        .grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    tk.Button(settings_frame, text="Bright", command=full_bright, font=("Times New Roman", 16, "bold"))\
        .grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    tk.Label(settings_frame, text="Confidence Threshold:", font=("Times New Roman", 16, "bold"))\
        .grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=(15,5))
    # Arrange the - button, value, and + button on a single row (row 4)
    tk.Button(settings_frame, text="-", command=decrement_confidence, font=("Times New Roman", 16, "bold"))\
        .grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
    global confidence_label
    confidence_label = tk.Label(settings_frame, text=f"{confidence_threshold}%", font=("Times New Roman", 16, "bold"))
    confidence_label.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
    tk.Button(settings_frame, text="+", command=increment_confidence, font=("Times New Roman", 16, "bold"))\
        .grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

    tk.Label(settings_frame, text="Return:", font=("Times New Roman", 16, "bold"))\
        .grid(row=5, column=0, sticky="nsew", padx=5, pady=(15,5))
    tk.Button(settings_frame, text="Back", command=settings_win.destroy, font=("Times New Roman", 16, "bold"))\
        .grid(row=5, column=1, columnspan=2, sticky="nsew", padx=5, pady=(15,5))

def UI():
    global root, frm, RTclk_label, hour_label, minute_label, second_label, Timer_stop_count, confidence_label, timer_frame, timer_spacers
    root = tk.Tk()
    root.geometry("480x320")
    root.title("Raspberry Pi Timer")
    frm = ttk.Frame(root, padding=0)
    frm.grid(sticky="nsew")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Set row and column weights for the main frame
    for r in range(8):
        frm.rowconfigure(r, weight=1)
    for c in range(6):
        frm.columnconfigure(c, weight=1)

    # Real-time clock label at the top
    RTclk_label = tk.Label(frm, text="Loading...", font=("Times New Roman", 25))
    RTclk_label.grid(column=0, row=0, columnspan=6, sticky="nsew")

    # Timer frame: three rows (plus buttons, digits, minus buttons)
    timer_frame = tk.Frame(frm)
    timer_frame.grid(column=0, row=1, columnspan=6, sticky="nsew")
    # Use 5 columns: hour, colon, minute, colon, second
    timer_frame.columnconfigure(0, weight=1, uniform="time")
    timer_frame.columnconfigure(1, weight=0)
    timer_frame.columnconfigure(2, weight=1, uniform="time")
    timer_frame.columnconfigure(3, weight=0)
    timer_frame.columnconfigure(4, weight=1, uniform="time")
    for r in range(3):
        timer_frame.rowconfigure(r, weight=1)

    # Row 0: Plus buttons
    tk.Button(timer_frame, text="+", command=increment_hr, font=("Times New Roman", 28, "bold"))\
        .grid(row=0, column=0, sticky="nsew")
    spacer = tk.Label(timer_frame, text="", font=("Times New Roman", 28))
    spacer.grid(row=0, column=1)
    timer_spacers.append(spacer)
    tk.Button(timer_frame, text="+", command=increment_min, font=("Times New Roman", 28, "bold"))\
        .grid(row=0, column=2, sticky="nsew")
    spacer = tk.Label(timer_frame, text="", font=("Times New Roman", 28))
    spacer.grid(row=0, column=3)
    timer_spacers.append(spacer)
    tk.Button(timer_frame, text="+", command=increment_sec, font=("Times New Roman", 28, "bold"))\
        .grid(row=0, column=4, sticky="nsew")

    # Row 1: Timer digits with colons between
    hour_label = tk.Label(timer_frame, text="00", font=("Courier", 48))
    hour_label.grid(row=1, column=0, sticky="nsew")
    tk.Label(timer_frame, text=":", font=("Courier", 48)).grid(row=1, column=1, sticky="nsew")
    minute_label = tk.Label(timer_frame, text="00", font=("Courier", 48))
    minute_label.grid(row=1, column=2, sticky="nsew")
    tk.Label(timer_frame, text=":", font=("Courier", 48)).grid(row=1, column=3, sticky="nsew")
    second_label = tk.Label(timer_frame, text="00", font=("Courier", 48))
    second_label.grid(row=1, column=4, sticky="nsew")

    # Row 2: Minus buttons
    tk.Button(timer_frame, text="-", command=decrement_hr, font=("Times New Roman", 28, "bold"))\
        .grid(row=2, column=0, sticky="nsew")
    spacer = tk.Label(timer_frame, text="", font=("Times New Roman", 28))
    spacer.grid(row=2, column=1)
    timer_spacers.append(spacer)
    tk.Button(timer_frame, text="-", command=decrement_min, font=("Times New Roman", 28, "bold"))\
        .grid(row=2, column=2, sticky="nsew")
    spacer = tk.Label(timer_frame, text="", font=("Times New Roman", 28))
    spacer.grid(row=2, column=3)
    timer_spacers.append(spacer)
    tk.Button(timer_frame, text="-", command=decrement_sec, font=("Times New Roman", 28, "bold"))\
        .grid(row=2, column=4, sticky="nsew")

    # Start and Stop Timer buttons in the next row of frm
    tk.Button(frm, text="Start Timer", command=start_timer, font=("Times New Roman", 20, "bold"))\
        .grid(column=0, row=2, columnspan=3, sticky="nsew", padx=(40, 10))
    tk.Button(frm, text="Stop Timer", command=stop_timer, font=("Times New Roman", 20, "bold"))\
        .grid(column=3, row=2, columnspan=3, sticky="nsew", padx=(10, 40))

    Timer_stop_count = tk.Label(frm, text="Timer Stops: 0", font=("Times New Roman", 16))
    Timer_stop_count.grid(column=0, row=3, columnspan=6, sticky="nsew")

    # Settings button in the bottom-right corner
    tk.Button(frm, text="\u2699", command=SettingsUI, font=("Times New Roman", 28, "bold"))\
        .grid(column=5, row=7, sticky="se")

    clock()
    root.mainloop()

def main():
    global time_left, bright, timer_running, present_object, trigger_sound, enable_night, timer_stopped, confidence_threshold
    timer_stopped = 0
    time_left = 0
    bright = 2
    timer_running = False
    present_object = True
    trigger_sound = False
    enable_night = False
    confidence_threshold = 20
    UI()

if __name__ == "__main__":
    main()
