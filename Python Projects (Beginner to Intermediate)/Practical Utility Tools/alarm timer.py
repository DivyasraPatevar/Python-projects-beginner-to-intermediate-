import datetime
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

try:
    import winsound
except ImportError:
    winsound = None


def play_alarm_sound(repeats=5, duration=700, frequency=1000):
    if sys.platform.startswith("win") and winsound:
        for _ in range(repeats):
            winsound.Beep(frequency, duration)
            time.sleep(0.2)
    else:
        for _ in range(repeats):
            print("\a", end="", flush=True)
            time.sleep(duration / 1000.0)


def run_alarm(alarm_time, message_text, status_var):
    while True:
        now = datetime.datetime.now()
        if now >= alarm_time:
            status_var.set("Alarm triggered!")
            play_alarm_sound()
            messagebox.showinfo("Alarm", message_text)
            status_var.set("Alarm finished.")
            break
        time.sleep(1)


def parse_alarm_time(time_text):
    parts = [p.strip() for p in time_text.split(":") if p.strip()]
    if len(parts) not in (2, 3):
        raise ValueError("Enter time as HH:MM or HH:MM:SS")

    hour = int(parts[0])
    minute = int(parts[1])
    second = int(parts[2]) if len(parts) == 3 else 0

    if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
        raise ValueError("Hour must be 0-23, minute/second must be 0-59")

    now = datetime.datetime.now()
    alarm_time = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
    if alarm_time <= now:
        alarm_time += datetime.timedelta(days=1)
    return alarm_time


def start_alarm(status_var, time_entry, message_entry, start_button):
    time_text = time_entry.get().strip()
    message_text = message_entry.get().strip() or "Time is up!"

    try:
        alarm_time = parse_alarm_time(time_text)
    except ValueError as exc:
        messagebox.showerror("Invalid time", str(exc))
        return

    status_var.set(f"Alarm set for {alarm_time.strftime('%H:%M:%S')}")
    start_button.config(state="disabled")

    def worker():
        run_alarm(alarm_time, message_text, status_var)
        start_button.config(state="normal")

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()


def build_gui():
    root = tk.Tk()
    root.title("Alarm Timer")
    root.geometry("360x200")
    root.resizable(False, False)

    tk.Label(root, text="Set alarm time (24-hour HH:MM or HH:MM:SS):", anchor="w").pack(fill="x", padx=12, pady=(12, 2))
    time_entry = tk.Entry(root, font=("Segoe UI", 12))
    time_entry.insert(0, "07:00")
    time_entry.pack(fill="x", padx=12, pady=(0, 10))

    tk.Label(root, text="Alarm message:", anchor="w").pack(fill="x", padx=12, pady=(0, 2))
    message_entry = tk.Entry(root, font=("Segoe UI", 12))
    message_entry.insert(0, "Wake up!")
    message_entry.pack(fill="x", padx=12, pady=(0, 10))

    status_var = tk.StringVar(value="Ready to set an alarm.")
    tk.Label(root, textvariable=status_var, anchor="w", fg="#333333").pack(fill="x", padx=12, pady=(0, 10))

    start_button = tk.Button(
        root,
        text="Set Alarm",
        font=("Segoe UI", 11, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#45a049",
        command=lambda: start_alarm(status_var, time_entry, message_entry, start_button),
    )
    start_button.pack(fill="x", padx=12, pady=(0, 10))

    def on_close():
        if messagebox.askokcancel("Quit", "Stop the alarm timer and exit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    build_gui()
