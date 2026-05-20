import tkinter as tk
from tkinter import messagebox

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.expression = ""
        self._create_widgets()

    def _create_widgets(self):
        self.display = tk.Entry(self, font=("Segoe UI", 20), borderwidth=2, relief="ridge", justify="right")
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=8)
        self.display.insert(0, "0")

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0), ("(", 5, 1), (")", 5, 2), ("⌫", 5, 3),
        ]

        for (text, row, column) in buttons:
            if text == "=":
                action = self._evaluate
            elif text == "C":
                action = self._clear
            elif text == "⌫":
                action = self._backspace
            else:
                action = lambda char=text: self._append(char)

            button = tk.Button(self, text=text, width=5, height=2, font=("Segoe UI", 16), command=action)
            button.grid(row=row, column=column, sticky="nsew", padx=4, pady=4)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        self.bind('<Key>', self._on_keypress)

    def _append(self, char: str) -> None:
        if self.expression == "" and char in "+-*/":
            return
        self.expression += char
        self._update_display(self.expression)

    def _clear(self) -> None:
        self.expression = ""
        self._update_display("0")

    def _backspace(self) -> None:
        self.expression = self.expression[:-1]
        self._update_display(self.expression if self.expression else "0")

    def _evaluate(self) -> None:
        try:
            result = eval(self.expression)
            self.expression = str(result)
            self._update_display(self.expression)
        except Exception:
            messagebox.showerror("Error", "Invalid expression")
            self._clear()

    def _update_display(self, text: str) -> None:
        self.display.delete(0, tk.END)
        self.display.insert(0, text)

    def _on_keypress(self, event):
        char = event.char
        if char in "0123456789.+-*/()":
            self._append(char)
        elif event.keysym == "Return":
            self._evaluate()
        elif event.keysym == "BackSpace":
            self._backspace()
        elif event.keysym == "Escape":
            self._clear()

if __name__ == "__main__":
    Calculator().mainloop()
