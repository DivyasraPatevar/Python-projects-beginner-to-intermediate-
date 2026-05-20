import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = os.path.join(os.path.dirname(__file__), "todo_data.txt")

class ToDoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.resizable(False, False)
        self._create_widgets()
        self._load_tasks()

    def _create_widgets(self):
        frame = tk.Frame(self, padx=12, pady=12)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="New Task:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(frame, width=40, font=("Segoe UI", 11))
        self.task_entry.grid(row=1, column=0, columnspan=3, pady=(0, 8), sticky="w")
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        tk.Button(frame, text="Add Task", font=("Segoe UI", 11), width=12, command=self.add_task).grid(row=1, column=3, padx=(8, 0))

        self.tasks_listbox = tk.Listbox(frame, width=48, height=12, font=("Segoe UI", 11), selectmode=tk.SINGLE)
        self.tasks_listbox.grid(row=2, column=0, columnspan=4, pady=(4, 8))

        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=4)

        tk.Button(button_frame, text="Complete", font=("Segoe UI", 11), width=12, command=self.complete_task).grid(row=0, column=0, padx=4)
        tk.Button(button_frame, text="Remove", font=("Segoe UI", 11), width=12, command=self.remove_task).grid(row=0, column=1, padx=4)
        tk.Button(button_frame, text="Clear All", font=("Segoe UI", 11), width=12, command=self.clear_all).grid(row=0, column=2, padx=4)
        tk.Button(button_frame, text="Save", font=("Segoe UI", 11), width=12, command=self.save_tasks).grid(row=0, column=3, padx=4)

    def _load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    for line in file:
                        self.tasks_listbox.insert(tk.END, line.strip())
            except Exception:
                messagebox.showwarning("Load Error", "Could not load saved tasks.")

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showinfo("Empty Task", "Please enter a task before adding.")
            return
        self.tasks_listbox.insert(tk.END, task)
        self.task_entry.delete(0, tk.END)

    def complete_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a task to mark complete.")
            return
        index = selected[0]
        task = self.tasks_listbox.get(index)
        if task.startswith("✔ "):
            messagebox.showinfo("Already Completed", "This task is already marked complete.")
            return
        self.tasks_listbox.delete(index)
        self.tasks_listbox.insert(index, f"✔ {task}")

    def remove_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a task to remove.")
            return
        self.tasks_listbox.delete(selected[0])

    def clear_all(self):
        if messagebox.askyesno("Clear All", "Remove all tasks from the list?"):
            self.tasks_listbox.delete(0, tk.END)

    def save_tasks(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                for idx in range(self.tasks_listbox.size()):
                    file.write(self.tasks_listbox.get(idx) + "\n")
            messagebox.showinfo("Saved", "Tasks saved successfully.")
        except Exception:
            messagebox.showerror("Save Error", "Could not save tasks.")

if __name__ == "__main__":
    ToDoListApp().mainloop()
