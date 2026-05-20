import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class FileSorterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Sorter")
        self.resizable(False, False)
        self.selected_folder = tk.StringVar()
        self._create_widgets()

    def _create_widgets(self):
        frame = tk.Frame(self, padx=12, pady=12)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="Source Folder:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.selected_folder, width=48, font=("Segoe UI", 11)).grid(row=1, column=0, pady=(0, 8), sticky="w")
        tk.Button(frame, text="Browse...", font=("Segoe UI", 11), width=12, command=self.choose_folder).grid(row=1, column=1, padx=(8,0))

        tk.Button(frame, text="Sort Files", font=("Segoe UI", 11), width=20, command=self.sort_files).grid(row=2, column=0, columnspan=2, pady=8)

        tk.Label(frame, text="Sort mode:", font=("Segoe UI", 11)).grid(row=3, column=0, sticky="w")
        self.mode_var = tk.StringVar(value="extension")
        modes = [("By extension", "extension"), ("By type folder", "type"), ("By first letter", "letter")]
        for index, (label, value) in enumerate(modes, start=4):
            tk.Radiobutton(frame, text=label, variable=self.mode_var, value=value, font=("Segoe UI", 11)).grid(row=index, column=0, sticky="w")

        tk.Label(frame, text="Status:", font=("Segoe UI", 11)).grid(row=7, column=0, sticky="w", pady=(8,0))
        self.status_label = tk.Label(frame, text="Select a folder to start.", font=("Segoe UI", 10), fg="gray")
        self.status_label.grid(row=8, column=0, columnspan=2, sticky="w")

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.selected_folder.set(folder)
            self.status_label.config(text=f"Folder selected: {folder}")

    def sort_files(self):
        folder = self.selected_folder.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Invalid folder", "Please select a valid source folder.")
            return
        if not os.listdir(folder):
            messagebox.showinfo("Empty folder", "Selected folder is empty.")
            return

        mode = self.mode_var.get()
        self.status_label.config(text="Sorting files...")
        try:
            self._perform_sort(folder, mode)
            self.status_label.config(text="Sorting complete.")
            messagebox.showinfo("Done", "Files sorted successfully.")
        except Exception as error:
            self.status_label.config(text="Sort failed.")
            messagebox.showerror("Error", f"Sorting failed:\n{error}")

    def _perform_sort(self, folder, mode):
        for item in os.listdir(folder):
            source_path = os.path.join(folder, item)
            if os.path.isdir(source_path):
                continue

            if mode == "extension":
                target_folder = self._get_extension_folder(item)
            elif mode == "type":
                target_folder = self._get_type_folder(item)
            else:
                target_folder = self._get_letter_folder(item)

            target_path = os.path.join(folder, target_folder)
            os.makedirs(target_path, exist_ok=True)
            shutil.move(source_path, os.path.join(target_path, item))

    def _get_extension_folder(self, filename):
        name, ext = os.path.splitext(filename)
        return ext[1:].lower() + "_files" if ext else "no_extension"

    def _get_type_folder(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]:
            return "Images"
        if ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv"]:
            return "Videos"
        if ext in [".mp3", ".wav", ".flac", ".aac"]:
            return "Audio"
        if ext in [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"]:
            return "Documents"
        if ext in [".zip", ".rar", ".7z", ".tar", ".gz"]:
            return "Archives"
        return "Others"

    def _get_letter_folder(self, filename):
        first = filename[0].upper() if filename else "#"
        return first if first.isalpha() else "Other"

if __name__ == "__main__":
    FileSorterApp().mainloop()
