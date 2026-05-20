import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from urllib.parse import urlparse
import urllib.request
import ssl

class SimpleWebScraper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Web Scraper")
        self.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="URL:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.url_entry = ttk.Entry(frame, width=60)
        self.url_entry.grid(row=1, column=0, columnspan=2, pady=(0, 8), sticky="w")
        self.url_entry.insert(0, "https://")

        ttk.Label(frame, text="CSS selector (optional):", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w")
        self.selector_entry = ttk.Entry(frame, width=60)
        self.selector_entry.grid(row=3, column=0, columnspan=2, pady=(0, 8), sticky="w")

        ttk.Button(frame, text="Fetch HTML", command=self.fetch_html).grid(row=4, column=0, pady=(0, 8), sticky="w")
        ttk.Button(frame, text="Extract Text", command=self.extract_text).grid(row=4, column=1, pady=(0, 8), sticky="e")

        ttk.Label(frame, text="Result:", font=("Segoe UI", 11)).grid(row=5, column=0, sticky="w")
        self.result_box = scrolledtext.ScrolledText(frame, width=72, height=22, font=("Segoe UI", 10))
        self.result_box.grid(row=6, column=0, columnspan=2)

    def _validate_url(self, url):
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and parsed.netloc

    def _get_html(self, url):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(url, context=context, timeout=15) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")

    def fetch_html(self):
        url = self.url_entry.get().strip()
        if not self._validate_url(url):
            messagebox.showerror("Invalid URL", "Enter a valid http or https URL.")
            return

        try:
            html = self._get_html(url)
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, html)
        except Exception as error:
            messagebox.showerror("Fetch error", f"Failed to fetch the page:\n{error}")

    def extract_text(self):
        selector = self.selector_entry.get().strip()
        url = self.url_entry.get().strip()
        if not self._validate_url(url):
            messagebox.showerror("Invalid URL", "Enter a valid http or https URL.")
            return

        try:
            html = self._get_html(url)
            text = self._extract_with_selector(html, selector)
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, text)
        except Exception as error:
            messagebox.showerror("Extract error", f"Failed to extract text:\n{error}")

    def _extract_with_selector(self, html, selector):
        if not selector:
            return self._strip_tags(html)

        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise RuntimeError("BeautifulSoup is required for selector extraction. Install bs4.")

        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(selector)
        if not elements:
            return f"No elements found for selector: {selector}"
        return "\n\n".join(element.get_text(strip=True) for element in elements)

    def _strip_tags(self, html):
        text = []
        inside = False
        for char in html:
            if char == "<":
                inside = True
            elif char == ">":
                inside = False
            elif not inside:
                text.append(char)
        return "".join(text).strip()

if __name__ == "__main__":
    SimpleWebScraper().mainloop()
