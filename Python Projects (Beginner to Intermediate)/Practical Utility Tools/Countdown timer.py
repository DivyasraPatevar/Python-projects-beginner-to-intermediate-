import tkinter as tk
from tkinter import messagebox

class CountdownTimer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Countdown Timer")
        self.resizable(False, False)
        self.remaining_seconds = 0
        self.timer_id = None
        self.is_paused = False
        self._create_widgets()

    def _create_widgets(self):
        frame = tk.Frame(self, padx=12, pady=12)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="Minutes:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="e", pady=4)
        self.minutes_var = tk.StringVar(value="0")
        tk.Entry(frame, width=5, font=("Segoe UI", 12), textvariable=self.minutes_var).grid(row=0, column=1, pady=4)

        tk.Label(frame, text="Seconds:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", pady=4)
        self.seconds_var = tk.StringVar(value="0")
        tk.Entry(frame, width=5, font=("Segoe UI", 12), textvariable=self.seconds_var).grid(row=1, column=1, pady=4)

        self.time_label = tk.Label(frame, text="00:00", font=("Segoe UI", 32), width=6)
        self.time_label.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=4)

        self.start_button = tk.Button(button_frame, text="Start", font=("Segoe UI", 12), width=10, command=self.start)
        self.start_button.grid(row=0, column=0, padx=4)
        self.pause_button = tk.Button(button_frame, text="Pause", font=("Segoe UI", 12), width=10, command=self.pause, state="disabled")
        self.pause_button.grid(row=0, column=1, padx=4)
        self.reset_button = tk.Button(button_frame, text="Reset", font=("Segoe UI", 12), width=10, command=self.reset, state="disabled")
        self.reset_button.grid(row=0, column=2, padx=4)

        self.bind('<Return>', lambda event: self.start())
        self.bind('<Escape>', lambda event: self.reset())

    def start(self):
        if self.timer_id:
            return

        if self.remaining_seconds > 0 and self.is_paused:
            self.is_paused = False
            self._update_buttons(running=True)
            self._tick()
            return

        try:
            minutes = int(self.minutes_var.get().strip())
            seconds = int(self.seconds_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid input", "Enter whole numbers for minutes and seconds.")
            return

        if minutes < 0 or seconds < 0 or seconds >= 60:
            messagebox.showerror("Invalid input", "Minutes must be >= 0 and seconds must be 0-59.")
            return

        self.remaining_seconds = minutes * 60 + seconds
        if self.remaining_seconds <= 0:
            messagebox.showerror("Invalid input", "Enter a time greater than 0 seconds.")
            return

        self.is_paused = False
        self._update_buttons(running=True)
        self._tick()

    def _tick(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.time_label.config(text=f"{minutes:02}:{seconds:02}")

        if self.remaining_seconds <= 0:
            self._finish()
            return

        self.remaining_seconds -= 1
        self.timer_id = self.after(1000, self._tick)

    def pause(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            self.is_paused = True
            self._update_buttons(running=False)

    def reset(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.remaining_seconds = 0
        self.is_paused = False
        self.time_label.config(text="00:00")
        self._update_buttons(running=False)
        self.minutes_var.set("0")
        self.seconds_var.set("0")

    def _finish(self):
        self.timer_id = None
        self.is_paused = False
        self._update_buttons(running=False)
        self.bell()
        messagebox.showinfo("Time's up!", "Countdown finished.")

    def _update_buttons(self, running: bool):
        start_text = "Resume" if self.is_paused else "Start"
        self.start_button.config(state="disabled" if running else "normal", text=start_text)
        self.pause_button.config(state="normal" if running else "disabled")
        self.reset_button.config(state="normal" if running or self.remaining_seconds > 0 else "disabled")

if __name__ == "__main__":
    CountdownTimer().mainloop()
