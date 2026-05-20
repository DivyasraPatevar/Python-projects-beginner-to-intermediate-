import tkinter as tk
from tkinter import ttk, messagebox

class UnitConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unit Converter")
        self.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Category:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.category_var = tk.StringVar(value="Length")
        categories = ["Length", "Weight", "Temperature"]
        self.category_menu = ttk.Combobox(frame, textvariable=self.category_var, values=categories, state="readonly", width=18)
        self.category_menu.grid(row=0, column=1, pady=4, sticky="w")
        self.category_menu.bind("<<ComboboxSelected>>", lambda event: self._update_units())

        ttk.Label(frame, text="From:", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w")
        self.from_var = tk.StringVar(value="Meter")
        self.from_menu = ttk.Combobox(frame, textvariable=self.from_var, values=[], state="readonly", width=18)
        self.from_menu.grid(row=1, column=1, pady=4, sticky="w")

        ttk.Label(frame, text="To:", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w")
        self.to_var = tk.StringVar(value="Kilometer")
        self.to_menu = ttk.Combobox(frame, textvariable=self.to_var, values=[], state="readonly", width=18)
        self.to_menu.grid(row=2, column=1, pady=4, sticky="w")

        ttk.Label(frame, text="Value:", font=("Segoe UI", 11)).grid(row=3, column=0, sticky="w")
        self.value_entry = ttk.Entry(frame, width=21, font=("Segoe UI", 11))
        self.value_entry.grid(row=3, column=1, pady=4, sticky="w")
        self.value_entry.insert(0, "0")

        ttk.Button(frame, text="Convert", command=self.convert).grid(row=4, column=0, pady=10, sticky="w")
        ttk.Button(frame, text="Clear", command=self.clear).grid(row=4, column=1, pady=10, sticky="w")

        ttk.Label(frame, text="Result:", font=("Segoe UI", 11)).grid(row=5, column=0, sticky="w")
        self.result_var = tk.StringVar(value="0")
        self.result_label = ttk.Label(frame, textvariable=self.result_var, font=("Segoe UI", 12, "bold"))
        self.result_label.grid(row=5, column=1, sticky="w")

        self._update_units()

    def _update_units(self):
        category = self.category_var.get()
        units = []
        if category == "Length":
            units = ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"]
        elif category == "Weight":
            units = ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"]
        elif category == "Temperature":
            units = ["Celsius", "Fahrenheit", "Kelvin"]

        self.from_menu.config(values=units)
        self.to_menu.config(values=units)
        if units:
            self.from_var.set(units[0])
            self.to_var.set(units[1] if len(units) > 1 else units[0])

    def convert(self):
        value = self.value_entry.get().strip()
        try:
            number = float(value)
        except ValueError:
            messagebox.showerror("Invalid input", "Enter a numeric value to convert.")
            return

        category = self.category_var.get()
        from_unit = self.from_var.get()
        to_unit = self.to_var.get()

        try:
            if category == "Length":
                result = self._convert_length(number, from_unit, to_unit)
            elif category == "Weight":
                result = self._convert_weight(number, from_unit, to_unit)
            else:
                result = self._convert_temperature(number, from_unit, to_unit)
        except ValueError as error:
            messagebox.showerror("Conversion error", str(error))
            return

        self.result_var.set(f"{result:.6g} {to_unit}")

    def clear(self):
        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0, "0")
        self.result_var.set("0")

    def _convert_length(self, value, from_unit, to_unit):
        factors = {
            "Meter": 1,
            "Kilometer": 1000,
            "Centimeter": 0.01,
            "Millimeter": 0.001,
            "Mile": 1609.344,
            "Yard": 0.9144,
            "Foot": 0.3048,
            "Inch": 0.0254,
        }
        return value * factors[from_unit] / factors[to_unit]

    def _convert_weight(self, value, from_unit, to_unit):
        factors = {
            "Kilogram": 1,
            "Gram": 0.001,
            "Milligram": 0.000001,
            "Pound": 0.45359237,
            "Ounce": 0.0283495231,
        }
        return value * factors[from_unit] / factors[to_unit]

    def _convert_temperature(self, value, from_unit, to_unit):
        if from_unit == to_unit:
            return value

        # convert to Celsius
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            raise ValueError("Unsupported temperature unit")

        if to_unit == "Celsius":
            return celsius
        if to_unit == "Fahrenheit":
            return celsius * 9 / 5 + 32
        if to_unit == "Kelvin":
            return celsius + 273.15
        raise ValueError("Unsupported temperature unit")

if __name__ == "__main__":
    UnitConverter().mainloop()
