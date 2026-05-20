import random
import string
import tkinter as tk
from tkinter import messagebox

class PasswordGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):
        frame = tk.Frame(self, padx=12, pady=12)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="Password Length:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=16)
        tk.Scale(frame, from_=8, to=32, orient="horizontal", variable=self.length_var, length=240).grid(row=1, column=0, columnspan=2, pady=(0, 12))

        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        tk.Checkbutton(frame, text="Include uppercase", variable=self.uppercase_var, font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w")
        tk.Checkbutton(frame, text="Include lowercase", variable=self.lowercase_var, font=("Segoe UI", 11)).grid(row=3, column=0, sticky="w")
        tk.Checkbutton(frame, text="Include digits", variable=self.digits_var, font=("Segoe UI", 11)).grid(row=4, column=0, sticky="w")
        tk.Checkbutton(frame, text="Include symbols", variable=self.symbols_var, font=("Segoe UI", 11)).grid(row=5, column=0, sticky="w")

        tk.Label(frame, text="Generated Password:", font=("Segoe UI", 11)).grid(row=6, column=0, sticky="w", pady=(12, 0))
        self.password_entry = tk.Entry(frame, font=("Segoe UI", 12), width=34, justify="center")
        self.password_entry.grid(row=7, column=0, columnspan=2, pady=4)

        button_frame = tk.Frame(frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=8)

        tk.Button(button_frame, text="Generate", font=("Segoe UI", 11), width=12, command=self.generate_password).grid(row=0, column=0, padx=4)
        tk.Button(button_frame, text="Copy", font=("Segoe UI", 11), width=12, command=self.copy_password).grid(row=0, column=1, padx=4)

        self.bind('<Return>', lambda event: self.generate_password())

    def generate_password(self):
        length = self.length_var.get()
        choices = ""

        if self.uppercase_var.get():
            choices += string.ascii_uppercase
        if self.lowercase_var.get():
            choices += string.ascii_lowercase
        if self.digits_var.get():
            choices += string.digits
        if self.symbols_var.get():
            choices += string.punctuation

        if not choices:
            messagebox.showwarning("Selection required", "Choose at least one character set.")
            return

        password = "".join(random.choice(choices) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return

        self.clipboard_clear()
        self.clipboard_append(password)
        self.update()  # keep clipboard content after window closes
        messagebox.showinfo("Copied", "Password copied to clipboard.")

if __name__ == "__main__":
    PasswordGenerator().mainloop()
