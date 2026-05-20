import tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import urlencode
from urllib.request import urlopen, Request
import json

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="City:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.city_entry = ttk.Entry(frame, width=32)
        self.city_entry.grid(row=0, column=1, padx=(8, 0), pady=4)
        self.city_entry.insert(0, "New York")

        self.units_var = tk.StringVar(value="metric")
        ttk.Label(frame, text="Units:", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w")
        unit_menu = ttk.Combobox(frame, textvariable=self.units_var, values=["metric", "imperial"], state="readonly", width=30)
        unit_menu.grid(row=1, column=1, padx=(8, 0), pady=4)

        ttk.Button(frame, text="Get Weather", command=self.get_weather).grid(row=2, column=0, columnspan=2, pady=8)

        ttk.Separator(frame, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=8)

        self.result_text = tk.Text(frame, width=54, height=12, wrap="word", font=("Segoe UI", 10))
        self.result_text.grid(row=4, column=0, columnspan=2, pady=(0, 8))
        self.result_text.config(state="disabled")

        self.bind('<Return>', lambda event: self.get_weather())

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Input error", "Enter a city name.")
            return
        try:
            weather = self._fetch_weather(city)
            self._show_weather(weather)
        except Exception as exc:
            messagebox.showerror("Error", f"Could not fetch weather:\n{exc}")

    def _fetch_weather(self, city):
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?{urlencode({'name': city, 'count': 1})}"
        request = Request(geocode_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

        if not data.get("results"):
            raise ValueError("City not found.")

        location = data["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        units = self.units_var.get()
        unit_params = {"temperature_unit": "celsius" if units == "metric" else "fahrenheit"}
        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            + urlencode({
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                **unit_params,
            })
        )
        weather_request = Request(weather_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(weather_request, timeout=15) as weather_response:
            return json.loads(weather_response.read().decode("utf-8"))

    def _show_weather(self, weather):
        current = weather.get("current_weather", {})
        if not current:
            raise ValueError("Weather details unavailable.")

        temp = current.get("temperature")
        wind = current.get("windspeed")
        direction = current.get("winddirection")
        weather_code = current.get("weathercode")
        unit = "°C" if self.units_var.get() == "metric" else "°F"

        text = (
            f"Temperature: {temp}{unit}\n"
            f"Wind Speed: {wind} km/h\n"
            f"Wind Direction: {direction}°\n"
            f"Weather Code: {weather_code}\n"
            "\nNote: This app uses Open-Meteo and does not require an API key."
        )
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    WeatherApp().mainloop()
