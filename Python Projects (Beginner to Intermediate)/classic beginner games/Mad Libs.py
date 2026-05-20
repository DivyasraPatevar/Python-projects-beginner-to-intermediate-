import tkinter as tk
from tkinter import messagebox

STORIES = {
    "1": {
        "title": "A Funny Day at the Zoo",
        "prompts": [
            ("animal", "Name an animal"),
            ("adjective", "Type an adjective"),
            ("verb", "Name a verb"),
            ("place", "Name a place"),
            ("food", "Name a food"),
        ],
        "template": (
            "Today I went to the zoo and saw a {adjective} {animal}.\n"
            "It decided to {verb} right in front of me, then ran to the {place}.\n"
            "After that, I shared my {food} with the {animal}. It was the funniest day ever!"
        ),
    },
    "2": {
        "title": "The Magic Adventure",
        "prompts": [
            ("name", "Enter a name"),
            ("color", "Name a color"),
            ("noun", "Name a noun"),
            ("adjective", "Type an adjective"),
            ("verb", "Name a verb"),
        ],
        "template": (
            "Once upon a time, {name} found a {color} {noun} in the forest.\n"
            "The object glowed {adjective} and began to {verb} by itself.\n"
            "From that moment, {name}'s life became a magical adventure."
        ),
    },
}


def start_gui():
    root = tk.Tk()
    root.title("Mad Libs")
    root.geometry("520x560")
    root.resizable(False, False)

    header = tk.Label(root, text="Welcome to Mad Libs!", font=("Arial", 18, "bold"))
    header.pack(pady=10)

    story_frame = tk.Frame(root)
    story_frame.pack(fill="x", padx=20)

    tk.Label(story_frame, text="Choose a story:", font=("Arial", 12)).pack(anchor="w")

    story_var = tk.StringVar(value="1")
    for key, story in STORIES.items():
        tk.Radiobutton(
            story_frame,
            text=f"{key}) {story['title']}",
            variable=story_var,
            value=key,
            font=("Arial", 11),
            anchor="w",
            justify="left",
        ).pack(fill="x", pady=2)

    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    footer = tk.Frame(root)
    footer.pack(fill="x", padx=20, pady=10)

    entries = {}

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def show_story_selection():
        clear_content()
        tk.Label(content_frame, text="Click Start to begin.", font=("Arial", 12)).pack(pady=20)
        start_button = tk.Button(
            content_frame,
            text="Start",
            font=("Arial", 12),
            width=16,
            command=lambda: build_prompt_form(story_var.get()),
        )
        start_button.pack(pady=10)

    def build_prompt_form(story_id):
        clear_content()
        story = STORIES[story_id]
        tk.Label(content_frame, text=story["title"], font=("Arial", 14, "bold")).pack(pady=6)
        form_frame = tk.Frame(content_frame)
        form_frame.pack(fill="x", pady=5)

        entries.clear()
        for key, prompt in story["prompts"]:
            row = tk.Frame(form_frame)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=prompt + ":", width=18, anchor="w", font=("Arial", 11)).pack(side="left")
            entry = tk.Entry(row, font=("Arial", 11), width=28)
            entry.pack(side="left", fill="x", expand=True)
            entries[key] = entry

        tk.Button(
            content_frame,
            text="Create Story",
            font=("Arial", 12),
            width=16,
            command=lambda: show_result(story_id),
        ).pack(pady=10)

    def show_result(story_id):
        story = STORIES[story_id]
        answers = {}
        for key, _prompt in story["prompts"]:
            value = entries[key].get().strip()
            if not value:
                messagebox.showwarning("Missing input", "Please fill in all fields before creating your story.")
                return
            answers[key] = value

        story_text = story["template"].format(**answers)
        clear_content()

        tk.Label(content_frame, text="Your Mad Libs Story", font=("Arial", 14, "bold")).pack(pady=6)
        text_box = tk.Text(content_frame, wrap="word", font=("Arial", 11), height=12)
        text_box.pack(fill="both", expand=True, pady=6)
        text_box.insert("1.0", story_text)
        text_box.config(state="disabled")

        button_frame = tk.Frame(content_frame)
        button_frame.pack(pady=10)
        tk.Button(
            button_frame,
            text="Play Again",
            font=("Arial", 11),
            width=12,
            command=show_story_selection,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="Exit",
            font=("Arial", 11),
            width=12,
            command=root.quit,
        ).pack(side="left", padx=5)

    show_story_selection()
    root.mainloop()


if __name__ == "__main__":
    start_gui()
