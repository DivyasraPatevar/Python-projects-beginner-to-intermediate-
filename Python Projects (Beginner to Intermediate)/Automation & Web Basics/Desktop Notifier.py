import tkinter as tk
from tkinter import messagebox
import subprocess
import platform

class DesktopNotifier(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Desktop Notifier")
        self.resizable(False, False)
        self.remaining_seconds = 0
        self.timer_id = None
        self._create_widgets()

    def _create_widgets(self):
        frame = tk.Frame(self, padx=12, pady=12)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="Notification Title:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(frame, width=40, font=("Segoe UI", 11))
        self.title_entry.grid(row=1, column=0, pady=(0, 8))
        self.title_entry.insert(0, "Reminder")

        tk.Label(frame, text="Message:", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w")
        self.message_entry = tk.Entry(frame, width=40, font=("Segoe UI", 11))
        self.message_entry.grid(row=3, column=0, pady=(0, 8))
        self.message_entry.insert(0, "Time to take a break!")

        options_frame = tk.Frame(frame)
        options_frame.grid(row=4, column=0, pady=(0, 12), sticky="w")

        tk.Label(options_frame, text="Delay (seconds):", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.delay_entry = tk.Entry(options_frame, width=8, font=("Segoe UI", 11))
        self.delay_entry.grid(row=0, column=1, padx=(6, 0))
        self.delay_entry.insert(0, "10")

        self.status_label = tk.Label(frame, text="Ready to schedule a notification.", font=("Segoe UI", 10), fg="gray")
        self.status_label.grid(row=5, column=0, pady=(0, 8), sticky="w")

        button_frame = tk.Frame(frame)
        button_frame.grid(row=6, column=0, sticky="w")

        tk.Button(button_frame, text="Schedule", font=("Segoe UI", 11), width=12, command=self.schedule_notification).grid(row=0, column=0, padx=(0, 6))
        tk.Button(button_frame, text="Cancel", font=("Segoe UI", 11), width=12, command=self.cancel_notification).grid(row=0, column=1)

        self.bind('<Return>', lambda event: self.schedule_notification())

    def schedule_notification(self):
        if self.timer_id:
            messagebox.showinfo("Already Scheduled", "A notification is already scheduled.")
            return

        title = self.title_entry.get().strip() or "Reminder"
        message = self.message_entry.get().strip() or "Your notification is ready."

        try:
            delay = int(self.delay_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid delay", "Enter a whole number of seconds.")
            return

        if delay < 0:
            messagebox.showerror("Invalid delay", "Delay must be zero or positive.")
            return

        self.target_title = title
        self.target_message = message
        self.remaining_seconds = delay
        self._update_status()
        self._tick()

    def _tick(self):
        if self.remaining_seconds < 0:
            return

        if self.remaining_seconds == 0:
            self._notify()
            return

        self.status_label.config(text=f"Notification in {self.remaining_seconds} second(s)...")
        self.remaining_seconds -= 1
        self.timer_id = self.after(1000, self._tick)

    def cancel_notification(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            self.remaining_seconds = 0
            self.status_label.config(text="Notification canceled.")
        else:
            self.status_label.config(text="No notification scheduled.")

    def _notify(self):
        self.timer_id = None
        self.status_label.config(text="Notification delivered.")
        self._send_desktop_notification(self.target_title, self.target_message)

    def _send_desktop_notification(self, title, message):
        if platform.system() == "Windows":
            try:
                script = (
                    "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime];"
                    " $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);"
                    f" $textNodes = $template.GetElementsByTagName(\"text\");"
                    f" $textNodes.Item(0).AppendChild($template.CreateTextNode(\"{title}\")) | Out-Null;"
                    f" $textNodes.Item(1).AppendChild($template.CreateTextNode(\"{message}\")) | Out-Null;"
                    " $toast = [Windows.UI.Notifications.ToastNotification]::new($template);"
                    " $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier(\"Desktop Notifier\");"
                    " $notifier.Show($toast);"
                )
                subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], check=True, capture_output=True)
                return
            except Exception:
                pass

        messagebox.showinfo(title, message)

    def _update_status(self):
        if self.remaining_seconds == 0:
            self.status_label.config(text="Ready to schedule a notification.")
        else:
            self.status_label.config(text=f"Notification in {self.remaining_seconds} second(s)...")

if __name__ == "__main__":
    DesktopNotifier().mainloop()
