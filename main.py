from tkinter import messagebox, ttk
import tkinter as tk
import ttkbootstrap
import csv

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.current_theme = "flatly"

        self.notes = []
        self.current_note_index = None

        self.sidebar_frame = ttk.Frame(root, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar_label = ttk.Label(self.sidebar_frame, text="Previous Notes")
        self.sidebar_label.pack(pady=(10, 10))

        self.sidebar_listbox = tk.Listbox(self.sidebar_frame, width=30)
        self.sidebar_listbox.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar_scrollbar = ttk.Scrollbar(self.sidebar_frame, orient=tk.VERTICAL,
                                               command=self.sidebar_listbox.yview)
        self.sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar_listbox.config(yscrollcommand=self.sidebar_scrollbar.set)

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.title_label = ttk.Label(self.main_frame, text="Title")
        self.title_label.pack()

        self.title_entry = ttk.Entry(self.main_frame, width=100)
        self.title_entry.pack()

        self.content_label = ttk.Label(self.main_frame, text="Content")
        self.content_label.pack()

        self.content_text = tk.Text(self.main_frame, height=20, width=100)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        self.new_note_button = ttk.Button(self.main_frame, text="New Note", command=self.new_note)
        self.new_note_button.pack(side=tk.RIGHT, pady=10)

        self.sidebar_listbox.bind('<<ListboxSelect>>', self.on_note_select)

        self.save_button = ttk.Button(self.main_frame, text="Save Note", command=self.save_note)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ttk.Button(self.main_frame, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.toggle_theme_button = ttk.Button(self.main_frame, text="Toggle Dark Mode", command=self.toggle_theme)
        self.toggle_theme_button.pack(side=tk.RIGHT, padx=10)

        self.load_notes()
        self.populate_sidebar()

    def load_notes(self):
        try:
            with open('notes.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                self.notes = list(reader)
        except FileNotFoundError:
            self.notes = []

    def populate_sidebar(self):
        self.sidebar_listbox.delete(0, tk.END)
        for note in self.notes:
            self.sidebar_listbox.insert(tk.END, note[0])

    def save_note(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()

        if title and content:
            if self.current_note_index is not None:
                self.notes[self.current_note_index] = [title, content]
            else:
                self.notes.append([title, content])
            self.save_notes_to_csv()
            self.populate_sidebar()
        else:
            messagebox.showwarning("Warning", "Please fill in both title and content")

    def save_notes_to_csv(self):
        with open('notes.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.notes)

    def delete_note(self):
        if self.current_note_index is not None:
            confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this note?")
            if confirmed:
                del self.notes[self.current_note_index]
                self.save_notes_to_csv()
                self.clear_entries()
                self.populate_sidebar()
                self.current_note_index = None
        else:
            messagebox.showwarning("Warning", "Please select a note to delete")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def on_note_select(self, event):
        selected_index = self.sidebar_listbox.curselection()
        if selected_index:
            self.current_note_index = selected_index[0]
            selected_note = self.notes[self.current_note_index]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(tk.END, selected_note[0])
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, selected_note[1])
        else:
            self.current_note_index = None

    def new_note(self):
        self.current_note_index = None
        self.clear_entries()

    def toggle_theme(self):
        self.current_theme = "darkly" if self.current_theme == "flatly" else "flatly"
        self.root.style.theme_use(self.current_theme)


if __name__ == "__main__":
    root = ttkbootstrap.Window("Noted", "flatly")
    app = NoteApp(root)
    root.mainloop()
